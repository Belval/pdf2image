"""
    pdf2image is a light wrapper for the poppler-utils tools that can convert your
    PDFs into Pillow images.
"""

import os
import platform
import tempfile
import types
import shutil
import subprocess
from subprocess import Popen, PIPE, TimeoutExpired
from typing import Any, Union, Tuple, List, Dict, Callable
from pathlib import PurePath
from PIL import Image

from pdf2image.generators import uuid_generator, counter_generator, ThreadSafeGenerator

from pdf2image.parsers import (
    parse_buffer_to_pgm,
    parse_buffer_to_ppm,
    parse_buffer_to_jpeg,
    parse_buffer_to_png,
)

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError,
)

TRANSPARENT_FILE_TYPES = ["png", "tiff"]
PDFINFO_CONVERT_TO_INT = ["Pages"]


def convert_from_path(
        pdf_path: Union[str, PurePath],
        dpi: int = 200,
        output_folder: Union[str, PurePath] = None,
        first_page: int = None,
        last_page: int = None,
        fmt: str = "ppm",
        jpegopt: Dict = None,
        thread_count: int = 1,
        userpw: str = None,
        ownerpw: str = None,
        use_cropbox: bool = False,
        strict: bool = False,
        transparent: bool = False,
        single_file: bool = False,
        output_file: Any = uuid_generator(),
        poppler_path: Union[str, PurePath] = None,
        grayscale: bool = False,
        size: Union[Tuple, int] = None,
        paths_only: bool = False,
        use_pdftocairo: bool = False,
        timeout: int = None,
        hide_annotations: bool = False,
        page_indexes: List[int] = None  # 允许指定要转换的特定页面
) -> List[Image.Image]:
    """Function wrapping pdftoppm and pdftocairo, allowing page selection by indexes."""

    # 如果指定了 page_indexes 参数，我们需要重新调整 first_page 和 last_page
    if page_indexes is not None:
        page_indexes = sorted(set(page_indexes))  # 排序并去重
        first_page = page_indexes[0]
        last_page = page_indexes[-1]

    # 验证页面范围
    if first_page is None or first_page < 1:
        first_page = 1

    # 获取总页数
    page_count = pdfinfo_from_path(
        pdf_path, userpw, ownerpw, poppler_path=poppler_path
    )["Pages"]

    if last_page is None or last_page > page_count:
        last_page = page_count

    if first_page > last_page:
        return []

    # 确定使用的转换工具
    if use_pdftocairo and fmt == "ppm":
        fmt = "png"

    # 如果传递的是 PurePath 对象，转换为字符串
    if isinstance(pdf_path, PurePath):
        pdf_path = pdf_path.as_posix()

    if isinstance(output_folder, PurePath):
        output_folder = output_folder.as_posix()

    if isinstance(poppler_path, PurePath):
        poppler_path = poppler_path.as_posix()

    parsed_fmt, final_extension, parse_buffer_func, use_pdfcairo_format = _parse_format(
        fmt, grayscale
    )

    use_pdfcairo = (
            use_pdftocairo
            or use_pdfcairo_format
            or (transparent and parsed_fmt in TRANSPARENT_FILE_TYPES)
    )

    # 如果线程数超过页面数，则限制线程数
    if thread_count > len(page_indexes) if page_indexes else (last_page - first_page + 1):
        thread_count = len(page_indexes) if page_indexes else (last_page - first_page + 1)

    processes = []
    images = []

    try:
        auto_temp_dir = False
        if output_folder is None and use_pdfcairo:
            output_folder = tempfile.mkdtemp()
            auto_temp_dir = True

        # 多线程处理
        for i in range(thread_count):
            thread_output_file = next(output_file)

            # 获取该线程应处理的页面范围
            if page_indexes is not None:
                pages_to_process = page_indexes[i::thread_count]  # 均匀分配页面到每个线程
            else:
                pages_to_process = list(range(first_page + i, last_page + 1, thread_count))

            if not pages_to_process:
                continue

            first_page_in_thread = pages_to_process[0]
            last_page_in_thread = pages_to_process[-1]

            # 构建命令
            args = _build_command(
                ["-r", str(dpi), pdf_path],
                output_folder,
                first_page_in_thread,
                last_page_in_thread,
                parsed_fmt,
                jpegopt,
                thread_output_file,
                userpw,
                ownerpw,
                use_cropbox,
                transparent,
                single_file,
                grayscale,
                size,
                hide_annotations,
            )

            if use_pdfcairo:
                if hide_annotations:
                    raise NotImplementedError(
                        "Hide annotations flag not implemented in pdftocairo."
                    )
                args = [_get_command_path("pdftocairo", poppler_path)] + args
            else:
                args = [_get_command_path("pdftoppm", poppler_path)] + args

            # Add poppler path to LD_LIBRARY_PATH
            env = os.environ.copy()
            if poppler_path is not None:
                env["LD_LIBRARY_PATH"] = (
                        poppler_path + ":" + env.get("LD_LIBRARY_PATH", "")
                )
            startupinfo = None
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # 启动进程
            processes.append(
                (
                    thread_output_file,
                    Popen(
                        args, env=env, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo
                    ),
                )
            )

        # 等待所有进程完成并收集结果
        for uid, proc in processes:
            try:
                data, err = proc.communicate(timeout=timeout)
            except TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
                raise PDFPopplerTimeoutError("Run poppler timeout.")

            if b"Syntax Error" in err and strict:
                raise PDFSyntaxError(err.decode("utf8", "ignore"))

            if output_folder is not None:
                images += _load_from_output_folder(
                    output_folder,
                    uid,
                    final_extension,
                    paths_only,
                    in_memory=auto_temp_dir,
                )
            else:
                images += parse_buffer_func(data)
    finally:
        if auto_temp_dir:
            shutil.rmtree(output_folder)

    return images


def convert_from_bytes(
    pdf_file: bytes,
    dpi: int = 200,
    output_folder: Union[str, PurePath] = None,
    first_page: int = None,
    last_page: int = None,
    fmt: str = "ppm",
    jpegopt: Dict = None,
    thread_count: int = 1,
    userpw: str = None,
    ownerpw: str = None,
    use_cropbox: bool = False,
    strict: bool = False,
    transparent: bool = False,
    single_file: bool = False,
    output_file: Union[str, PurePath] = uuid_generator(),
    poppler_path: Union[str, PurePath] = None,
    grayscale: bool = False,
    size: Union[Tuple, int] = None,
    paths_only: bool = False,
    use_pdftocairo: bool = False,
    timeout: int = None,
    hide_annotations: bool = False,
) -> List[Image.Image]:
    """Function wrapping pdftoppm and pdftocairo.

    :param pdf_bytes: Bytes of the PDF that you want to convert
    :type pdf_bytes: bytes
    :param dpi: Image quality in DPI (default 200), defaults to 200
    :type dpi: int, optional
    :param output_folder: Write the resulting images to a folder (instead of directly in memory), defaults to None
    :type output_folder: Union[str, PurePath], optional
    :param first_page: First page to process, defaults to None
    :type first_page: int, optional
    :param last_page: Last page to process before stopping, defaults to None
    :type last_page: int, optional
    :param fmt: Output image format, defaults to "ppm"
    :type fmt: str, optional
    :param jpegopt: jpeg options `quality`, `progressive`, and `optimize` (only for jpeg format), defaults to None
    :type jpegopt: Dict, optional
    :param thread_count: How many threads we are allowed to spawn for processing, defaults to 1
    :type thread_count: int, optional
    :param userpw: PDF's password, defaults to None
    :type userpw: str, optional
    :param ownerpw: PDF's owner password, defaults to None
    :type ownerpw: str, optional
    :param use_cropbox: Use cropbox instead of mediabox, defaults to False
    :type use_cropbox: bool, optional
    :param strict: When a Syntax Error is thrown, it will be raised as an Exception, defaults to False
    :type strict: bool, optional
    :param transparent: Output with a transparent background instead of a white one, defaults to False
    :type transparent: bool, optional
    :param single_file: Uses the -singlefile option from pdftoppm/pdftocairo, defaults to False
    :type single_file: bool, optional
    :param output_file: What is the output filename or generator, defaults to uuid_generator()
    :type output_file: Any, optional
    :param poppler_path: Path to look for poppler binaries, defaults to None
    :type poppler_path: Union[str, PurePath], optional
    :param grayscale: Output grayscale image(s), defaults to False
    :type grayscale: bool, optional
    :param size: Size of the resulting image(s), uses the Pillow (width, height) standard, defaults to None
    :type size: Union[Tuple, int], optional
    :param paths_only: Don't load image(s), return paths instead (requires output_folder), defaults to False
    :type paths_only: bool, optional
    :param use_pdftocairo: Use pdftocairo instead of pdftoppm, may help performance, defaults to False
    :type use_pdftocairo: bool, optional
    :param timeout: Raise PDFPopplerTimeoutError after the given time, defaults to None
    :type timeout: int, optional
    :param hide_annotations: Hide PDF annotations in the output, defaults to False
    :type hide_annotations: bool, optional
    :raises NotImplementedError: Raised when conflicting parameters are given (hide_annotations for pdftocairo)
    :raises PDFPopplerTimeoutError: Raised after the timeout for the image processing is exceeded
    :raises PDFSyntaxError: Raised if there is a syntax error in the PDF and strict=True
    :return: A list of Pillow images, one for each page between first_page and last_page
    :rtype: List[Image.Image]
    """

    fh, temp_filename = tempfile.mkstemp()
    try:
        with open(temp_filename, "wb") as f:
            f.write(pdf_file)
            f.flush()
            return convert_from_path(
                f.name,
                dpi=dpi,
                output_folder=output_folder,
                first_page=first_page,
                last_page=last_page,
                fmt=fmt,
                jpegopt=jpegopt,
                thread_count=thread_count,
                userpw=userpw,
                ownerpw=ownerpw,
                use_cropbox=use_cropbox,
                strict=strict,
                transparent=transparent,
                single_file=single_file,
                output_file=output_file,
                poppler_path=poppler_path,
                grayscale=grayscale,
                size=size,
                paths_only=paths_only,
                use_pdftocairo=use_pdftocairo,
                timeout=timeout,
                hide_annotations=hide_annotations,
            )
    finally:
        os.close(fh)
        os.remove(temp_filename)


def _build_command(
    args: List,
    output_folder: str,
    first_page: int,
    last_page: int,
    fmt: str,
    jpegopt: Dict,
    output_file: str,
    userpw: str,
    ownerpw: str,
    use_cropbox: bool,
    transparent: bool,
    single_file: bool,
    grayscale: bool,
    size: Union[int, Tuple[int, int]],
    hide_annotations: bool,
) -> List[str]:
    if use_cropbox:
        args.append("-cropbox")

    if hide_annotations:
        args.append("-hide-annotations")

    if transparent and fmt in TRANSPARENT_FILE_TYPES:
        args.append("-transp")

    if first_page is not None:
        args.extend(["-f", str(first_page)])

    if last_page is not None:
        args.extend(["-l", str(last_page)])

    if fmt not in ["pgm", "ppm"]:
        args.append("-" + fmt)

    if fmt in ["jpeg", "jpg"] and jpegopt:
        args.extend(["-jpegopt", _parse_jpegopt(jpegopt)])

    if single_file:
        args.append("-singlefile")

    if output_folder is not None:
        args.append(os.path.join(output_folder, output_file))

    if userpw is not None:
        args.extend(["-upw", userpw])

    if ownerpw is not None:
        args.extend(["-opw", ownerpw])

    if grayscale:
        args.append("-gray")

    if size is None:
        pass
    elif isinstance(size, tuple) and len(size) == 2:
        if size[0] is not None:
            args.extend(["-scale-to-x", str(int(size[0]))])
        else:
            args.extend(["-scale-to-x", str(-1)])
        if size[1] is not None:
            args.extend(["-scale-to-y", str(int(size[1]))])
        else:
            args.extend(["-scale-to-y", str(-1)])
    elif isinstance(size, tuple) and len(size) == 1:
        args.extend(["-scale-to", str(int(size[0]))])
    elif isinstance(size, int) or isinstance(size, float):
        args.extend(["-scale-to", str(int(size))])
    else:
        raise ValueError(f"Size {size} is not a tuple or an integer")

    return args


def _parse_format(fmt: str, grayscale: bool = False) -> Tuple[str, str, Callable, bool]:
    fmt = fmt.lower()
    if fmt[0] == ".":
        fmt = fmt[1:]
    if fmt in ("jpeg", "jpg"):
        return "jpeg", "jpg", parse_buffer_to_jpeg, False
    if fmt == "png":
        return "png", "png", parse_buffer_to_png, False
    if fmt in ("tif", "tiff"):
        return "tiff", "tif", None, True
    if fmt == "ppm" and grayscale:
        return "pgm", "pgm", parse_buffer_to_pgm, False
    # Unable to parse the format so we'll use the default
    return "ppm", "ppm", parse_buffer_to_ppm, False


def _parse_jpegopt(jpegopt: Dict) -> str:
    parts = []
    for k, v in jpegopt.items():
        if v is True:
            v = "y"
        if v is False:
            v = "n"
        parts.append("{}={}".format(k, v))
    return ",".join(parts)


def _get_command_path(command: str, poppler_path: str = None) -> str:
    if platform.system() == "Windows":
        command = command + ".exe"

    if poppler_path is not None:
        command = os.path.join(poppler_path, command)

    return command


def _get_poppler_version(
    command: str, poppler_path: str = None, timeout: int = None
) -> Tuple[int, int]:
    command = [_get_command_path(command, poppler_path), "-v"]

    env = os.environ.copy()
    if poppler_path is not None:
        env["LD_LIBRARY_PATH"] = poppler_path + ":" + env.get("LD_LIBRARY_PATH", "")
    proc = Popen(command, env=env, stdout=PIPE, stderr=PIPE)

    try:
        data, err = proc.communicate(timeout=timeout)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        raise PDFPopplerTimeoutError("Run poppler poppler timeout.")

    try:
        # TODO: Make this more robust
        version = err.decode("utf8", "ignore").split("\n")[0].split(" ")[-1].split(".")
        return int(version[0]), int(version[1])
    except:
        # Lowest version that includes pdftocairo (2011)
        return 0, 17


def pdfinfo_from_path(
    pdf_path: str,
    userpw: str = None,
    ownerpw: str = None,
    poppler_path: str = None,
    rawdates: bool = False,
    timeout: int = None,
    first_page: int = None,
    last_page: int = None,
) -> Dict:
    """Function wrapping poppler's pdfinfo utility and returns the result as a dictionary.

    :param pdf_path: Path to the PDF that you want to convert
    :type pdf_path: str
    :param userpw: PDF's password, defaults to None
    :type userpw: str, optional
    :param ownerpw: PDF's owner password, defaults to None
    :type ownerpw: str, optional
    :param poppler_path: Path to look for poppler binaries, defaults to None
    :type poppler_path: Union[str, PurePath], optional
    :param rawdates: Return the undecoded data strings, defaults to False
    :type rawdates: bool, optional
    :param timeout: Raise PDFPopplerTimeoutError after the given time, defaults to None
    :type timeout: int, optional
    :param first_page: First page to process, defaults to None
    :type first_page: int, optional
    :param last_page: Last page to process before stopping, defaults to None
    :type last_page: int, optional
    :raises PDFPopplerTimeoutError: Raised after the timeout for the image processing is exceeded
    :raises PDFInfoNotInstalledError: Raised if pdfinfo is not installed
    :raises PDFPageCountError: Raised if the output could not be parsed
    :return: Dictionary containing various information on the PDF
    :rtype: Dict
    """
    try:
        command = [_get_command_path("pdfinfo", poppler_path), pdf_path]

        if userpw is not None:
            command.extend(["-upw", userpw])

        if ownerpw is not None:
            command.extend(["-opw", ownerpw])

        if rawdates:
            command.extend(["-rawdates"])

        if first_page:
            command.extend(["-f", str(first_page)])

        if last_page:
            command.extend(["-l", str(last_page)])

        # Add poppler path to LD_LIBRARY_PATH
        env = os.environ.copy()
        if poppler_path is not None:
            env["LD_LIBRARY_PATH"] = poppler_path + ":" + env.get("LD_LIBRARY_PATH", "")
        proc = Popen(command, env=env, stdout=PIPE, stderr=PIPE)

        try:
            out, err = proc.communicate(timeout=timeout)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
            raise PDFPopplerTimeoutError("Run poppler poppler timeout.")

        d = {}
        for field in out.decode("utf8", "ignore").split("\n"):
            sf = field.split(":")
            key, value = sf[0], ":".join(sf[1:])
            if key != "":
                d[key] = (
                    int(value.strip())
                    if key in PDFINFO_CONVERT_TO_INT
                    else value.strip()
                )

        if "Pages" not in d:
            raise ValueError

        return d

    except OSError:
        raise PDFInfoNotInstalledError(
            "Unable to get page count. Is poppler installed and in PATH?"
        )
    except ValueError:
        raise PDFPageCountError(
            f"Unable to get page count.\n{err.decode('utf8', 'ignore')}"
        )


def pdfinfo_from_bytes(
    pdf_bytes: bytes,
    userpw: str = None,
    ownerpw: str = None,
    poppler_path: str = None,
    rawdates: bool = False,
    timeout: int = None,
    first_page: int = None,
    last_page: int = None,
) -> Dict:
    """Function wrapping poppler's pdfinfo utility and returns the result as a dictionary.

    :param pdf_bytes: Bytes of the PDF that you want to convert
    :type pdf_bytes: bytes
    :param userpw: PDF's password, defaults to None
    :type userpw: str, optional
    :param ownerpw: PDF's owner password, defaults to None
    :type ownerpw: str, optional
    :param poppler_path: Path to look for poppler binaries, defaults to None
    :type poppler_path: Union[str, PurePath], optional
    :param rawdates: Return the undecoded data strings, defaults to False
    :type rawdates: bool, optional
    :param timeout: Raise PDFPopplerTimeoutError after the given time, defaults to None
    :type timeout: int, optional
    :param first_page: First page to process, defaults to None
    :type first_page: int, optional
    :param last_page: Last page to process before stopping, defaults to None
    :type last_page: int, optional
    :return: Dictionary containing various information on the PDF
    :rtype: Dict
    """
    fh, temp_filename = tempfile.mkstemp()
    try:
        with open(temp_filename, "wb") as f:
            f.write(pdf_bytes)
            f.flush()
        return pdfinfo_from_path(
            temp_filename,
            userpw=userpw,
            ownerpw=ownerpw,
            poppler_path=poppler_path,
            rawdates=rawdates,
            timeout=timeout,
            first_page=first_page,
            last_page=last_page,
        )
    finally:
        os.close(fh)
        os.remove(temp_filename)


def _load_from_output_folder(
    output_folder: str,
    output_file: str,
    ext: str,
    paths_only: bool,
    in_memory: bool = False,
) -> List[Image.Image]:
    images = []
    for f in sorted(os.listdir(output_folder)):
        if f.startswith(output_file) and f.split(".")[-1] == ext:
            if paths_only:
                images.append(os.path.join(output_folder, f))
            else:
                images.append(Image.open(os.path.join(output_folder, f)))
                if in_memory:
                    images[-1].load()
    return images
