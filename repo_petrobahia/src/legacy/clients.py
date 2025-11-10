import re

REGEX_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def register_client(client):
    if "email" not in client or "name" not in cliente:
        print("Missing mandatory fields")
        return False
    if not re.match(REGEX_EMAIL, client["email"]):
        print("Invalid email format")
        return False
    
    file = open("clients.txt", "a", encoding="utf-8")
    file.write(str(client) + "\n")
    file.close()
    
    print("Sending greeting email to ", client["email"])
    return True
