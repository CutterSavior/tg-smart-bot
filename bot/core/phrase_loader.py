import re
from pathlib import Path
from typing import Dict, List
from bot.core.config import SETTINGS

class PhraseRow(BaseModel):
    text: str
    category: str
    shortcut: str = ""
    phrase_type: str = "general"

class PhraseLoader:
    def __init__(self, path: Path = SETTINGS.phrases_path):
        self.path = path

    def load(self) -> Dict[str, PhraseRow]:
        lines = self._read_lines()
        data = {}
        for idx, line in enumerate(lines, 1):
            if not self._is_valid_line(line):
                continue
            cat, text = self._parse_line(line)
            if not text or len(text) < 4:
                continue
            data[f"line_{idx}"] = PhraseRow(
                text=text, category=cat, phrase_type=self._classify(text)
            )
        return data

    def _read_lines(self) -> List[str]:
        for enc in SETTINGS.encodings:
            try:
                return self.path.read_text(encoding=enc).splitlines()
            except Exception:
                continue
        raise RuntimeError(f"無法讀取 {self.path}，請檢查編碼")

    def _is_valid_line(self, line: str) -> bool:
        line = line.strip()
        if not line or line.startswith(("#", ";", "[")):
            return False
        return "=" in line and re.match(r"^[A-Z]{2}\d+,\d+=", line)

    def _parse_line(self, line: str):
        left, right = line.split("=", 1)
        return left.strip(), right.strip()

    def _classify(self, text: str) -> str:
        # 把原本 _classify_phrase 邏輯搬進來
        t = text.lower()
        if "請提供" in t or "麻煩提供" in t:
            if "截圖" in t and "帳號" in t:
                return "request_full_info"
            if "截圖" in t or "帳號" in t:
                return "request_missing_info"
        if any(k in t for k in ["正在處理", "核實中", "查詢中"]):
            return "processing_reply"
        if any(k in t for k in ["分鐘", "自動到帳", "稍後"]):
            return "wait_time_reply"
        return "general"