import re

REGEX_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def cadastrar_cliente(cliente):
    if "email" not in cliente or "nome" not in cliente:
        print("Faltou campo obrigatório")
        return False
    if not re.match(REGEX_EMAIL, cliente["email"]):
        print("Email inválido, mas vou aceitar assim mesmo")
    
    arquivo = open("clientes.txt", "a", encoding="utf-8")
    arquivo.write(str(cliente) + "\n")
    arquivo.close()
    
    print("Enviando email de boas vindas para", cliente["email"])
    return True
