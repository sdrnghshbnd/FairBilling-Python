import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch
from pathlib import Path
from datetime import datetime

from processor.path_validator import PathValidator
from processor.record_validator import RecordValidator
from processor.session_calculator import SessionCalculator
from processor.results_outputter import ResultsOutputter


class TestLogProcessor(unittest.TestCase):

    def test_validate_filepath(self):
        valid_path = Path("/valid/path/log.txt")
        invalid_path = Path("hjcg--asdasd!!SACCSDVAGGF!!---")
        self.assertTrue(PathValidator.validate_filepath(valid_path))
        self.assertTrue(PathValidator.validate_filepath(invalid_path))

    def test_does_file_exist(self):
        file_path = Path(__file__).parent.parent / "sample_logs" / "log.txt"
        existing_file = file_path
        non_existing_file = Path("/nonexistent/path/log.txt")

        self.assertTrue(PathValidator.does_file_exist(existing_file))
        self.assertFalse(PathValidator.does_file_exist(non_existing_file))

    def test_validate_record_valid(self):
        valid_record = "14:02:03 ALICE99 Start"
        result = RecordValidator.is_valid_record(valid_record)
        self.assertTrue(result)

    def test_validate_record_invalid_time(self):
        invalid_record = "25:63:72 ALICE99 Start"
        result = RecordValidator.is_valid_record(invalid_record)
        self.assertFalse(result)

    def test_validate_record_invalid_format(self):
        invalid_record = "14:02:03ALICE99Start"
        result = RecordValidator.is_valid_record(invalid_record)
        self.assertFalse(result)

    def test_validate_record_invalid_action(self):
        invalid_record = "14:02:03 ALICE99 Jump"
        result = RecordValidator.is_valid_record(invalid_record)
        self.assertFalse(result)

    def _run_session_calculator(self, log_data, latest_time_str):
        latest_time = datetime.strptime(latest_time_str, "%H:%M:%S")
        calc = SessionCalculator(RecordValidator, latest_time)
        for line in log_data.strip().splitlines():
            calc.process_line(line)
        return calc.get_results()

    def test_empty_file(self):
        result = self._run_session_calculator("", "14:00:00")
        self.assertEqual(result, {})

    def test_single_user(self):
        log_data = """14:02:03 ALICE99 Start
14:02:34 ALICE99 End"""
        result = self._run_session_calculator(log_data, "14:02:34")
        expected_result = {"ALICE99": (1, 31)}
        self.assertEqual(result, expected_result)

    def test_multiple_users(self):
        log_data = """14:02:03 ALICE99 Start
14:02:34 ALICE99 End
14:02:58 CHARLIE Start
14:03:02 CHARLIE End"""
        result = self._run_session_calculator(log_data, "14:03:02")
        expected_result = {"ALICE99": (1, 31), "CHARLIE": (1, 4)}
        self.assertEqual(result, expected_result)

    def test_real_file(self):
        file_path = Path(__file__).parent.parent / "sample_logs" / "log.txt"
        log_data = file_path.read_text()
        latest_time = max(
            datetime.strptime(line.split()[0], "%H:%M:%S")
            for line in log_data.splitlines()
            if RecordValidator.is_valid_record(line)
        )
        calc = SessionCalculator(RecordValidator, latest_time)
        for line in log_data.strip().splitlines():
            calc.process_line(line)
        result = calc.get_results()
        expected_result = {
            "ALICE99": (4, 270),
            "CHARLIE": (7, 104),
            "SADRA": (1, 30),
            "DAVID": (1, 140)
        }
        self.assertEqual(result, expected_result)

    def test_output_results(self):
        results = {"ALICE99": (1, 31), "CHARLIE": (1, 4)}
        with patch('builtins.print') as mocked_print:
            ResultsOutputter.output(results)
            mocked_print.assert_any_call("ALICE99 1 31")
            mocked_print.assert_any_call("CHARLIE 1 4")


if __name__ == "__main__":
    unittest.main()