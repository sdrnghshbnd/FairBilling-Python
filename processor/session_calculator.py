from collections import defaultdict
from datetime import datetime

from processor.record_validator import RecordValidator


class SessionCalculator:
    def __init__(self, validator: RecordValidator, latest_time: datetime):
        self.validator = validator
        self.latest_time = latest_time
        self.unmatched_starts = defaultdict(int)
        self.session_counter = defaultdict(int)
        self.total_session_seconds = defaultdict(int)
        self.earliest_time = None

    def process_line(self, line: str):
        if not self.validator.is_valid_record(line):
            return

        time_str, username, action = line.split()
        event_time = datetime.strptime(time_str, "%H:%M:%S")

        if self.earliest_time is None:
            self.earliest_time = event_time

        if action == "Start":
            self.unmatched_starts[username] += 1
            self.session_counter[username] += 1
            self.total_session_seconds[username] += int((self.latest_time - event_time).total_seconds())
        elif action == "End":
            if self.unmatched_starts[username] > 0:
                self.unmatched_starts[username] -= 1
                self.total_session_seconds[username] -= int((self.latest_time - event_time).total_seconds())
            else:
                self.session_counter[username] += 1
                self.total_session_seconds[username] += int((event_time - self.earliest_time).total_seconds())

    def get_results(self):
        return {
            user: (self.session_counter[user], self.total_session_seconds[user])
            for user in self.session_counter.keys()
        }
