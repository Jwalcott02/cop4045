# p5_Walcott_Justice_test.py
# Justice Walcott
# Unit tests for the Caesar cipher and letter frequency functions.

import unittest

from p5_Walcott_Justice import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):

    def test_basic_shift(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")

    def test_wraps_around_alphabet(self):
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_preserves_uppercase(self):
        self.assertEqual(caesar_cipher("ABC", 1), "BCD")

    def test_preserves_mixed_case(self):
        self.assertEqual(caesar_cipher("Hello", 3), "Khoor")

    def test_preserves_spaces_and_punctuation(self):
        self.assertEqual(caesar_cipher("Hello, World!", 3), "Khoor, Zruog!")

    def test_zero_shift_returns_same_text(self):
        self.assertEqual(caesar_cipher("Same Text!", 0), "Same Text!")

    def test_shift_of_26_returns_same_text(self):
        self.assertEqual(caesar_cipher("Same Text!", 26), "Same Text!")

    def test_negative_shift(self):
        self.assertEqual(caesar_cipher("bcd", -1), "abc")

    def test_shift_larger_than_alphabet(self):
        self.assertEqual(caesar_cipher("abc", 27), caesar_cipher("abc", 1))

    def test_digits_and_symbols_untouched(self):
        self.assertEqual(caesar_cipher("abc123!@#", 2), "cde123!@#")


class TestCaesarDecipher(unittest.TestCase):

    def test_basic_decipher(self):
        self.assertEqual(caesar_decipher("bcd", 1), "abc")

    def test_decipher_undoes_cipher(self):
        original = "Hello, World! Zz"
        for shift in range(-30, 30):
            ciphered = caesar_cipher(original, shift)
            self.assertEqual(caesar_decipher(ciphered, shift), original)

    def test_decipher_preserves_case_and_punctuation(self):
        self.assertEqual(caesar_decipher("Khoor, Zruog!", 3), "Hello, World!")

    def test_decipher_wraps_around(self):
        self.assertEqual(caesar_decipher("abc", 3), "xyz")


class TestLetterFrequency(unittest.TestCase):

    def test_counts_simple_word(self):
        counts = letter_frequency("aabbc")
        self.assertEqual(counts["a"], 2)
        self.assertEqual(counts["b"], 2)
        self.assertEqual(counts["c"], 1)
        self.assertEqual(counts["d"], 0)

    def test_is_case_insensitive(self):
        counts = letter_frequency("AaAa")
        self.assertEqual(counts["a"], 4)

    def test_ignores_non_alphabetic_characters(self):
        counts = letter_frequency("a1 b2! c3?")
        self.assertEqual(counts["a"], 1)
        self.assertEqual(counts["b"], 1)
        self.assertEqual(counts["c"], 1)
        total = sum(counts.values())
        self.assertEqual(total, 3)

    def test_returns_all_26_letters_as_keys(self):
        counts = letter_frequency("xyz")
        self.assertEqual(len(counts), 26)
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.assertIn(letter, counts)

    def test_empty_string_gives_all_zero_counts(self):
        counts = letter_frequency("")
        self.assertEqual(sum(counts.values()), 0)

    def test_no_alphabetic_characters(self):
        counts = letter_frequency("12345 !@#$%")
        self.assertEqual(sum(counts.values()), 0)


if __name__ == "__main__":
    unittest.main()
