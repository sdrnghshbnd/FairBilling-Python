import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class FileParser:

    @staticmethod
    def validate_filepath(filename):
        try:
            Path(filename)
            return True
        except ValueError:
            return False

    @staticmethod
    def does_file_exist(filename):
        path = Path(filename)
        return path.exists() and path.is_file()

    @staticmethod
    def validate_record(record):
        # "HH:MM:SS USERNAME ACTION"
        pattern = re.compile(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d) \w+ (Start|End)")
        return bool(pattern.match(record))

    @staticmethod
    def find_latest_time(file_path):
        with file_path.open('rb') as file:
            file.seek(0, 2)  # Move the pointer to the end of the file
            buffer = bytearray()
            end_of_file = file.tell()

            while file.tell() > 0:
                file.seek(file.tell() - 1)
                char = file.read(1)
                if char == b'\n':
                    if buffer:
                        # We have a full line, reverse and decode it
                        line = buffer[::-1].decode('utf-8')
                        if FileParser.validate_record(line):
                            time_str = line.split()[0]
                            return datetime.strptime(time_str, "%H:%M:%S")
                        buffer.clear()
                else:
                    buffer.append(char[0])

                # Move one step back if not at start
                if file.tell() <= end_of_file:
                    file.seek(file.tell() - 1)

            # If the file ends without a newline at the end
            if buffer:
                line = buffer[::-1].decode('utf-8')
                if FileParser.validate_record(line):
                    time_str = line.split()[0]
                    return datetime.strptime(time_str, "%H:%M:%S")

        return None

    @staticmethod
    def data_results_calculator(file_path):
        unmatched_starts = defaultdict(int)
        session_counter = defaultdict(int)
        total_session_seconds = defaultdict(int)

        latest_time = FileParser.find_latest_time(file_path)

        if latest_time is None:
            return {}

        earliest_time = None

        with file_path.open('r') as file:
            for line in file:
                if not FileParser.validate_record(line):
                    continue

                time_str, username, action = line.split()
                event_time = datetime.strptime(time_str, "%H:%M:%S")

                if earliest_time is None:
                    earliest_time = event_time

                if action == "Start":
                    unmatched_starts[username] += 1
                    session_counter[username] += 1
                    total_session_seconds[username] += int((latest_time - event_time).total_seconds())

                elif action == "End":
                    if unmatched_starts[username] > 0:
                        unmatched_starts[username] -= 1
                        total_session_seconds[username] -= int((latest_time - event_time).total_seconds())
                    else:
                        session_counter[username] += 1
                        total_session_seconds[username] += int((event_time - earliest_time).total_seconds())

        # Combine results into a dictionary
        results = {
            username: (session_counter[username], total_session_seconds[username])
            for username in session_counter.keys()
        }

        return results

    @staticmethod
    def output_results(results):
        for username, (session_count, total_time) in results.items():
            print(f"{username} {session_count} {total_time}")
