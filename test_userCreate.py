import unittest
from unittest.mock import patch, mock_open, MagicMock
import logging
import requests
import csv
import os

from userCreate import create_users, send_user_creation_request, is_valid_row
class TestUserCreation(unittest.TestCase):
    
    @patch("requests.post")
    def test_send_user_creation_request_success(self, mock_post):
        mock_post.return_value.status_code = 201
        user_data = {"name": "John Doe", "email": "john@example.com", "role": "admin"}
        self.assertTrue(send_user_creation_request(user_data))
    
    @patch("requests.post")
    def test_send_user_creation_request_user_exists(self, mock_post):
        mock_post.return_value.status_code = 409
        user_data = {"name": "Jane Doe", "email": "jane@example.com", "role": "user"}
        self.assertFalse(send_user_creation_request(user_data))
    
    @patch("requests.post")
    def test_send_user_creation_request_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"
        user_data = {"name": "Alice", "email": "alice@example.com", "role": "editor"}
        self.assertFalse(send_user_creation_request(user_data))
    
    @patch("requests.post", side_effect=requests.RequestException("Network Error"))
    def test_send_user_creation_request_exception(self, mock_post):
        user_data = {"name": "Bob", "email": "bob@example.com", "role": "moderator"}
        self.assertFalse(send_user_creation_request(user_data))
    
    def test_is_valid_row_valid(self):
        row = {"name": "Valid User", "email": "valid@example.com", "role": "admin"}
        self.assertTrue(is_valid_row(row))
    
    def test_is_valid_row_missing_fields(self):
        row = {"name": "No Email", "email": "", "role": "user"}
        self.assertFalse(is_valid_row(row))
    
    def test_is_valid_row_invalid_email(self):
        row = {"name": "Invalid Email", "email": "invalidemail", "role": "editor"}
        self.assertFalse(is_valid_row(row))
    
    @patch("builtins.open", new_callable=mock_open, read_data="name,email,role\nJohn Doe,john@example.com,admin\n")
    @patch("requests.post")
    @patch("os.path.exists", return_value=True)
    def test_create_users_success(self, mock_exists, mock_post, mock_file):
        mock_post.return_value.status_code = 201
        create_users("users.csv")
        mock_post.assert_called_once_with("https://example.com/api/create_user", json={"name": "John Doe", "email": "john@example.com", "role": "admin"})
    
    @patch("builtins.open", new_callable=mock_open, read_data="name,email,role\nInvalid User,invalidemail,admin\n")
    @patch("requests.post")
    @patch("os.path.exists", return_value=True)
    def test_create_users_invalid_email(self, mock_exists, mock_post, mock_file):
        create_users("users.csv")
        mock_post.assert_not_called()
    
    @patch("builtins.open", new_callable=mock_open, read_data="name,role\nNo Email,user\n")
    @patch("requests.post")
    @patch("os.path.exists", return_value=True)
    def test_create_users_missing_headers(self, mock_exists, mock_post, mock_file):
        with self.assertLogs(logging.getLogger(), level="ERROR") as log:
            create_users("users.csv")
            self.assertIn("Missing required headers in CSV", log.output[0])

    @patch("os.path.exists", return_value=False)
    def test_create_users_file_not_found(self, mock_exists):
        with self.assertLogs(logging.getLogger(), level="ERROR") as log:
            create_users("missing.csv")
            self.assertIn("File not found", log.output[0])
    
    @patch("builtins.open", side_effect=csv.Error("CSV Parsing Error"))
    @patch("os.path.exists", return_value=True)
    def test_create_users_csv_parsing_error(self, mock_exists, mock_file):
        with self.assertLogs(logging.getLogger(), level="ERROR") as log:
            create_users("users.csv")
            self.assertIn("CSV parsing error", log.output[0])

if __name__ == "__main__":
    unittest.main()
