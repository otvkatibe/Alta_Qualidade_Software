from domain.entities import Client
from domain.repositories import ClientWriter
from domain.services import ClientValidator, EmailSender


class RegisterClientUseCase:
    """
    Caso de uso para registrar um novo cliente.

    Segue o Princípio da Inversão de Dependência ao depender de abstrações.
    """

    def __init__(
        self,
        repository: ClientWriter,
        validator: ClientValidator,
        email_sender: EmailSender,
    ):
        """Inicializa o caso de uso de registro de cliente."""
        self._repository = repository
        self._validator = validator
        self._email_sender = email_sender

    def execute(self, client: Client) -> bool:
        """Registra um novo cliente."""
        # Valida os dados do cliente
        self._validator.validate(client)

        # Salva no repositório
        self._repository.save(client)

        # Envia email de boas-vindas
        subject = "Bem-vindo à PetroBahia!"
        body = (
            f"Olá {client.name},\n\n"
            "Obrigado por se registrar!\n\n"
            "Atenciosamente,\nEquipe PetroBahia"
        )
        self._email_sender.send(client.email, subject, body)

        return True
