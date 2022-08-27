from psd2pngs import convert
from unittest import TestCase


class TestConvert(TestCase):
    def test_convert(self):
        convert(
            r"tests/cc0-psds/1.psd",
            use_json_camel_case=True,
            out_dir_path="tests/.test_results"
        )
