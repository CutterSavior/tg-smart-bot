from pathlib import Path
from pydantic import BaseSettings, Field, validator
from typing import List, Dict, Any
import yaml

class IntentRule(BaseModel):
    keywords: List[str]
    required: List[str]
    wait_minutes: int = 0

class SimilarityConfig(BaseModel):
    keyword_weight: float = 0.5
    front_match_weight: float = 0.2
    length_weight: float = 0.1
    sequence_weight: float = 0.05
    base_string_weight: float = 0.15

class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    superusers: List[int] = []
    phrases_path: Path = Path("phrases.ini")
    encodings: List[str] = ["utf-8-sig", "gbk", "gb2312"]
    min_similarity: float = 0.18
    intents: Dict[str, IntentRule]
    similarity: SimilarityConfig

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("intents", pre=True)
    def load_intents(cls, v):
        return {k: IntentRule(**r) for k, r in v.items()}

SETTINGS = Settings.parse_file("settings.yaml")