from cryptography.fernet import Fernet
import bcrypt
import keyring
from keyring.errors import PasswordDeleteError
import random
import string
import re
import pyotp
import qrcode
import atexit
import os


class SecurityEngine:
    """
    Encapsulates all logic related to security.
    """
    def __init__(self):
        self._client = "password manager"
        self._crypt_engine = None
        self._totp = None
        self.registration_complete = True
        atexit.register(self.cleanup_on_exit)

    def cleanup_on_exit(self):
        """
        Deletes all secrets from keyring if registration was not completed.
        """
        if not self.registration_complete:
            self.delete_secrets()

    def initialize_crypt_engine(self):
        """
        Initializes or re-initializes Fernet with new or existing key.
        """
        del self._crypt_engine
        self._crypt_engine = Fernet(self.key)

    def initialize_totp(self):
        """
        Initializes or re-initializes TOTP with new or existing key.
        """
        del self._totp
        self._totp = pyotp.TOTP(self.otp_key)

    @property
    def crypt_engine(self) -> Fernet:
        return self._crypt_engine

    @property
    def totp(self):
        return self._totp

    @property
    def client(self) -> str:
        return self._client

    @property
    def otp_key(self):
        return keyring.get_password(self.client, "otp_key")

    def create_otp_key(self):
        """
        Generates new OTP key and saves to keyring.
        """
        otp_key = pyotp.random_base32()
        keyring.set_password(self.client, "otp_key", otp_key)

    @otp_key.deleter
    def otp_key(self):
        """
        Deletes OTP key from keyring.
        """
        keyring.delete_password(self.client, "otp_key")

    @property
    def key(self) -> str or None:
        return keyring.get_password(self.client, "key")

    def create_key(self):
        """
        Generates new Fernet key and saves to keyring.
        """
        key = Fernet.generate_key().decode()
        keyring.set_password(self.client, "key", key)

    @key.deleter
    def key(self):
        """
        Deletes Fernet key from keyring.
        """
        keyring.delete_password(self.client, "key")

    @property
    def salt(self) -> str or None:
        return keyring.get_password(self.client, "salt")

    def create_salt(self):
        """
        Generates salt and saves to keyring.
        """
        salt = bcrypt.gensalt().decode()
        keyring.set_password(self.client, "salt", salt)

    @salt.deleter
    def salt(self):
        """
        Deletes salt from keyring.
        """
        keyring.delete_password(self.client, "salt")

    @property
    def password(self) -> str or None:
        return keyring.get_password(self.client, "password")

    @password.setter
    def password(self, password: str):
        """
        Takes password, hashes it and adds to keyring.
        :param str password: Password as string.
        """
        hashed_password = self.hash_password(password)
        keyring.set_password(self.client, "password", hashed_password)

    @password.deleter
    def password(self):
        """
        Deletes password from keyring.
        """
        keyring.delete_password(self.client, "password")

    @property
    def user_email(self) -> str or None:
        return keyring.get_password(self.client, "user_email")

    @user_email.setter
    def user_email(self, email: str):
        """
        Takes user e-mail and saves to keyring.
        :param str email: User e-mail as string.
        """
        keyring.set_password(self.client, "user_email", email)

    @user_email.deleter
    def user_email(self):
        """
        Deletes user e-mail from keyring.
        """
        keyring.delete_password(self.client, "user_email")

    def encrypt(self, password: str) -> str:
        """
        Takes password and encrypts it using symmetric encryption.
        :param str password: Password to encrypt
        :return: Encrypted password
        """
        return self.crypt_engine.encrypt(password.encode()).decode()

    def decrypt(self, password: str) -> str:
        """
        Takes encrypted password, decrypts and returns as string.
        :param str password: Encrypted password
        :return str: Decrypted password
        """
        return self.crypt_engine.decrypt(password.encode()).decode()

    def hash_password(self, password: str) -> str:
        """
        Adds salt and hashes password.
        :param str password: Password to be hashed
        :return str: Hashed password
        """
        return bcrypt.hashpw(password.encode(), self.salt.encode()).decode()

    def check_password(self, password: str) -> bool:
        """
        Takes password, hashes it and compares to saved user password.
        :param str password: Password to be compared
        :return bool: True if passwords are equal, otherwise False
        """
        entered_pw = self.hash_password(password)
        user_password = self.password
        return entered_pw == user_password

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Takes password and checks if password meets following requirements:
        Password is 8 - 72 characters long
        Contains at least 1 lowercase letter
        Contains at least 1 uppercase letter
        Contains at least 1 digit
        Contains at least 1 special symbol
        :param str password: Password to be validated
        :return bool: True if password meets all requirements, otherwise False
        """
        if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[#?!@$%^&*-]).{8,}$", password):
            return True
        return False

    @staticmethod
    def generate_token() -> str:
        """
        Generates random 6 digit token.
        :return str: Token as string
        """
        return "".join([random.choice(string.digits) for _ in range(6)])

    def create_otp_qr(self):
        """
        Generates uri and creates qr code image from it. Saves as qr.png
        """
        uri = pyotp.totp.TOTP(self.otp_key).provisioning_uri(
            name=self.user_email,
            issuer_name=self.client
        )
        qrcode.make(uri).save("pwm_data/qr.png")

    def verify_otp(self, otp: str) -> bool:
        """
        Takes entered OTP and verifies it. Returns True or False.
        :param otp: Entered OTP.
        :return bool: True or False.
        """
        return self._totp.verify(otp)

    def initialize_new_acc(self):
        """
        Encapsulates functions that will be called when new account is created.
        """
        self.create_salt()
        self.create_key()
        self.create_otp_key()
        self.initialize_crypt_engine()
        self.initialize_totp()

    def load_acc(self):
        """
        Encapsulates functions that will be called when existing account is loaded.
        """
        self.initialize_crypt_engine()
        self.initialize_totp()

    @staticmethod
    def delete_qr():
        """
        Deletes qr.png if it exists in directory.
        """
        if os.path.exists("pwm_data/qr.png"):
            os.remove("pwm_data/qr.png")

    def delete_secrets(self):
        """
        Deletes all saved user details from keyring.
        """
        try:
            del self.key
        except PasswordDeleteError:
            pass
        try:
            del self.salt
        except PasswordDeleteError:
            pass
        try:
            del self.user_email
        except PasswordDeleteError:
            pass
        try:
            del self.password
        except PasswordDeleteError:
            pass
        try:
            del self.otp_key
        except PasswordDeleteError:
            pass
