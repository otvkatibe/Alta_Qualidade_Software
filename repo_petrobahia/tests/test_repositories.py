"""Testes unitários para o repositório de clientes em arquivo."""

import tempfile
from pathlib import Path

import pytest

from domain.entities import Client
from infrastructure.repositories import FileClientRepository


class TestFileClientRepository:
    """Casos de teste para FileClientRepository."""

    def test_save_client(self):
        """Testa o salvamento de um cliente no arquivo."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            client = Client(name="João Silva", email="joao@example.com", tier="gold")

            repo.save(client)

            # Lê o arquivo e verifica o conteúdo
            with open(temp_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "João Silva,joao@example.com,gold" in content
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_save_multiple_clients(self):
        """Testa o salvamento de múltiplos clientes."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            client1 = Client(name="João Silva", email="joao@example.com", tier="gold")
            client2 = Client(
                name="Maria Santos", email="maria@example.com", tier="silver"
            )

            repo.save(client1)
            repo.save(client2)

            clients = repo.load_all()
            assert len(clients) == 2
            assert clients[0].name == "João Silva"
            assert clients[1].name == "Maria Santos"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_load_all_clients(self):
        """Testa o carregamento de todos os clientes do arquivo."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", encoding="utf-8"
        ) as f:
            f.write("João Silva,joao@example.com,gold\n")
            f.write("Maria Santos,maria@example.com,silver\n")
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            clients = repo.load_all()

            assert len(clients) == 2
            assert clients[0].name == "João Silva"
            assert clients[0].email == "joao@example.com"
            assert clients[0].tier == "gold"
            assert clients[1].name == "Maria Santos"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_load_all_skips_malformed_lines(self):
        """Testa que linhas malformadas são ignoradas."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", encoding="utf-8"
        ) as f:
            f.write("João Silva,joao@example.com,gold\n")
            f.write("LinhaInválida\n")
            f.write("Maria Santos,maria@example.com,silver\n")
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            clients = repo.load_all()

            # Deve carregar apenas linhas válidas
            assert len(clients) == 2
            assert clients[0].name == "João Silva"
            assert clients[1].name == "Maria Santos"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_load_all_empty_file(self):
        """Testa o carregamento de um arquivo vazio."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            clients = repo.load_all()

            assert len(clients) == 0
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_load_all_file_not_found(self):
        """Testa que FileNotFoundError é lançado quando o arquivo não existe."""
        repo = FileClientRepository("/caminho/inexistente/clientes.txt")

        with pytest.raises(FileNotFoundError, match="Arquivo de clientes não encontrado"):
            repo.load_all()

    def test_load_all_skips_empty_lines(self):
        """Testa que linhas vazias são ignoradas."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", encoding="utf-8"
        ) as f:
            f.write("João Silva,joao@example.com,gold\n")
            f.write("\n")
            f.write("   \n")
            f.write("Maria Santos,maria@example.com,silver\n")
            temp_file = f.name

        try:
            repo = FileClientRepository(temp_file)
            clients = repo.load_all()

            assert len(clients) == 2
        finally:
            Path(temp_file).unlink(missing_ok=True)
