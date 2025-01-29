import csv
import requests
import logging
import os

# Configure logging to write errors to a file
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_user_creation_request(user_data, retries=3):
    """
    Send a POST request to create a user with a retry mechanism.

    Args:
        user_data (dict): The user data to be sent in the request.
        retries (int): The number of retry attempts.

    Returns:
        bool: True if the user was created successfully, False otherwise.
    """
    for attempt in range(retries):
        try:
            response = requests.post("https://example.com/api/create_user", json=user_data)
            if response.status_code == 201:
                return True
            elif response.status_code == 409:
                logging.error(f"User already exists: {user_data.get('email', 'N/A')}")
                return False
            else:
                logging.error(f"Failed to create user {user_data.get('email', 'N/A')}: {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            logging.error(f"Request exception for user {user_data.get('email', 'N/A')} (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                continue
            return False

def is_valid_row(row):
    """
    Check if the row contains all required fields and validate the email format.

    Args:
        row (dict): The row data from the CSV file.

    Returns:
        bool: True if the row is valid, False otherwise.
    """
    required_fields = ["name", "email", "role"]
    if not all(row.get(field) for field in required_fields):
        return False
    if "@" not in row["email"] or "." not in row["email"]:
        logging.error(f"Invalid email format: {row['email']}")
        return False
    return True

def create_users(file_path):
    """
    Process the CSV file and create users.

    Args:
        file_path (str): The path to the CSV file.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, "r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Validate headers
            expected_headers = {"name", "email", "role"}
            if not expected_headers.issubset(reader.fieldnames):
                logging.error(f"Missing required headers in CSV. Found: {reader.fieldnames}")
                return

            for row_number, row in enumerate(reader, start=1):
                # Skip invalid rows
                if not is_valid_row(row):
                    logging.error(f"Skipping invalid row at line {row_number}: {row}")
                    continue

                # Attempt user creation
                if not send_user_creation_request(row):
                    logging.error(f"Failed to process row at line {row_number}: {row}")
    except csv.Error as e:
        logging.error(f"CSV parsing error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # File path to the CSV file
    file_path = "users.csv"
    create_users(file_path)

# Further Improvement Suggestions:
# 1. Configuration:
#    - Make the API endpoint configurable via a settings file or environment variables.
#    - Example: Use a config file (config.ini) or environment variables to store the API endpoint.
#
# 2. Unit Tests:
#    - Add unit tests to ensure the functions work as expected and handle edge cases correctly.
#    - Example: Use the unittest framework to create tests for each function.
#
# 3. Enhanced Logging:
#    - Add more detailed logging for debugging purposes, such as logging the start and end of the script execution.
#    - Example: Log the start and end of the create_users function with timestamps.
#
# 4. Error Handling:
#    - Implement more granular error handling for specific exceptions.
#    - Example: Handle specific exceptions like ConnectionError, Timeout, etc., separately.