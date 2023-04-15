import random
import string
import subprocess

def generate_password(length, complexity, include_name=False, reject_zero=True):
    # Sprawdź poprawność poziomu złożoności
    if complexity == "słaby":
        allowed_chars = string.ascii_letters + string.digits
    elif complexity == "średni":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation
    elif complexity == "silny":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    else:
        return None

    # Jeśli hasło ma zawierać imię, dodaj je na początku
    if include_name:
        allowed_chars = string.ascii_letters + string.digits + string.punctuation
        allowed_chars = allowed_chars.replace(name, "")
        password = name + ''.join(random.choice(allowed_chars) for _ in range(length - len(name)))
    else:
        password = ''.join(random.choice(allowed_chars) for _ in range(length))

    # Jeśli hasło nie może zaczynać się od zera, zmień pierwszy znak
    if reject_zero and password[0] == "0":
        password = password[1:] + random.choice(string.ascii_letters + string.digits + string.punctuation)

    return password

# Ustawienie minimalnej i maksymalnej długości hasła
min_length = 16
max_length = 28

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
    complexity = input("Podaj poziom złożoności (słaby, średni lub silny): ")
    if complexity not in ["słaby", "średni", "silny"]:
        print("Nieprawidłowy poziom złożoności hasła. Wybierz spośród: słaby, średni, silny.")
    else:
        break

include_name = False
name = ""
if input("Czy hasło ma zawierać twoją nazwę? (Tak/Nie): ").lower() == "tak":
    include_name = True
    while True:
        name = input("Podaj nazwę (maksymalnie 10 znaków, bez spacji, dwukropka i cudzysłowia): ")
        if len(name) > 10:
            print("Nazwa nie może przekraczać 10 znaków. Spróbuj ponownie.")
        elif any(char in name for char in [' ', ':', '"']):
            print("Nazwa nie może zawierać spacji, dwukropka ani cudzysłowia. Spróbuj ponownie.")
        else:
            break

# Generuj hasło
password = generate_password(int(length), complexity, include_name=include_name, reject_zero=True)

if password:
    print("Wygenerowane hasło:", password)
    # Zapisz hasło do pliku
    with open("haslo.txt", "w") as file:
        file.write("Wygenerowane hasło: " + password)
    print("Hasło zostało zapisane w pliku haslo.txt")
    # Otwórz plik .txt z hasłem
    try:
        subprocess.run(['notepad', 'haslo.txt'], check=True)  # Otwiera plik .txt z hasłem w notatniku na Windowsie
    except subprocess.CalledProcessError:
        print("Nie udało się otworzyć pliku z hasłem.")
else:
    print("Nie udało się wygenerować hasła. Spróbuj ponownie.")
