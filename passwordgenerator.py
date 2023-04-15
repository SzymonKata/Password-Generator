import random
import string
import subprocess

def generate_password(length, complexity, include_name=False, reject_zero=True):
    # Sprawdź poprawność poziomu złożoności
    if complexity == "słaby":
        allowed_chars = string.ascii_letters + string.digits
    elif complexity == "średni":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "")
    elif complexity == "silny":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', "") + string.whitespace
    else:
        return None

    # Jeśli hasło ma zawierać imię, dodaj je na początku
    if include_name:
        allowed_chars = allowed_chars.replace(name, "")
        password = name
    else:
        password = ''

    prev_char = ''

    # Wybierz pierwsze trzy cyfry lub znaki specjalne
    first_chars = random.sample(string.digits + string.punctuation.replace(" ", "").replace(":", "").replace('"', ""), 3)
    random.shuffle(first_chars)
    password += ''.join(first_chars)

    # Generuj pozostałą część hasła
    for _ in range(length - 3):
        curr_char = random.sample(allowed_chars, 1)[0]
        allowed_chars = allowed_chars.replace(curr_char, '')
        if curr_char in string.ascii_letters and prev_char in string.ascii_letters and \
                curr_char.lower() == prev_char.lower():
            # Jeśli generowany znak jest literą i poprzedni znak jest literą oraz są one równa małymi literami,
            # wygeneruj nowy znak z innych dostępnych znaków
            curr_char = random.sample(allowed_chars, 1)[0]
            allowed_chars = allowed_chars.replace(curr_char, '')
        password += curr_char
        prev_char = curr_char

    # Jeśli hasło nie może zaczynać się od zera, zmień pierwszy znak
    if reject_zero and password[0] == "0":
        allowed_chars = string.ascii_letters + string.digits + string.punctuation.replace("0", "").replace(" ", "").replace(":", "").replace('"', "")
        password = password[1:] + random.choice(allowed_chars)

    # Usuń puste miejsca i spacje między znakami
    password = ''.join(password.split())

    return password

# Ustawienie minimalnej i maksymalnej długości hasła
min_length = 15
max_length = 24

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
    # Otwórz plik .txt z hasłem
    try:
        subprocess.run(['notepad', 'haslo.txt'], check=True)  # Otwiera plik .txt z hasłem w notatniku na Windowsie
    except subprocess.CalledProcessError:
        print("Nie udało się otworzyć pliku z hasłem.")
else:
    print("Nie udało się wygenerować hasła. Spróbuj ponownie.")
