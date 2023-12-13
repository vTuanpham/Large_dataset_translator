import sys
sys.path.insert(0,r'./')
from typing import List, Dict
from .config import Config
from dataclasses import dataclass, asdict, fields


@dataclass
class DialogsConfig(Config):
    """
    A single training/test example for conversation config.
    """
    system_prompt: str

    user_prompts: list

    agent_responses: list = None

    answer_lengths: List[int] = None
    prompt_lengths: List[int] = None

    def __post_init__(self) -> None:
        # Post validate
        self.prompt_lengths = [len(prompt) for prompt in self.user_prompts]
        self.answer_lengths = [len(answer) for answer in self.agent_responses]

    @staticmethod
    def intersect_lists(list1, list2):
        intersected = []
        min_length = min(len(list1), len(list2))

        for i in range(min_length):
            intersected.append(list1[i])
            intersected.append(list2[i])

        # Add remaining elements if any list is longer
        if len(list1) > len(list2):
            intersected.extend(list1[min_length:])
        elif len(list2) > len(list1):
            intersected.extend(list2[min_length:])

        return intersected

    @property
    def __repr__(self) -> str:
        s = ""
        s += f"\n Question id: {self.qas_id}"
        s += f"\n System prompt: {self.system_prompt}"
        s += f"\n Dialogs: \n"

        if self.user_prompts and self.agent_responses:
            final_dialogs = self.intersect_lists(self.user_prompts, self.agent_responses)
            final_dialogs_length = self.intersect_lists(self.prompt_lengths, self.answer_lengths)
            for idx, (dialog, length) in enumerate(zip(final_dialogs, final_dialogs_length)):
                s += f"Dialog {idx}: {dialog} \n"
                s += f"Dialog {idx} length: {length}\n"

        return s

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [v.name for v in all_fields]


if __name__ == "__main__":
    example_dialog = {"qas_id": 10,
     "system_prompt": "You are an AI assistant, help as much as you can",
     "user_prompts": ["Tell me a bit about AI", "How does AI learn"],
     "agent_responses": ["Artificial Intelligence (AI) is a broad field focusing on creating systems or machines that can perform tasks that typically require human intelligence. It encompasses various subfields like machine learning, natural language processing, computer vision, robotics, and more. AI aims to simulate human cognitive functions, such as learning, problem-solving, perception, reasoning, and decision-making.",
                         '''AI learning primarily occurs through machine learning algorithms. There are a few key ways in which AI learns:

Supervised Learning: This method involves training AI models on labeled data. The algorithm learns patterns and associations between input data and corresponding output labels. For instance, in image recognition, showing the AI images labeled as "cat" or "dog" helps it learn to differentiate between the two.

Unsupervised Learning: Here, the AI learns from data without labeled outcomes. It looks for patterns, structures, or relationships within the data. Clustering algorithms, for example, can group similar data points together without prior labeling.

Reinforcement Learning: This method involves the AI learning through trial and error by interacting with an environment. It receives feedback in the form of rewards or penalties based on its actions. The AI's goal is to maximize cumulative reward, learning optimal strategies by exploring different actions.

Transfer Learning: This technique involves transferring knowledge learned from one task to another. Models pre-trained on vast amounts of data for one task can be fine-tuned or adapted to perform related tasks more effectively with smaller datasets.

AI learns by adjusting internal parameters or features in its algorithms to minimize errors or differences between predicted and actual outputs. This adjustment process, often referred to as "training," involves feeding the AI large amounts of data, iterating through algorithms, and refining the model's predictions or actions over time.

As AI continues to evolve, researchers are exploring new learning methodologies to enhance its capabilities, making it more adaptable, efficient, and capable of handling complex tasks across various domains.'''],
    }
    dialog_config_data = DialogsConfig(**example_dialog)
    print(dialog_config_data)


