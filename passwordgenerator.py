import random
import string
import subprocess
import platform

def generate_password(length, complexity, include_name=False, reject_zero=True):
    # Tym silniejsza kompleksowość, tym więcej różnych znaków program ma szansę wygenerować. Hasło generuje długość, kompleksowość, nazwę jeżeli użytkownik wybrał.
    if complexity == "słaby":
        allowed_chars = string.ascii_letters + string.digits
    elif complexity == "średni":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "")
    elif complexity == "silny":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "") + string.whitespace
    else:
        return None

    # Opcjonalna własna nazwa do hasła
    if include_name:
        allowed_chars = allowed_chars.replace(name, "")
        password = name
    else:
        password = ''

    prev_char = ''

    # Kod stara się, żeby hasło nie zawierało dwóch tych samych znaków między sobą. Nie dotyczy nazwy własnej do hasła.
    while len(password) < length - 2:
        next_char = random.choice(allowed_chars)
        if reject_zero and prev_char == '0' and next_char == '0':
            continue
        password += next_char
        prev_char = next_char

    # Zmienia pierwszy znak na inny, jeżeli tym pierwszym jest cyfra 0
    if reject_zero and password[0] == "0":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace("0", "").replace(" ", "").replace(":", "").replace('"', "")
        password = password[1:] + random.choice(allowed_chars)

    # Usuwa puste miejsca i spacje między znakami.
    password = ''.join(password.split())

    return password

# Minimalna i maksymalna długość hasła
min_length = 20
max_length = 32

# Pobiera dane o długości hasła i poziom kompleksowośći od użytkownika
while True:
    length = input(f"Podaj długość hasła (minimum {min_length}, maksimum {max_length} znaków): ")
    if not length.isdigit() or int(length) <= 0:
        print("Podana długość hasła musi być liczbą dodatnią. Spróbuj ponownie.")
    elif int(length) < min_length:
        print(f"Minimalna długość hasła to {min_length} znaków. Spróbuj ponownie.")
    elif int(length) > max_length:
        print(f"Maksymalna długość hasła to {max_length} znaków. Spróbuj ponownie.")
    else:
        break

while True:
    complexity = input("Podaj poziom zabezpieczenia hasła (słaby, średni lub silny): ")
    if complexity not in ["słaby", "średni", "silny"]:
        print("Nieprawidłowy poziom zabezpieczenia hasła. Wybierz spośród opcji: słaby, średni, silny.")
    else:
        break

include_name = False
name = ""
while True:
    user_input = input("Czy hasło ma zawierać wybraną przez ciebie nazwę? (Tak/Nie): ").lower()
    if user_input == "tak":
        include_name = True
        while True:
            name = input("Podaj nazwę (maksymalnie 10 znaków, bez spacji, dwukropka i cudzysłowia): ")
            if len(name) > 10:
                print("Nazwa nie może przekraczać 10 znaków. Spróbuj ponownie.")
            elif any(char in name for char in [' ', ':', '"']):
                print("Nazwa nie może zawierać spacji, dwukropka ani cudzysłowia. Spróbuj ponownie.")
            else:
                break
        break
    elif user_input == "nie":
        break
    else:
        print("Niepoprawna odpowiedź. Proszę odpowiedzieć 'Tak' lub 'Nie'.")

# Odpowiada za generowanie hasła.
password = generate_password(int(length), complexity, include_name=include_name, reject_zero=True)

length = random.randint(11, 20)
password += random.choice(string.ascii_letters + string.digits + string.punctuation)
if not any(char.isupper() for char in password):
         password += random.choice(string.ascii_uppercase)
if not any(char.islower() for char in password):
         password += random.choice(string.ascii_lowercase)
if not any(char in string.punctuation.replace(":", "").replace('"', "") for char in password):
         password += random.choice(string.punctuation.replace(":", "").replace('"', ""))
if not any(char.isdigit() for char in password):
         password += random.choice(string.digits)

if password:
    # Zapisuje hasło do pliku .txt
    with open("haslo.txt", "w") as file:
        file.write("Wygenerowane hasło: " + password)
    print("Hasło zostało zapisane w pliku haslo.txt")

    # Otwiera plik .txt w odpowiednim edytorze tekstu na podstawie danego systemu operacyjnego
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", "haslo.txt"])
    elif system == "Windows":  # Windows
        subprocess.run(["start", "notepad", "haslo.txt"], shell=True)
    elif system == "Linux":  # Linux
        subprocess.run(["xdg-open", "haslo.txt"])
    else:
        print("Nieobsługiwany system operacyjny.")
else:
    print("Nie udało się wygenerować hasła.")
