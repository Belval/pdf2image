"""Deterministic coverage of conversion failures and bytes-wrapper forwarding."""
import unittest
from inspect import signature
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch, sentinel

from pdf2image import pdf2image as api
from pdf2image.exceptions import PDFPopplerTimeoutError


class ConversionFailureTests(unittest.TestCase):
    def setUp(self):
        self.info = self.patch("pdfinfo_from_path", return_value={"Pages": 2})
        self.patch("_get_poppler_version", return_value=(24, 1))
        self.launch = self.patch("Popen")

    def patch(self, name, **kwargs):
        patcher = patch.object(api, name, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def assert_failed_render(self, stdout):
        self.launch.return_value.returncode = 1
        self.launch.return_value.communicate.return_value = stdout, b"render failed"
        with self.assertRaisesRegex(Exception, "render failed"):
            api.convert_from_path("input.pdf")

    @unittest.expectedFailure
    def test_nonzero_exit_with_empty_output(self):
        self.assert_failed_render(b"")

    @unittest.expectedFailure
    def test_nonzero_exit_after_a_complete_page(self):
        self.assert_failed_render(b"P6\n1 1\n255\n" + bytes(3))

    @unittest.expectedFailure
    def test_page_count_receives_conversion_deadline(self):
        def probe(*args, timeout=None, **kwargs):
            if timeout is not None and 0 <= timeout <= 1:
                raise PDFPopplerTimeoutError("metadata timeout")
            return {"Pages": 2}

        self.info.side_effect = probe
        self.launch.return_value.communicate.return_value = b"", b""
        with self.assertRaises(PDFPopplerTimeoutError):
            api.convert_from_path("input.pdf", timeout=1)
        self.launch.assert_not_called()

    @unittest.expectedFailure
    def test_second_launch_failure_reaps_first_worker(self):
        worker = Mock()
        worker.poll.return_value = None
        self.launch.side_effect = [worker, OSError("launch failed")]
        with self.assertRaises(Exception):
            api.convert_from_path("input.pdf", thread_count=2)
        self.assertTrue(worker.kill.called or worker.terminate.called)
        self.assertTrue(worker.wait.called or worker.communicate.called)

    @unittest.expectedFailure
    def test_reused_prefix_excludes_pages_from_previous_call(self):
        def launch(args, **kwargs):
            prefix = Path(args[-1])
            for page in range(1, int(args[args.index("-l") + 1]) + 1):
                Path(f"{prefix}-{page}.ppm").touch()
            worker = Mock(returncode=0)
            worker.communicate.return_value = b"", b""
            return worker

        self.launch.side_effect = launch
        with TemporaryDirectory() as directory:
            options = dict(output_folder=directory, output_file="report", paths_only=True)
            first = api.convert_from_path("input.pdf", **options)
            self.assertEqual(len(first), 2)
            second = api.convert_from_path("input.pdf", last_page=1, **options)
            self.assertEqual(len(second), 1)


class WrapperContractTests(unittest.TestCase):
    def test_wrappers_preserve_options_and_forward_values(self):
        for wrapper, target in (
            (api.convert_from_bytes, api.convert_from_path),
            (api.pdfinfo_from_bytes, api.pdfinfo_from_path),
        ):
            with self.subTest(wrapper=wrapper.__name__):
                options = list(signature(wrapper).parameters.values())[1:]
                path_options = list(signature(target).parameters.values())[1:]
                self.assertEqual([p.name for p in options], [p.name for p in path_options])
                for left, right in zip(options, path_options):
                    self.assertEqual(left.kind, right.kind)
                    if left.name == "output_file":
                        # Each entry point owns its own default UUID generator.
                        self.assertEqual(type(left.default), type(right.default))
                    else:
                        self.assertEqual(left.default, right.default)
                values = {p.name: getattr(sentinel, p.name) for p in options}

                def check_input(path, **kwargs):
                    self.assertEqual(Path(path).read_bytes(), b"pdf input")
                    self.assertEqual(kwargs, values)
                    return sentinel.result

                with patch.object(api, target.__name__, side_effect=check_input):
                    self.assertIs(wrapper(b"pdf input", **values), sentinel.result)
