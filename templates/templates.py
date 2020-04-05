from enum import Enum
from pathlib import Path

CURRENT_DIR = Path(__file__)


class Templates(Enum):
    participants = CURRENT_DIR.parent.absolute() / "participants.tsv"
    dataset = CURRENT_DIR.parent.absolute() / "dataset_description.json"
