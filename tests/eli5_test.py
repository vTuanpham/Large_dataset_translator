import os
import unittest
import warnings
from examples.ELI5.ELI5_10docs_Parser import ELI5Val


class TestELI5Val(unittest.TestCase):

    def step1(self):
        self.file_path = "examples/ELI5/ELI5_val_10_doc.json"
        self.output_dir = "examples/ELI5"
        self.parser = ELI5Val(self.file_path, self.output_dir, target_lang="de",
                              max_example_per_thread=100, large_chunks_threshold=800)

    def step2(self):
        self.parser.read()
        self.assertIsNotNone(self.parser.data_read)  # Check that data_read is not None

    def step3(self):
        self.parser.convert()
        self.assertIsNotNone(self.parser.converted_data)  # Check that converted_data is not None

    def step4(self):
        self.parser.save

        self.output_path = os.path.join(self.output_dir, "ELI5_val_translated_de.json")

        self.assertTrue(os.path.exists(self.output_path), f"File '{self.output_path}' does not exist")

    def step5(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

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


if __name__ == '__main__':
    unittest.main()





