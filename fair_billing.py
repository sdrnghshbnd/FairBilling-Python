import argparse
from pathlib import Path
from processor.file_parser import FileParser

def main():
    parser = argparse.ArgumentParser(description="Process a log file.")
    parser.add_argument("log_file_path", type=str, help="Path to the log file")
    args = parser.parse_args()

    log_file_path = Path(args.log_file_path)

    if not FileParser.validate_filepath(log_file_path):
        print("Invalid file path.")
        return

    if not FileParser.does_file_exist(log_file_path):
        print("File does not exist.")
        return

    results = FileParser.data_results_calculator(log_file_path)
    FileParser.output_results(results)

if __name__ == "__main__":
    main()