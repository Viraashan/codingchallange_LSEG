# User Creation Script

## Overview

This script, developed by Virashan Athukorala, automates the process of creating users by reading data from a CSV file and sending HTTP POST requests to an API endpoint. It includes logging, error handling, and a retry mechanism to ensure reliability.

## Features

- Reads user data from a CSV file.
- Sends HTTP POST requests to create users.
- Implements a retry mechanism for failed requests.
- Logs errors and invalid data entries.
- Validates CSV structure and email format.

## Requirements

- Python 3
- `requests` module

### Install Dependencies
```sh
pip install requests
```

## Usage

1. Prepare a CSV file (`users.csv`) with the following headers:
   ```
   name,email,role
   ```
2. Place the CSV file in the same directory as the script.
3. Run the script:
   ```sh
   python userCreate.py
   ```

## Configuration

- Modify the API endpoint in `send_user_creation_request()` to match your actual API.
- Ensure the CSV file format is correct to avoid errors.

## Error Handling

- Logs errors in `error_log.txt`.
- Skips invalid rows with missing or incorrectly formatted data.

## Future Enhancements

- Add unit tests for validation and API requests.
- Improve logging with detailed execution timestamps.
- Externalize configurations via environment variables.

---

Developed by **Virashan Athukorala**
