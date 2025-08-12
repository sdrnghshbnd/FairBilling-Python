import re

class RecordValidator:
    pattern = re.compile(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d) \w+ (Start|End)")

    @classmethod
    def is_valid_record(cls, record: str) -> bool:
        return bool(cls.pattern.match(record))
