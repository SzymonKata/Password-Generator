import random
import string
import subprocess
import platform

def generate_password(length, complexity, include_name=False, reject_zero=True):
    # Sprawdź poprawność poziomu zabezpieczenia
    if complexity == "słaby":
        allowed_chars = string.ascii_letters + string.digits
    elif complexity == "średni":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "")
    elif complexity == "silny":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "") + string.whitespace
    else:
        return None

    # Jeśli hasło ma zawierać nazwę, dodaj ją na początku
    if include_name:
        allowed_chars = allowed_chars.replace(name, "")
        password = name
    else:
        password = ''

    prev_char = ''

    # Generuj pozostałą część hasła
    while len(password) < length - 4:  # Zmieniono długość hasła o 4 znaki
        next_char = random.choice(allowed_chars)
        if reject_zero and prev_char == '0' and next_char == '0':
            continue
        password += next_char
        prev_char = next_char

    # Dodaj na końcu jedną dużą literę, jedną małą literę, jeden znak specjalny i jedną cyfrę
    password += random.choice(string.ascii_uppercase)  # Dodano jedną dużą literę
    password += random.choice(string.ascii_lowercase)  # Dodano jedną małą literę
    password += random.choice(string.punctuation.replace(":", "").replace('"', ""))  # Usunięto ":" i """
    password += random.choice(string.digits)  # Dodano jedną cyfrę

    # Jeśli hasło nie może zaczynać się od zera, zmień pierwszy znak
    if reject_zero and password[0] == "0":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace("0", "").replace(" ", "").replace(":", "").replace('"', "")
        password = password[1:] + random.choice(allowed_chars)

    # Usuń puste miejsca i spacje między znakami
    password = ''.join(password.split())

    return password

# Ustawienie minimalnej i maksymalnej długości hasła
min_length = 16
max_length = 26

# Pobierz długość hasła i poziom złożoności od użytkownika
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

# Generuj hasło
password = generate_password(int(length), complexity, include_name=include_name, reject_zero=True)

if password:
    # Zapisz hasło do pliku
    with open("haslo.txt", "w") as file:
        file.write("Wygenerowane hasło: " + password)
    print("Hasło zostało zapisane w pliku haslo.txt")

    # Otwórz plik .txt w odpowiednim edytorze tekstu na podstawie systemu operacyjnego
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
