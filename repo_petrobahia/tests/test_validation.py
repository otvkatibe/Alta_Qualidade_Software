"""Testes unitários para o serviço de validação."""

import pytest

from domain.entities import Client
from services.validation import ClientValidator, EmailValidator


class TestEmailValidator:
    """Casos de teste para EmailValidator."""

    def test_valid_email(self):
        """Testa a validação de um email válido."""
        validator = EmailValidator()
        assert validator.is_valid("test@example.com") is True

    def test_valid_email_with_subdomain(self):
        """Testa a validação de email com subdomínio."""
        validator = EmailValidator()
        assert validator.is_valid("test@mail.example.com") is True

    def test_invalid_email_no_at(self):
        """Testa a validação de email sem o símbolo @."""
        validator = EmailValidator()
        assert validator.is_valid("testexample.com") is False

    def test_invalid_email_no_domain(self):
        """Testa a validação de email sem domínio."""
        validator = EmailValidator()
        assert validator.is_valid("test@") is False

    def test_invalid_email_no_extension(self):
        """Testa a validação de email sem extensão."""
        validator = EmailValidator()
        assert validator.is_valid("test@example") is False

    def test_empty_email(self):
        """Testa a validação de email vazio."""
        validator = EmailValidator()
        assert validator.is_valid("") is False

    def test_none_email(self):
        """Testa a validação de email None."""
        validator = EmailValidator()
        assert validator.is_valid(None) is False


class TestClientValidator:
    """Casos de teste para ClientValidator."""

    def test_valid_client(self):
        """Testa a validação de um cliente válido."""
        email_validator = EmailValidator()
        validator = ClientValidator(email_validator)
        client = Client(name="João Silva", email="joao@example.com", tier="gold")

        assert validator.validate(client) is True

    def test_client_with_invalid_email(self):
        """Testa a validação de cliente com formato de email inválido."""
        email_validator = EmailValidator()
        validator = ClientValidator(email_validator)
        client = Client(name="João Silva", email="email-invalido", tier="gold")

        with pytest.raises(ValueError, match="Formato de email inválido"):
            validator.validate(client)

    def test_client_with_empty_name(self):
        """Testa a validação de cliente com nome vazio."""
        email_validator = EmailValidator()
        validator = ClientValidator(email_validator)

        with pytest.raises(ValueError, match="O nome do cliente não pode estar vazio"):
            client = Client(name=" ", email="joao@example.com", tier="gold")
            validator.validate(client)

    def test_client_with_empty_email(self):
        """Testa a validação de cliente com email vazio."""
        email_validator = EmailValidator()
        validator = ClientValidator(email_validator)

        with pytest.raises(ValueError, match="O email do cliente não pode estar vazio"):
            client = Client(name="João Silva", email=" ", tier="gold")
            validator.validate(client)

    def test_client_with_empty_tier(self):
        """Testa a validação de cliente com nível vazio."""
        email_validator = EmailValidator()
        validator = ClientValidator(email_validator)

        with pytest.raises(ValueError, match="O nível do cliente não pode estar vazio"):
            client = Client(name="João Silva", email="joao@example.com", tier=" ")
            validator.validate(client)
