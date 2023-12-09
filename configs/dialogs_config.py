import sys
sys.path.insert(0,r'./')
import pprint
from typing import List, Dict
from dataclasses import dataclass, asdict, fields


@dataclass
class DialogsConfig:
    """
    A single training/test example for conversation config.
    """
    qas_id: str
    system_prompt: str

    user_prompts: list

    agent_responses: list = None

    answer_lengths: List[int] = None
    prompt_lengths: List[int] = None

    def __post_init__(self) -> None:
        # Post validate
        self.answer_lengths = [len(answer) for answer in self.answers_list]
        self.prompt_lengths = [len(prompt) for prompt in self.user_prompts]

    def __str__(self) -> str:
        return self.__repr__

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

    @staticmethod
    def get_keys() -> List[str]:
        all_fields = fields(DialogsConfig)
        return [v.name for v in all_fields]

    @property
    def get_dict_str(self, indent: int=4) -> None:
        pp = pprint.PrettyPrinter(indent=indent)
        pp.pprint(self.get_dict)



