import argparse

from generators import uuid_generator
from pdf2image import convert_from_path

# repackage will get around the issue of trying to call a runnable script with a __main__ block
# inside a module that has relative imports
# See https://stackoverflow.com/questions/16981921/relative-imports-in-python-3#47670795
import repackage
repackage.up()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line call to convert_from_path - Convert PDF to Image will throw whenever one of the condition is reached.", prog="convert_from_path.py")
    parser.add_argument("pdf_path", help="str: Path to the PDF that you want to convert. Required.")
    parser.add_argument("--dpi", type=int, default=200, help="int: Image quality in DPI. Default=200")
    parser.add_argument("--output_folder", help="str: Write the resulting images to a folder (instead of directly in memory).")
    parser.add_argument("--first_page", type=int, default=1, help="int: First page to process. Default=1")
    parser.add_argument("--last_page", type=int, help="int: Last page to process before stopping.")
    parser.add_argument("--fmt", "--format", default="ppm", help="str: Output image format. Default=ppm")
    parser.add_argument("--jpegopt", "--jpgopt", help="str: jpeg options `quality`, `progressive`, and `optimize` (only for jpeg format)")
    parser.add_argument("--thread_count", type=int, default=1, help="int: How many threads we are allowed to spawn for processing. Default=1")
    parser.add_argument("--userpw", help="str: PDF's password.")
    parser.add_argument("--use_cropbox", action="store_true", help="flag: Use cropbox instead of mediabox.")
    parser.add_argument("--strict", action="store_true", help="flag: When a Syntax Error is thrown, it will be raised as an Exception.")
    parser.add_argument("--transparent", action="store_true", help="flag: Output with a transparent background instead of a white one.")
    parser.add_argument("--single_file", action="store_true", help="flag: Uses the -singlefile option from pdftoppm/pdftocairo.")
    parser.add_argument("--output_file", default=uuid_generator(), help="str: What is the output filename or generator. Default=uuid_generator")
    parser.add_argument("--poppler_path", help="str: Path to look for poppler binaries.")
    parser.add_argument("--grayscale", action="store_true", help="flag: Output grayscale image(s).")
    parser.add_argument("--size", nargs='+', help="int or tuple: Size of the resulting image(s), uses the Pillow (width, height) standard. Ex: `--size 1000` or `--size None 2400`")
    parser.add_argument("--paths_only", action="store_true", help="flag: Don't load image(s), return paths instead (requires output_folder).")
    parser.add_argument("--use_pdftocairo", action="store_true", help="flag: Use pdftocairo instead of pdftoppm, may help performance.")
    parser.add_argument("--timeout", type=int, help="int: Raise PDFPopplerTimeoutError after the given time in seconds.")

    args = parser.parse_args()
    if args.size:
        # argparse cannot handle tuples, so need to deal with it as a list of strings and convert to a tuple.
        # https://stackoverflow.com/questions/33564246/passing-a-tuple-as-command-line-argument
        for index, item in enumerate(args.size):
            if item.lower() == "none":
                args.size[index] = None
            else:
                try:
                    args.size[index] = int(item)
                except:
                    # Leave as a string anything that cannot be converted to an int.
                    pass
        args.size = tuple(args.size)


    results = convert_from_path(
        args.pdf_path, 
        dpi=args.dpi, 
        output_folder=args.output_folder, 
        first_page=args.first_page,
        last_page=args.last_page,
        fmt=args.fmt,
        jpegopt=args.jpegopt,
        thread_count=args.thread_count,
        userpw=args.userpw,
        use_cropbox=args.use_cropbox,
        strict=args.strict,
        transparent=args.transparent,
        single_file=args.single_file,
        output_file=args.output_file,
        poppler_path=args.poppler_path,
        grayscale=args.grayscale,
        size=args.size,
        paths_only=args.paths_only,
        use_pdftocairo=args.use_pdftocairo,
        timeout=args.timeout
    )
    print(results)