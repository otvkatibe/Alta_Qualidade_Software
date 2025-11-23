"""Testes unitários para o caso de uso de gerenciamento de clientes."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from domain.entities import Client
from infrastructure.repositories import FileClientRepository
from services.validation import ClientValidator, EmailValidator
from use_cases.client_management import RegisterClientUseCase


class TestRegisterClientUseCase:
    """Casos de teste para RegisterClientUseCase."""

    def test_register_valid_client(self):
        """Testa o registro de um cliente válido."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            email_validator = EmailValidator()
            validator = ClientValidator(email_validator)
            mock_email = MagicMock()

            use_case = RegisterClientUseCase(repo, validator, mock_email)
            client = Client(name="João Silva", email="joao@example.com", tier="gold")

            result = use_case.execute(client)

            assert result is True
            mock_email.send.assert_called_once()

            # Verifica que o cliente foi salvo
            saved_clients = repo.load_all()
            assert len(saved_clients) == 1
            assert saved_clients[0].name == "João Silva"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_register_invalid_email_raises_error(self):
        """Testa que email inválido gera ValueError."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            email_validator = EmailValidator()
            validator = ClientValidator(email_validator)
            mock_email = MagicMock()

            use_case = RegisterClientUseCase(repo, validator, mock_email)
            client = Client(name="João Silva", email="email-invalido", tier="gold")

            with pytest.raises(ValueError, match="Formato de email inválido"):
                use_case.execute(client)

            # Verifica que nenhum email foi enviado
            mock_email.send.assert_not_called()
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_register_sends_welcome_email(self):
        """Testa que o email de boas-vindas é enviado ao cliente."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            email_validator = EmailValidator()
            validator = ClientValidator(email_validator)
            mock_email = MagicMock()

            use_case = RegisterClientUseCase(repo, validator, mock_email)
            client = Client(name="João Silva", email="joao@example.com", tier="gold")

            use_case.execute(client)

            # Verifica que o email foi enviado com os parâmetros corretos
            call_args = mock_email.send.call_args
            assert call_args[0][0] == "joao@example.com"
            assert "Bem-vindo à PetroBahia!" in call_args[0][1]
            assert "João Silva" in call_args[0][2]
        finally:
            Path(temp_file).unlink(missing_ok=True)
