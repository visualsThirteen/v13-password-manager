import random
import string


class PasswordGenerator:
    """
    Encapsulates logic for generating passwords.
    """

    characters: dict = {
        "letters_lower": string.ascii_lowercase,
        "letters_upper": string.ascii_uppercase,
        "digits": string.digits,
        "punctuation": string.punctuation,
    }

    @classmethod
    def generate_password(cls, length):
        """
        Creates password from randomly chosen characters, contains:
        At least 1 uppercase letter
        At least 1 lowercase letter
        At least 1 digit
        At least 1 special character
        :return str: Randomly created password as string
        """
        password: list = []
        for char_set in cls.characters.values():
            for _ in range(length // 4):
                password.append(random.choice(char_set))
        random.shuffle(password)
        return "".join(password)
