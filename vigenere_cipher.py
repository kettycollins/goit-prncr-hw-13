import math
from collections import defaultdict

ENGLISH_FREQUENCIES = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23, 'G': 2.02, 'H': 6.09,
    'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93,
    'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}

# Крок 1. Шифрування та дешифрування за Відомим Ключем
def vigenere_encrypt(plaintext, key):
    encrypted_text = []
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - ord('A') - shift + 26) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

# Метод Касіскі
def find_repeating_sequences(text, length=3):
    sequences = defaultdict(list)
    for i in range(len(text) - length + 1):
        sequence = text[i:i+length]
        sequences[sequence].append(i)
    return {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

def calculate_distances(repeating_sequences):
    distances = []
    for positions in repeating_sequences.values():
        for i in range(1, len(positions)):
            distances.append(positions[i] - positions[i - 1])
    return distances

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_gcd_for_list(nums):
    return math.gcd(*nums) if nums else 1

# Тест Фрідмана
def calculate_ic(text):
    frequencies = defaultdict(int)
    for char in text:
        if char.isalpha():
            frequencies[char] += 1
    N = len(text)
    ic = sum(freq * (freq - 1) for freq in frequencies.values())
    ic /= (N * (N - 1))
    return ic

def friedman_test(ciphertext):
    N = len(ciphertext)
    IC = calculate_ic(ciphertext)
    K = (0.0265 * N) / (0.065 - IC + (N * IC - 1))
    return round(K)

# Частотний аналіз для відновлення ключа
def frequency_analysis(ciphertext, key_length):
    key = []
    for i in range(key_length):
        subtext = ''.join([ciphertext[j] for j in range(i, len(ciphertext), key_length) if ciphertext[j].isalpha()])
        best_shift = find_best_shift(subtext)
        key.append(chr(best_shift + ord('A')))
    return ''.join(key)

def find_best_shift(subtext):
    min_difference = float('inf')
    best_shift = 0
    for shift in range(26):
        shifted_subtext = ''.join(chr((ord(char) - shift - ord('A')) % 26 + ord('A')) for char in subtext)
        frequencies = calculate_frequencies(shifted_subtext)
        difference = calculate_frequency_difference(frequencies, ENGLISH_FREQUENCIES)
        if difference < min_difference:
            min_difference = difference
            best_shift = shift
    return best_shift

def calculate_frequencies(text):
    frequencies = defaultdict(int)
    total = 0
    for char in text:
        if char.isalpha():
            frequencies[char.upper()] += 1
            total += 1
    for char in frequencies:
        frequencies[char] = frequencies[char] / total * 100
    return frequencies

def calculate_frequency_difference(frequencies, expected_frequencies):
    difference = 0
    for letter in expected_frequencies:
        difference += abs(frequencies.get(letter, 0) - expected_frequencies[letter])
    return difference

# Основна функція
if __name__ == "__main__":
    # Оригінальний текст
    plaintext = """Knowledge is power. Understanding the world around us gives us the ability to change it. To learn is to grow, and to grow is to become a better version of ourselves."""
    key = "KEY"
    
    # 1. Шифрування тексту
    encrypted_text = vigenere_encrypt(plaintext, key)
    print(f"Зашифрований текст (з ключем '{key}'): {encrypted_text}")

    # 2. Дешифрування тексту
    decrypted_text = vigenere_decrypt(encrypted_text, key)
    print(f"Розшифрований текст: {decrypted_text}")

    # 3. Метод Касіскі
    repeating_sequences = find_repeating_sequences(encrypted_text)
    distances = calculate_distances(repeating_sequences)
    probable_key_length_kasiski = find_gcd_for_list(distances) if distances else None
    print(f"Ймовірна довжина ключа за методом Касіскі: {probable_key_length_kasiski}")

    # 4. Тест Фрідмана
    probable_key_length_friedman = friedman_test(encrypted_text)
    print(f"Оцінена довжина ключа за тестом Фрідмана: {probable_key_length_friedman}")

    # 5. Частотний аналіз
    estimated_key_length = probable_key_length_kasiski or probable_key_length_friedman
    estimated_key = frequency_analysis(encrypted_text, estimated_key_length)
    print(f"Відновлений ключ: {estimated_key}")

    # 6. Розшифрування тексту за відновленим ключем
    decrypted_with_estimated_key = vigenere_decrypt(encrypted_text, estimated_key)
    print(f"Розшифрований текст (з відновленим ключем): {decrypted_with_estimated_key}")