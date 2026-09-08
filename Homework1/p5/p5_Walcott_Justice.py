# p5_Walcott_Justice.py
# Justice Walcott
# Caesar cipher encryption/decryption and letter frequency analysis.

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def caesar_cipher(text, shift):
    """Shift every letter in text forward by shift positions.

    Spaces, punctuation, and digits are left alone, and the original
    upper/lower casing of each letter is preserved.
    """
    result = ""
    for character in text:
        lowered = character.lower()
        position = -1
        # Find where this character lives in the alphabet using indexing.
        for i in range(len(ALPHABET)):
            if ALPHABET[i] == lowered:
                position = i
        if position == -1:
            # Not a letter, so copy it through unchanged.
            result = result + character
        else:
            new_position = (position + shift) % 26
            new_letter = ALPHABET[new_position]
            if character.isupper():
                new_letter = new_letter.upper()
            result = result + new_letter
    return result


def caesar_decipher(ciphertext, shift):
    """Undo caesar_cipher by shifting the letters back the other way."""
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """Count how often each letter a-z appears, ignoring case and non-letters.

    Returns a dictionary whose keys are the 26 lowercase letters.
    """
    counts = {}
    for letter in ALPHABET:
        counts[letter] = 0
    for character in text:
        lowered = character.lower()
        if lowered in counts:
            counts[lowered] = counts[lowered] + 1
    return counts


def print_frequency(counts):
    """Display the letter counts, one line per letter that actually appears."""
    total = 0
    for letter in ALPHABET:
        total = total + counts[letter]
    if total == 0:
        print("  (no alphabetic characters found)")
        return
    for letter in ALPHABET:
        if counts[letter] > 0:
            bar = "*" * counts[letter]
            percent = counts[letter] / total * 100
            print("  " + letter + ": " + str(counts[letter]).rjust(3) +
                  "  (" + format(percent, ".1f") + "%)  " + bar)
    print("  total letters: " + str(total))


def get_shift():
    """Ask the user for a whole-number shift value until they give a valid one."""
    while True:
        entry = input("Enter a shift value (whole number): ")
        try:
            return int(entry)
        except ValueError:
            print("That is not a whole number. Please try again.")


def main():
    print("=" * 46)
    print(" Caesar Cipher and Letter Frequency Analyzer")
    print("=" * 46)

    while True:
        print()
        print("Menu:")
        print("  1) Encrypt a message")
        print("  2) Decrypt a message")
        print("  3) Letter frequency of a message")
        print("  4) Full report (cipher + frequency + decipher)")
        print("  5) Quit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            message = input("Enter your message: ")
            shift = get_shift()
            print("Ciphered text: " + caesar_cipher(message, shift))

        elif choice == "2":
            message = input("Enter the ciphered message: ")
            shift = get_shift()
            print("Deciphered text: " + caesar_decipher(message, shift))

        elif choice == "3":
            message = input("Enter your message: ")
            print("Letter frequency:")
            print_frequency(letter_frequency(message))

        elif choice == "4":
            message = input("Enter your message: ")
            shift = get_shift()
            ciphered = caesar_cipher(message, shift)
            deciphered = caesar_decipher(ciphered, shift)
            print()
            print("Original text:   " + message)
            print("Ciphered text:   " + ciphered)
            print("Deciphered text: " + deciphered)
            print("Letter frequency of the original text:")
            print_frequency(letter_frequency(message))
            print("Letter frequency of the ciphered text:")
            print_frequency(letter_frequency(ciphered))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
