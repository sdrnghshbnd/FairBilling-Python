# Fair Billing

## Overview

Fair Billing is a Python project that processes log files to calculate session times and counts. The project includes functionality to validate file paths, read log files, and output results.

## Project Structure

- `fair_billing.py`: Main script to run the application.
- `processor/file_parser.py`: Contains the `FileParser` class with methods for file processing and validation.
- `tests/TestLogProcessor.py`: Contains unit tests for `FileParser`.

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone the repository:

    ```bash
    git clone https://your-repository-url.git
    cd your-repository-folder
    ```

2. (Optional) Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the application and process a log file, use the following command:

```bash
python fair_billing.py /path/to/your/logfile.txt
