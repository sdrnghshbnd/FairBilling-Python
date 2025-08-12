from datetime import datetime
from pathlib import Path

from processor.record_validator import RecordValidator


class LogFileReader:
    def __init__(self, file_path: Path, validator: RecordValidator):
        self.file_path = file_path
        self.validator = validator

    def find_latest_time(self) -> datetime | None:
        with self.file_path.open('rb') as file:
            file.seek(0, 2)  # End of file
            buffer = bytearray()
            end_of_file = file.tell()

            while file.tell() > 0:
                file.seek(file.tell() - 1)
                char = file.read(1)
                if char == b'\n':
                    if buffer:
                        line = buffer[::-1].decode('utf-8')
                        if self.validator.is_valid_record(line):
                            time_str = line.split()[0]
                            return datetime.strptime(time_str, "%H:%M:%S")
                        buffer.clear()
                else:
                    buffer.append(char[0])

                if file.tell() <= end_of_file:
                    file.seek(file.tell() - 1)

            # Check for file without trailing newline
            if buffer:
                line = buffer[::-1].decode('utf-8')
                if self.validator.is_valid_record(line):
                    time_str = line.split()[0]
                    return datetime.strptime(time_str, "%H:%M:%S")

        return None

    def read_lines(self):
        with self.file_path.open('r') as file:
            for line in file:
                yield line.strip()
