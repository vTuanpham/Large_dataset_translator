import sys
sys.path.insert(0,r'./')
from .config import Config
from typing import List, Dict
from dataclasses import dataclass, asdict, fields


@dataclass
class QAConfig(Config):
    """
    A single training/test example for question answering config.
    """
    system_prompt: str

    question_text: str
    context_list: list

    answers_list: list = None
    answer_lengths: List[int] = None
    context_lengths: List[int] = None

    def __post_init__(self) -> None:
        # Post validate
        self.answer_lengths = [len(answer) for answer in self.answers_list]
        self.context_lengths = [len(context) for context in self.context_list]

    @property
    def __repr__(self) -> str:
        s = ""
        s += f"\n Question id: {self.qas_id}"
        s += f"\n System prompt: {self.system_prompt}"
        s += f"\n Question: {self.question_text}"
        if self.context_list:
            s += "\n Context list: \n"
            for context, length in zip(self.context_list, self.context_lengths):
                s += f"{context}\n"
                s += f"Context length: {length}\n\n"
        if self.answers_list:
            s += "\n Answer list: \n"
            for answer, length in zip(self.answers_list, self.answer_lengths):
                s += f"{answer}\n"
                s += f"Answer length: {length}\n\n"

        return s

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [v.name for v in all_fields]



