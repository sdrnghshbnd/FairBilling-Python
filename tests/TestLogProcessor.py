import os
import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
from processor.file_parser import FileParser
from datetime import datetime


class TestLogProcessor(unittest.TestCase):
    def test_validate_filepath(self):
        valid_path = "/valid/path/log.txt"
        invalid_path = "hjcg--asdasd!!SACCSDVAGGF!!---"
        self.assertTrue(FileParser.validate_filepath(valid_path))
        self.assertTrue(FileParser.validate_filepath(invalid_path))

    def test_does_file_exist(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'sample_logs', 'log.txt')

        existing_file = file_path
        non_existing_file = "/nonexistent/path/log.txt"

        self.assertTrue(FileParser.does_file_exist(existing_file))
        self.assertFalse(FileParser.does_file_exist(non_existing_file))

    def test_validate_record_valid(self):
        valid_record = "14:02:03 ALICE99 Start"
        result = FileParser.validate_record(valid_record)
        self.assertTrue(result)

    def test_validate_record_invalid_time(self):
        invalid_record = "25:63:72 ALICE99 Start"  # Invalid time
        result = FileParser.validate_record(invalid_record)
        self.assertFalse(result)

    def test_validate_record_invalid_format(self):
        invalid_record = "14:02:03ALICE99Start"  # Missing spaces
        result = FileParser.validate_record(invalid_record)
        self.assertFalse(result)

    def test_validate_record_invalid_action(self):
        invalid_record = "14:02:03 ALICE99 Jump"  # Invalid action
        result = FileParser.validate_record(invalid_record)
        self.assertFalse(result)

    @patch("processor.file_parser.FileParser.find_latest_time")
    @patch("pathlib.Path.open", new_callable=mock_open, read_data="")
    def test_data_results_calculator_empty_file(self, mock_open, mock_find_latest_time):
        mock_find_latest_time.return_value = None  # Simulate empty file by returning None
        result = FileParser.data_results_calculator(Path("dummy/path/to/empty_log.txt"))
        self.assertEqual(result, {})

    @patch("processor.file_parser.FileParser.find_latest_time")
    @patch("pathlib.Path.open", new_callable=mock_open, read_data="14:02:03 ALICE99 Start\n14:02:34 ALICE99 End\n")
    def test_data_results_calculator_single_user_mocked(self, mock_open, mock_find_latest_time):
        mock_find_latest_time.return_value = datetime.strptime("14:02:34", "%H:%M:%S")
        result = FileParser.data_results_calculator(Path("dummy/path/to/log.txt"))
        expected_result = {"ALICE99": (1, 31)}
        self.assertEqual(result, expected_result)

    @patch("processor.file_parser.FileParser.find_latest_time")
    @patch("pathlib.Path.open", new_callable=mock_open,
           read_data="14:02:03 ALICE99 Start\n14:02:34 ALICE99 End\n14:02:58 CHARLIE Start\n14:03:02 CHARLIE End\n")
    def test_data_results_calculator_multiple_users_mocked(self, mock_open, mock_find_latest_time):
        mock_find_latest_time.return_value = datetime.strptime("14:03:02", "%H:%M:%S")
        result = FileParser.data_results_calculator(Path("dummy/path/to/log.txt"))
        expected_result = {"ALICE99": (1, 31), "CHARLIE": (1, 4)}
        self.assertEqual(result, expected_result)

    def test_data_results_calculator_real_file(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'sample_logs', 'log.txt')
        result = FileParser.data_results_calculator(
            Path(file_path))
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
            FileParser.output_results(results)
            mocked_print.assert_any_call("ALICE99 1 31")
            mocked_print.assert_any_call("CHARLIE 1 4")


if __name__ == "__main__":
    unittest.main()
