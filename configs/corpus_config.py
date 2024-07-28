import sys
sys.path.insert(0,r'./')
from .config import Config
from typing import List, Dict
from dataclasses import dataclass, asdict, fields


@dataclass
class CorpusConfig(Config):

    orig_corpus_texts: str = None
    corpus_lengths: int = None

    def __post_init__(self) -> None:
        # Post validate
        self.corpus_lengths = len(self.orig_corpus_texts) if self.orig_corpus_texts is not None else None

    @property
    def __repr__(self) -> str:
        s = ""
        s += f"\n Text id: {self.qas_id}"
        if self.orig_corpus_texts:
            s += f"\n Text: {self.orig_corpus_texts}"
            s += f"\n Length: {self.corpus_lengths}"

        return s

    @property
    def get_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> List[str]:
        all_fields = fields(cls)
        return [v.name for v in all_fields]
