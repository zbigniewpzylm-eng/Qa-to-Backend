# ===============================
# POZIOM 1 – PODSTAWY (Junior QA)
# ===============================

# 1. Masz listę liczb:
numbers = [1, 2, 3, 4, 5, 6]

# * Utwórz listę liczb podniesionych do potęgi trzeciej.
result = [i*i*i for i in numbers]

# * Utwórz listę tylko liczb parzystych.
result = [i for i in numbers if i % 2 == 0]


# 2. Masz listę słów:
words = ["test", "api", "python", "selenium"]

# * Utwórz listę długości każdego słowa.
result = [len(word) for word in words]

# * Utwórz listę słów zapisanych wielkimi literami.
result = [i.upper() for i in words]


# ===============================
# POZIOM 2 – FILTRY I WARUNKI
# ===============================

# 3. Masz listę liczb:
numbers = list(range(1, 21))

# * Utwórz listę kwadratów liczb, które są podzielne przez 3.
result = [i*i for i in numbers if i % 3 == 0]

# * Utwórz listę liczb, które są nieparzyste i większe niż 10.
result = [i for i in numbers if i % 2 == 1 and i > 10]


# 4. Masz tekst:
text = "Quality assurance requires attention to detail"

# * Utwórz listę słów dłuższych niż 6 znaków.
result = [word for word in text.split() if len(word) > 6]

# * Utwórz listę długości słów, które zaczynają się od spółgłoski.
samogloski = ["a","e","o","u","i","y"]
result = [len(word) for word in text.split() if word[0].lower() not in samogloski]


# ===============================
# POZIOM 3 – SŁOWNIKI (Mid QA)
# ===============================

# 5. Masz słownik z wynikami testów:
results = {
    "test_login": True,
    "test_logout": False,
    "test_signup": True,
    "test_profile": False
}

# * Utwórz listę nazw testów, które zakończyły się sukcesem.
result = [k for k, v in results.items() if v == True]

# * Utwórz słownik tylko z testami, które się nie powiodły.
result = {k:v for k,v in results.items() if v == False}


# 6. Masz listę imion i listę wieków:
names = ["Anna", "Bartek", "Celina", "Daniel"]
ages = [28, 17, 34, 16]

# * Utwórz słownik: imię -> wiek, tylko dla osób pełnoletnich.
result = {name:age for name, age in zip(names,ages) if age >= 18}


# ===============================
# POZIOM 4 – LISTY SŁOWNIKÓW
# ===============================

# 7. Masz listę użytkowników:
users = [
    {"name": "Alice", "role": "admin", "active": True},
    {"name": "Bob", "role": "user", "active": False},
    {"name": "Charlie", "role": "user", "active": True},
    {"name": "Diana", "role": "admin", "active": False}
]

# * Utwórz listę imion aktywnych użytkowników.
result = [user["name"] for user in users if user["active"] == True]

# * Utwórz słownik: imię -> rola, tylko dla adminów.
result = {k["name"]:v["role"] for k,v in users if v["role"] == "admin"}


# ===============================
# POZIOM 5 – ZAGNIEŻDŻONE COMPREHENSION (Senior QA)
# ===============================

# 8. Masz listę list (np. dane z tabeli):
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# * Spłaszcz macierz do jednej listy.
# result = [...]

# * Utwórz listę kwadratów liczb większych niż 4.
# result = [...]


# 9. Masz tekst:
text = "api tests should be fast and reliable"

# * Utwórz słownik:
#   klucz -> pierwsza litera słowa
#   wartość -> lista słów zaczynających się na tę literę
# result = [...]


# ===============================
# POZIOM 6 – WYZWANIE (Senior+)
# ===============================

# 10. Masz dane:
names = ["Alice", "Bob", "Charlie", "Diana"]
scores = [85, 40, 90, 70]
statuses = ["pass", "fail", "pass", "fail"]

# * Utwórz słownik:
#   imię -> wynik
#   tylko dla osób, które:
#     - mają status "pass"
#     - wynik >= 80
# result = [...]
