import sys

sys.path.insert(0, r"./")
from typing import List, Dict
from .config import Config
from dataclasses import dataclass, asdict, fields


@dataclass
class KTOConfig(Config):
    """
    A single training/test example for KTO config, compatible with trl library.
    """

    system_prompt: str

    conversation_history: list
    conversation_roles: list

    agent_prompt_completion: str

    label: bool

    @staticmethod
    def construct_kto_example(
        conversation_history: list,
        conversation_roles: list,
        agent_prompt_completion: str,
        label: bool,
        system_prompt: str = None,
    ) -> Dict:
        prompt = []
        if system_prompt:
            prompt.append({"content": system_prompt, "role": "system"})
        for role, dialog in zip(conversation_roles, conversation_history):
            prompt.append({"content": dialog, "role": role})

        return {
            "conversation_history": prompt,
            "agent_prompt_completion": [
                {"content": agent_prompt_completion, "role": "assistant"}
            ],
            "conversation_roles": conversation_roles,
            "label": label,
            "system_prompt": system_prompt,
        }

    @property
    def __repr__(self) -> str:
        s = ""
        s += f"\n Data id: {self.qas_id}"
        s += f"\n System prompt: {self.system_prompt}"
        s += f"\n conversation_history: \n"

        for role, dialog in zip(self.conversation_roles, self.conversation_history):
            s += f"\n Role: {role} \n Dialog: {dialog}"
        s += f"\n Agent prompt completion: {self.agent_prompt_completion}"
        s += f"\n Label: {self.label}"

        return s

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [v.name for v in all_fields]


if __name__ == "__main__":
    kto_config = KTOConfig(
        qas_id="1",
        system_prompt="Hello",
        conversation_history=["Hi", "How are you?"],
        conversation_roles=["user", "assistant"],
        agent_prompt_completion="I am fine",
        label=True,
    )

    print(kto_config)
    print(kto_config.get_dict)
    print(kto_config.get_keys())

    kto_config = KTOConfig.construct_kto_example(
        system_prompt="Hello",
        conversation_history=["Hi", "How are you?"],
        conversation_roles=["user", "assistant"],
        agent_prompt_completion="I am fine",
        label=True,
    )

    print(kto_config)
