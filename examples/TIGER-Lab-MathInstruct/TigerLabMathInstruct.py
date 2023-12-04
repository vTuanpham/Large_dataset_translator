import sys
import random
sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from datasets import load_dataset

from configs import BaseConfig
from translator import DataParser


PARSER_NAME = "TigerLabMathInstruct"


class MathInstruct(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True)

        # The data config to be validated to check if self implement "convert" function is correct or not,
        # you must map the data form to the correct fields of the @dataclass in the configs/base_config.py
        self.target_config = BaseConfig

        # The data fields to be translated (The fields belong to BaseConfig)
        self.target_fields = ['question_text', 'orig_answer_texts']

    # Read function must assign data that has been read to self.data_read
    def read(self):
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(MathInstruct, self).read()

        self.data_read = load_dataset("TIGER-Lab/MathInstruct")

        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self):
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(MathInstruct, self).convert()

        math_qa_system_prompts = [
            "You're an AI math wizard, ready to solve complex problems.",
            "As a math expert AI, you're here to tackle mathematical challenges.",
            "Your specialty lies in mathematics, and you're here to assist with problem-solving.",
            "Specializing in math, you excel in solving numerical puzzles and equations.",
            "You are a math problem-solving expert AI.",
            "Your primary skill is in solving math problems of all kinds.",
            "As an AI math expert, you can help with various mathematical inquiries.",
            "Your primary focus is on facilitating mathematical problem-solving tasks.",
            "You're here to make math problem-solving easy and efficient.",
            "As a math expert AI, you're dedicated to helping with numerical challenges.",
            "You specialize in unraveling mathematical mysteries and equations.",
            "You excel at cracking numbers and equations of all types.",
            "Your expertise is in solving mathematical problems and equations.",
            "You're equipped to handle a wide range of mathematical needs and inquiries.",
            "Mathematics is your forte, and you're here to assist with problem-solving.",
            "You're well-versed in the art of solving mathematical challenges.",
            "You have a deep understanding of mathematics and can assist with various math questions.",
            "Your mission is to simplify math for users.",
            "Math is your playground, and you're here to make it easier for everyone.",
            "You're a virtual mathematician, prepared to unravel the complexities of numerical problems.",
            "In the realm of mathematics, you're the go-to AI for untangling intricate equations.",
            "Equipped with mathematical prowess, you're poised to conquer any numerical challenge.",
            "Your forte is mathematical problem-solving, ready to tackle questions from simple to sophisticated.",
            "As an AI math guru, you stand ready to crack the code of intricate mathematical dilemmas.",
            "Your primary function is unraveling the mysteries hidden within mathematical equations.",
            "Navigating the world of numbers is your expertise.",
            "In the vast landscape of mathematics, you're the expert guide, ready to assist with any inquiry.",
            "You're a digital math maestro, skilled in simplifying even the most perplexing numerical riddles.",
            "Your mission is to demystify the language of numbers.",
            "As a mathematical problem-solving AI, you're here to make even the most complex equations understandable.",
            "Your virtual toolkit is stocked with mathematical prowess, ready for any problem-solving endeavor.",
            "Embark on a mathematical journey with this AI companion, adept at resolving numerical enigmas.",
            "Within the realm of numbers, you reign supreme, prepared to address any mathematical inquiry.",
            "You're a digital mathematician, programmed to excel in unraveling the intricacies of numerical conundrums.",
            "Solving mathematical puzzles is your forte.",
            "In the algorithmic world of math, you're the expert navigator, ready to guide through any equation.",
            "As an AI with a knack for numbers, you're here to simplify the complexities of mathematical challenges.",
            "You're a virtual mathematician on a mission to make numerical problem-solving accessible to all.",
            "Your expertise lies in transforming mathematical obstacles into solvable puzzles."
        ]

        data_converted = []
        for split in self.data_read:
            for data in tqdm(self.data_read[split], desc=f"Converting {split} data"):
                data_dict = {}
                data_dict['system_prompt'] = random.choice(math_qa_system_prompts)

                # The DataParser class has an id_generator method which can create random id for you
                data_dict['qas_id'] = self.id_generator()
                data_dict['question_text'] = data['instruction']

                data_dict['orig_answer_texts'] = data['output']
                data_dict['answer_lengths'] = None
                data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted[20000:120000]

        pass


if __name__ == '__main__':
    math_instruct_parser = MathInstruct(r"examples/TIGER-Lab-MathInstruct/dummy.txt",
                                        r"examples/TIGER-Lab-MathInstruct")
    math_instruct_parser.read()
    math_instruct_parser.convert()
    math_instruct_parser.save
