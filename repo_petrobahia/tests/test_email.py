"""Testes unitários para o serviço de email."""

from unittest.mock import MagicMock

from services.email import ConsoleEmailService, WelcomeEmailService


class TestConsoleEmailService:
    """Casos de teste para ConsoleEmailService."""

    def test_send_email(self, capsys):
        """Testa que o envio de email imprime no console."""
        service = ConsoleEmailService()
        service.send("test@example.com", "Assunto Teste", "Corpo Teste")

        captured = capsys.readouterr()
        assert "Para: test@example.com" in captured.out
        assert "Assunto: Assunto Teste" in captured.out
        assert "Mensagem: Corpo Teste" in captured.out


class TestWelcomeEmailService:
    """Casos de teste para WelcomeEmailService."""

    def test_send_welcome(self):
        """Testa o envio de email de boas-vindas."""
        mock_sender = MagicMock()
        service = WelcomeEmailService(mock_sender)

        service.send_welcome("joao@example.com", "João Silva")

        mock_sender.send.assert_called_once()
        call_args = mock_sender.send.call_args
        assert call_args[0][0] == "joao@example.com"
        assert "Bem-vindo à PetroBahia!" in call_args[0][1]
        assert "João Silva" in call_args[0][2]

    def test_send_greeting(self):
        """Testa o envio de email de saudação."""
        mock_sender = MagicMock()
        service = WelcomeEmailService(mock_sender)

        service.send_greeting("joao@example.com")

        mock_sender.send.assert_called_once()
        call_args = mock_sender.send.call_args
        assert call_args[0][0] == "joao@example.com"
        assert "Saudações da PetroBahia" in call_args[0][1]
