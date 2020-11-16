import unittest

from testfixtures import TempDirectory

import main


class CheckNumberTest(unittest.TestCase):
    def test_retrieve_list_from_input(self):
        # given
        d = TempDirectory()
        payload = (
            "elixirem [ELIXIR - em] e l i k s i r e m\n"
            "elixirowi [Elixir] e l i k s i r o w i\n"
            "elixiry [Elixir] e l i k s i r y\n"
        )
        x = bytes(payload, "utf-8")
        response = main.retrieve_list_from_input(d.write("test.txt", x))
        # then
        self.assertEqual(3, len(response))
        self.assertEqual(
            [
                ["elixirem", "[ELIXIR - em]", "e l i k s i r e m\n"],
                ["elixirowi", "[Elixir]", "e l i k s i r o w i\n"],
                ["elixiry", "[Elixir]", "e l i k s i r y\n"],
            ],
            response,
        )
        d.cleanup()

    def test_retrieve_list_from_input__when_input_lacks_spaces(self):
        # given
        d = TempDirectory()
        payload = (
            "ipconfig [IPconfig] a j p i k o n f i k\n"
            "ipconfig [IPconfig] i p e k o n f i g\n"
            "ipconfig [IPconfig] i p e k o n f i k\n"
            "iphona [iphona] a j f o n a\n"
            "iphona [iphona] i p h o n a\n"
        )
        x = bytes(payload, "utf-8")
        response = main.retrieve_list_from_input(d.write("test.txt", x))
        # then
        self.assertEqual(5, len(response))
        self.assertEqual(
            [
                ["ipconfig", "[IPconfig]", "a j p i k o n f i k\n"],
                ["ipconfig", "[IPconfig]", "i p e k o n f i g\n"],
                ["ipconfig", "[IPconfig]", "i p e k o n f i k\n"],
                ["iphona", "[iphona]", "a j f o n a\n"],
                ["iphona", "[iphona]", "i p h o n a\n"],
            ],
            response,
        )
        d.cleanup()

    def test_find_duplicates_ort_vs_disp(self):
        # given
        d = TempDirectory()
        payload = (
            "adekwatne [adekwatne] a d e k f a t n e\n"
            "abstynenta [Abstynenta] a b s t y n e n t a\n"
            "bąk [bąk] b a_ k\n"
            "bąk [Bąk] b o n k\n"
            "Bąk [Bąk] b a_ k\n"
            "3dsecure [3-D Secure] cz y d e s e k j u r\n"
            "3dsecure [trzy D Secure] t sz y d e s e k j u r"
        )
        x = bytes(payload, "utf-8")
        lines = main.retrieve_list_from_input(d.write("test.txt", x))

        # when
        response = main.find_duplicates_ort_vs_disp(lines)

        # then
        self.assertEqual(4, len(response))
        self.assertEqual(
            [
                ["bąk", "[bąk]", "b a_ k\n"],
                ["bąk", "[Bąk]", "b o n k\n"],
                ["3dsecure", "[3-D Secure]", "cz y d e s e k j u r\n"],
                ["3dsecure", "[trzy D Secure]", "t sz y d e s e k j u r"],
            ],
            response,
        )

        d.cleanup()

    def test_find_duplicates_ort_symbols(self):
        d = TempDirectory()
        payload = (
            "email [e-mail] i m e j l\n"
            "emaili [emaili] e m a i l i\n"
            "e_mailem [e-mailem] i m e j l e m\n"
            "e_maili [e-maili] i m e j l i\n"
            "e_maili [e-maili] e m e j l i\n"
            "sister_s [sister's] s i s t e r s\n"
            "sisters [sister's] s i s t e r s\n"
        )
        x = bytes(payload, "utf-8")
        lines = main.retrieve_list_from_input(d.write("test2.txt", x))

        # when
        response = main.find_duplicate_ort_words_ignoring_symbols(lines)

        # then
        self.assertEqual(3, len(response))
        self.assertEqual(
            [
                ["e_maili", "[e-maili]", "i m e j l i\n"],
                ["e_maili", "[e-maili]", "e m e j l i\n"],
                ["sister_s", "[sister's]", "s i s t e r s\n"],
            ],
            response,
        )
        d.cleanup()

    def test_find_phonetic_duplicates(self):
        d = TempDirectory()
        payload = (
            "puchatek [Puchatek] p u h a t e k\n"
            "puchatek [puchatek] p u h a t e k\n"
            "puchatka [Puchatka] p u h a t k a\n"
            "puchatka [puchatka] p u h a t k a\n"
            "spróbuję [spróbuję] s p r u b u j e\n"
            "żabce [żabce] rz a p c e\n"
        )
        x = bytes(payload, "utf-8")
        lines = main.retrieve_list_from_input(d.write("test3.txt", x))

        # when
        response = main.find_phonetic_duplicates(lines)

        # then
        self.assertEqual(4, len(response))
        self.assertEqual(
            [
                ["puchatek", "[Puchatek]", "p u h a t e k\n"],
                ["puchatek", "[puchatek]", "p u h a t e k\n"],
                ["puchatka", "[Puchatka]", "p u h a t k a\n"],
                ["puchatka", "[puchatka]", "p u h a t k a\n"],
            ],
            response,
        )
        d.cleanup()

    def test_find_full_duplicates(self):
        d = TempDirectory()
        payload = (
            "puchatek [Puchatek] p u h a t e k\n"
            "puchatek [puchatek] p u h a t e k\n"
            "puchatek [puchatek] p u h a t e k\n"
            "puchatka [Puchatka] p u h a t k a\n"
            "puchatka [puchatka] p u h a t k a\n"
            "spróbuję [spróbuję] s p r u b u j e\n"
            "spróbuję [spróbuję] s p r u b u j e\n"
            "żabce [żabce] rz a p c e\n"
        )
        x = bytes(payload, "utf-8")
        lines = main.retrieve_list_from_input(d.write("test3.txt", x))

        # when
        response = main.find_full_duplicates(lines)

        # then
        self.assertEqual(2, len(response))
        self.assertEqual(
            [
                ["puchatek", "[puchatek]", "p u h a t e k\n"],
                ["spróbuję", "[spróbuję]", "s p r u b u j e\n"],
            ],
            response,
        )
        d.cleanup()


if __name__ == "__main__":
    unittest.main()
