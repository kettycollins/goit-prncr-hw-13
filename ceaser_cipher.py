import string
from collections import defaultdict

# Функція для шифрування Цезаря
def caesar_encrypt(plaintext, shift):
    encrypted_text = []
    for char in plaintext:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

# Частотний аналіз шифротексту
def frequency_analysis(text):
    frequencies = defaultdict(int)
    total_chars = 0
    for char in text:
        if char.isalpha():
            frequencies[char.upper()] += 1
            total_chars += 1

    frequency_table = {char: round(frequencies[char] / total_chars * 100, 2) for char in frequencies}
    return frequency_table

# Функція для визначення зсуву на основі частотного аналізу
def determine_shift(frequency_table):
    # Знайдемо найчастішу літеру в шифрованому тексті
    max_freq_char = max(frequency_table, key=frequency_table.get)
    guessed_shift = (ord(max_freq_char) - ord('E')) % 26  # 'E' - найчастіша літера в англійській
    return guessed_shift

# Оригінальний текст
plaintext = """Knowledge is power. Understanding the world around us gives us the ability to change it. To learn is to grow, and to grow is to become a better version of ourselves."""

# Створення набору слів з оригінального тексту
english_words = set(word.lower().strip(string.punctuation) for word in plaintext.split())

# Функція для перевірки, чи є слово в англійському словнику
def is_english_word(word):
    return word.lower() in english_words

# Функція для оцінки розшифрованого тексту
def score_decryption(text):
    words = text.split()
    score = sum(is_english_word(word) for word in words)
    return score

# Спроба розшифрувати текст для кількох можливих зсувів
def try_multiple_shifts(ciphertext, max_shift=26):
    best_shift = 0
    best_score = 0
    best_decryption = ciphertext
    
    for shift in range(max_shift):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        score = score_decryption(decrypted_text)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_decryption = decrypted_text
    
    return best_shift, best_decryption

# Функція для дешифрування Цезаря
def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

# Зашифрований текст із зсувом на 3
shift = 3
ciphertext_caesar = caesar_encrypt(plaintext, shift)
print(f"Зашифрований текст Цезаря: {ciphertext_caesar}")

# Аналіз шифротексту
frequency_table_caesar = frequency_analysis(ciphertext_caesar)
print("Частотний розподіл шифротексту Цезаря:", frequency_table_caesar)

# Розшифрування тексту з зсувом 3
decrypted_caesar = caesar_decrypt(ciphertext_caesar, shift)
print(f"Розшифрований текст Цезаря (із зсувом 3): {decrypted_caesar}")

# Визначення зсуву на основі частотного аналізу
guessed_shift = determine_shift(frequency_table_caesar)
print(f"Визначений зсув за частотним аналізом: {guessed_shift}")

# Розшифрування тексту з визначеним зсувом
decrypted_caesar = caesar_decrypt(ciphertext_caesar, guessed_shift)
print(f"Розшифрований текст Цезаря: {decrypted_caesar}")

# Спроба знайти найкращий зсув
best_shift, best_decryption = try_multiple_shifts(ciphertext_caesar)
print(f"Найкращий зсув: {best_shift}")
print(f"Найкраще розшифрування: {best_decryption}")
