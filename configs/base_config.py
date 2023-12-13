import sys
sys.path.insert(0,r'./')
from .config import Config
from typing import List, Dict
from dataclasses import dataclass, asdict, fields


@dataclass
class BaseConfig(Config):
    """
    A single training/test example for base config.
    """
    system_prompt: str

    question_text: str

    orig_answer_texts: str = None
    answer_lengths: int = None

    def __post_init__(self) -> None:
        # Post validate
        self.answer_lengths = len(self.orig_answer_texts) if self.orig_answer_texts is not None else None

    @property
    def __repr__(self) -> str:
        s = ""
        s += f"\n Question id: {self.qas_id}"
        s += f"\n System prompt: {self.system_prompt}"
        s += f"\n Question: {self.question_text}"
        if self.orig_answer_texts:
            s += f"\n Answer text: {self.orig_answer_texts}"
            s += f"\n Answer length: {self.answer_lengths}"

        return s

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [v.name for v in all_fields]

    def get_example(self,
                    inputs_column: str="prompt",
                    targets_column: str="target",
                    system_prefix: str="@@@@@@@@@@@@@ System prompt:",
                    question_prefix: str="####### Instruction:",
                    response_prefix: str="%%%%%%% Response:",
                    is_training: bool=True,
                    do_perplexity_eval: bool=False,
                    do_generative_eval: bool=False,
                    task_type: str=None,
                    ) -> Dict:
        assert task_type, "Please specified the task type inorder to get the example"

        system_msg = ' ' + system_prefix + '\n' + self.system_prompt + "\n\n"
        question_msg = question_prefix + '\n' + self.question_text + "\n\n"
        prompt = system_msg + ' ' + question_msg
        label = self.orig_answer_texts + "\n"

        if task_type == "SEQ_2_SEQ_LM":
            return {inputs_column: prompt,
                    targets_column: label}
        elif task_type == "CAUSAL_LM":
            if is_training:
                return {inputs_column: prompt + ' ' + response_prefix + '\n' + label}

            example_dict = {}
            # The perplexity field is for perplexity evaluation, which needed the full prompt and label
            # while the inputs_column only have prompt and response_prefix for model.generate evaluation
            if do_generative_eval:
                example_dict[inputs_column] = prompt + ' ' + response_prefix + '\n'
                example_dict[targets_column] = label

            if do_perplexity_eval:
                example_dict["perplexity"] = prompt + ' ' + response_prefix + '\n' + label

            if not bool(example_dict):
                raise "Evaluation files is provided but don't know what to do with them..."

            return example_dict
        else:
            raise f"This task type {task_type} is not support"


if __name__ == "__main__":
    python_question_contexts = [
        "To comment a single line in Python, you use the '#' symbol. Anything after the '#' on the same line is considered a comment and is ignored by the Python interpreter.",
        "Python 2 and Python 3 are two different versions of the Python programming language. Python 3 introduced several backward-incompatible changes to the language to improve its design and fix inconsistencies.",
        "To generate a random number in Python, you can use the 'random' module. Import the module and then use functions like 'random.random()' or 'random.randint()' depending on your requirements.",
        "The 'if __name__ == '__main__':' statement is used to determine whether the Python script is being run as the main program or if it is being imported as a module into another program.",
        "To open and read a file in Python, you can use the 'open()' built-in function in combination with various file modes. After reading, close the file using the 'close()' method of the file object.",
        "The 'range()' function generates a sequence of numbers in Python. It can be used in 'for' loops or to create lists of numbers within a specified range.",
        "Decorators in Python are a powerful way to modify or extend the behavior of functions or methods without changing their actual code. They use the '@' symbol and can be used to add functionality like logging, caching, etc.",
        "Exception handling in Python is done using 'try', 'except', 'else', and 'finally' blocks. It allows you to gracefully handle errors and exceptions that may occur during program execution.",
        "Lists and tuples are both used to store collections of items in Python, but lists are mutable (can be changed), whereas tuples are immutable (cannot be changed).",
        "A virtual environment in Python is a self-contained directory that contains its own Python interpreter and installed packages. It allows you to work on different projects with different dependencies without conflicts.",
        "To remove duplicates from a list in Python, you can convert it to a 'set' and then back to a 'list', as sets automatically remove duplicate elements.",
        "In Python lists, 'append()' adds an element to the end of the list, 'extend()' appends elements from another iterable, and 'insert()' inserts an element at a specified index.",
        "To iterate over a dictionary in Python, you can use a 'for' loop, which by default, iterates over the keys. You can also use the 'items()' method to loop over both keys and values.",
        "A lambda function in Python is a small anonymous function defined using the 'lambda' keyword. It can have any number of arguments but can only have one expression.",
        "You can find the length of a string in Python using the built-in 'len()' function, which returns the number of characters in the string.",
        "The 'pass' statement in Python is a null operation; it does nothing. It is used as a placeholder where syntactically some code is required, but you want to skip its execution.",
        "In Python, you create a class using the 'class' keyword, and you define methods (functions within the class) to perform actions or return information about the object.",
        "Shallow copy creates a new object, but it references the same elements as the original object. Deep copy creates a completely independent copy of the object and its elements.",
        "To sort a dictionary by its values in Python, you can use the 'sorted()' function with a lambda function as the 'key' argument or utilize the 'collections' module.",
        "The 'zip()' function in Python is used to combine multiple iterables into a single iterable of tuples. Each tuple contains elements from corresponding positions in the input iterables."
    ]

    # print(AdvanceQAExample.straighten_docs(python_question_contexts))

    example8 = BaseConfig(qas_id="8", question_text="What do cats eat?",
                                    orig_answer_texts="meat and fish", system_prompt="Hi")

    # print(example8)
    print(example8.get_example(is_training=True, task_type="CAUSAL_LM"))
    # print(example8.get_dict)

    example6 = BaseConfig(qas_id="6", question_text="What is the meaning of existence?",
                                     orig_answer_texts="Dying", system_prompt="Hello")
    # print(example6)
    print(example6.get_example(is_training=True, task_type="SEQ_2_SEQ_LM"))
    # print(example6.get_dict)
    # print(example6.get_dict_str)
    # print(example6.get_keys())