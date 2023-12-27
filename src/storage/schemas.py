from datetime import datetime

from src.models import CustomModel
from src.storage.constants import MemeType


# minimal data to send a meme
class MemeData(CustomModel):
    meme_id: int
    meme_type: MemeType
    file_id: str
    caption: str | None
