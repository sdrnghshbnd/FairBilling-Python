import argparse
from pathlib import Path
from processor.path_validator import PathValidator
from processor.record_validator import RecordValidator
from processor.log_file_reader import LogFileReader
from processor.session_calculator import SessionCalculator
from processor.results_outputter import ResultsOutputter

def main():
    parser = argparse.ArgumentParser(description="Process a log file and calculate user sessions.")
    parser.add_argument('logfile', type=str, help="Path to the log file to process")
    args = parser.parse_args()

    log_file_path = Path(args.logfile)

    if not PathValidator.validate_filepath(log_file_path):
        print("Invalid file path.")
        return

    if not PathValidator.does_file_exist(log_file_path):
        print("File does not exist.")
        return

    validator = RecordValidator()
    reader = LogFileReader(log_file_path, validator)
    latest_time = reader.find_latest_time()

    if latest_time is None:
        print("No valid records found in the log file.")
        return

    calculator = SessionCalculator(validator, latest_time)
    for line in reader.read_lines():
        calculator.process_line(line)

    results = calculator.get_results()
    ResultsOutputter.output(results)


if __name__ == "__main__":
    main()