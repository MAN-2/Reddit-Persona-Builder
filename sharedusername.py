# shared.py — reads/writes username to a text file

def set_username(name):
    with open("username.txt", "w", encoding="utf-8") as f:
        f.write(name.strip())

def get_username():
    try:
        with open("username.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
