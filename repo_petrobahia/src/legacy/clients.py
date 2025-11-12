"""
Module for client data management.

This module provides functionality to load and manage client information
from text files.
"""

import re

REGEX_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def load_clients(file_path):
    """
    Load client data from a text file.

    Args:
        file_path (str): Path to the file containing client data.

    Returns:
        list: A list of dictionaries containing client information.
              Each dictionary has 'name', 'email', and 'tier' keys.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    clients = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    client = {
                        "name": parts[0].strip(),
                        "email": parts[1].strip(),
                        "tier": parts[2].strip(),
                    }
                    clients.append(client)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Client file not found: {file_path}") from exc

    return clients


class ClientValidator:
    """Validates client data including email format and required fields."""

    @staticmethod
    def validate_email(email):
        """Validate email format using regex."""
        return bool(re.match(REGEX_EMAIL, email))

    def validate(self, client):
        """
        Validate client data.

        Args:
            client (dict): Client dictionary with 'email' and 'name' keys.

        Returns:
            bool: True if client data is valid, False otherwise.
        """
        if "email" not in client or "name" not in client:
            print("Missing mandatory fields")
            return False
        if not self.validate_email(client["email"]):
            print("Invalid email format")
            return False
        return True


class ClientRepository:
    """Repository for persisting client data to file."""

    def __init__(self, file_path="clients.txt"):
        """
        Initialize repository with file path.

        Args:
            file_path (str): Path to the clients file.
        """
        self.file_path = file_path

    def save(self, client):
        """
        Save client data to file.

        Args:
            client (dict): Client dictionary to save.
        """
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(str(client) + "\n")

    def load_all(self):
        """
        Load all clients from file.

        Returns:
            list: List of client dictionaries.
        """
        return load_clients(self.file_path)


class EmailService:
    """Service for sending emails to clients."""

    @staticmethod
    def send_greeting(email):
        """
        Send greeting email to client.

        Args:
            email (str): Client email address.
        """
        print(f"Sending greeting email to {email}")

    def send_welcome(self, email, name):
        """
        Send welcome email with personalized message.

        Args:
            email (str): Client email address.
            name (str): Client name.
        """
        print(f"Sending welcome email to {name} at {email}")


def register_client(client):
    """
    Register a new client in the system.

    Args:
        client (dict): Client data dictionary.

    Returns:
        bool: True if registration successful, False otherwise.
    """
    validator = ClientValidator()
    repository = ClientRepository()
    email_service = EmailService()

    if not validator.validate(client):
        return False

    repository.save(client)
    email_service.send_greeting(client["email"])
    return True
