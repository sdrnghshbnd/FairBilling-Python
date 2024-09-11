```
  ____       _ _   _     _       _______   _                                                _           _   _                 
 |  _ \     (_| | (_)   | |     |__   __| | |                                              (_)         | | (_)                
 | |_) |_ __ _| |_ _ ___| |__      | | ___| | ___  ___ ___  _ __ ___  _ __ ___  _   _ _ __  _  ___ __ _| |_ _  ___  _ __  ___ 
 |  _ <| '__| | __| / __| '_ \     | |/ _ | |/ _ \/ __/ _ \| '_ ` _ \| '_ ` _ \| | | | '_ \| |/ __/ _` | __| |/ _ \| '_ \/ __|
 | |_) | |  | | |_| \__ | | | |    | |  __| |  __| (_| (_) | | | | | | | | | | | |_| | | | | | (_| (_| | |_| | (_) | | | \__ \
 |____/|_|  |_|\__|_|___|_| |_|    |_|\___|_|\___|\___\____|_______|_|_| |_| |_|\__,_|_| |_|_|\___\__,_|\__|_|\___/|_| |_|___/ 



                                                         ____ _______ 
                                                        |  _ |__   __|
                                                        | |_) | | |   
                                                        |  _ <  | |   
                                                        | |_) | | |   
                                                        |____/  |_| 


```

# Fair Billing Application

## Overview
This Python application provides a summary of each user's total session time to have fair billing.

## Features
- Parses log file with user session start and end times
- Handles incomplete sessions (missing start or end times)
- Calculates and outputs session count and total session duration for each user

## Project Structure

- `fair_billing.py`: Main script to run the application.
- `processor/file_parser.py`: Contains the `FileParser` class with methods for file processing and validation.
- `tests/TestLogProcessor.py`: Contains unit tests for `FileParser`.

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sdrnghshbnd/FairBilling-Python.git
    cd FairBilling-Python.git
    ```

2. (Optional) Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Running the Application

To run the application and process a log file, use the following command:

```bash
Python fair_billing.py /path/to/your/logfile.txt
