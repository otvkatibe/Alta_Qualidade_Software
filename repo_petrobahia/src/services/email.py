from domain.services import EmailSender


class ConsoleEmailService(EmailSender):
    """Serviço de email que imprime no console (para testes/desenvolvimento)."""

    def send(self, to: str, subject: str, body: str) -> None:
        """Imprime os detalhes do email no console."""
        print("--- Email ---")
        print(f"Para: {to}")
        print(f"Assunto: {subject}")
        print(f"Mensagem: {body}")
        print("-------------")


class WelcomeEmailService:
    """Serviço para envio de emails de boas-vindas para novos clientes."""

    def __init__(self, email_sender: EmailSender):
        """Inicializa com a dependência do enviador de email."""
        self._email_sender = email_sender

    def send_welcome(self, email: str, name: str) -> None:
        """Envia email de boas-vindas para novo cliente."""
        subject = "Bem-vindo à PetroBahia!"
        body = (
            f"Olá {name},\n\n"
            "Seja bem-vindo ao nosso serviço!\n\n"
            "Atenciosamente,\nEquipe PetroBahia"
        )
        self._email_sender.send(email, subject, body)

    def send_greeting(self, email: str) -> None:
        """Envia email de saudação simples."""
        subject = "Saudações da PetroBahia"
        body = "Obrigado por ser nosso valorizado cliente!"
        self._email_sender.send(email, subject, body)
