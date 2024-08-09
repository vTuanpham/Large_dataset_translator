import os
import unittest
import warnings
import sys
sys.path.insert(0,r'./')

from datasets import load_dataset

from providers import MultipleProviders
from examples.ELI5.ELI5_10docs_Parser import ELI5Val


class TestELI5Val(unittest.TestCase):

    def step1(self):
        self.file_path = "examples/ELI5/ELI5_val_10_doc.json"
        self.output_dir = "examples/ELI5"
        self.parser = ELI5Val(self.file_path, self.output_dir, target_lang="vie",
                              max_example_per_thread=50, large_chunks_threshold=500,
                              translator=MultipleProviders)

    def step2(self):
        self.parser.read()
        self.assertIsNotNone(self.parser.data_read)  # Check that data_read is not None

    def step3(self):
        self.parser.convert()
        self.assertIsNotNone(self.parser.converted_data)  # Check that converted_data is not None

    def step4(self):
        self.parser.save

        self.output_path = os.path.join(self.output_dir, "ELI5_val.json")
        self.output_path_translated = os.path.join(self.output_dir, "ELI5_val_translated_vie.json")

        self.assertTrue(os.path.exists(self.output_path), f"File '{self.output_path}' does not exist")
        self.assertTrue(os.path.exists(self.output_path_translated), f"File '{self.output_path_translated}' does not exist")

    def step5(self):
        try:
            self.parsed_dataset = load_dataset("json", data_files=self.output_path, keep_in_memory=False)
            self.translated_dataset = load_dataset("json", data_files=self.output_path_translated, keep_in_memory=False)
        except Exception as e:
            raise SyntaxError("Invalid syntax for save function, the data output must be in the form of"
                              f"line-delimited json,\n Error message: {e}")

    def step6(self):
        self.assertEqual(len(self.parsed_dataset['train']), len(self.parser.converted_data),
                         msg="The parsed dataset does not match the length of the parsed dataset")
        self.assertAlmostEqualInt(len(self.translated_dataset['train']), len(self.parser.converted_data),
                                  msg="The parsed translated dataset fail too much and does not meet the length criteria of the parsed dataset",
                                  tolerance=1507)

    def step7(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists(self.output_path_translated):
            os.remove(self.output_path_translated)

    def _steps(self):
        for name in dir(self):  # dir() result is implicitly sorted
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail(f"{step} failed ({type(e)}: {e})")

    def assertAlmostEqualInt(self, int1, int2, tolerance=1, msg=None):
        """
        Asserts that two integers are almost equal within a specified tolerance range.
        """
        if abs(int1 - int2) > tolerance:
            standard_msg = f"{int1} and {int2} are not almost equal within a tolerance of {tolerance}."
            if msg:
                standard_msg = f"{msg}: {standard_msg}"
            raise self.failureException(standard_msg)


if __name__ == '__main__':
    unittest.main()




