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
    Python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Running the Application

To run the application and process a log file, use the following command:

```bash
Python fair_billing.py /path/to/your/logfile.txt
```

## Fair Billing - Assumptions and Discussion Points

### Dojo Session (11/09/2024)

During the Dojo session, several discussion points were raised to improve the system for a real-world, scalable implementation:

1. Assumed input file time is UTC time - in real system UTC plus TimeZone/locale to handle daylight saving/time changes/midnight crossover
so not charge double or less depending 

2. Assumed file is not replaced mid processing.

3. If the power/ or issue whereby process is killed, to resume without reprocessing, would require state hard stored so we could resume.
Tracking Processiing e.g. Line we are processing, RecordProcessingStatus: Started/In Progress/Completed, save to a permanent store ACID, transaction commit confirmation.
 
4. In a real system file size could large gigabytes-> paging, pageSize configuration parameter, load N lines from file at a time.

5. Concurrency, in a real system possible multiple processes/multi-thread processing of other session files, so complete result calculation sum of sub output to a specifc time period.

6. Use a hash/UUID for uniquely identifying a user, could potentially be better since name of user is of arbitary length, as longer hash is optimal length (less than typical user name length).
UUID 36 char a bit long, use hash which is human readable, easier debugging.

