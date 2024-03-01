from v13pwm.models.security_engine import SecurityEngine


class TestSecurityEngine:

    def setup_method(self, method):
        self.security_engine = SecurityEngine()
        self.security_engine._client = "test"
        self.security_engine.initialize_new_acc()

    def teardown_method(self, method):
        self.security_engine.delete_secrets()
        del self.security_engine

    def test_encrypt_decrypt(self):
        passwords = ["test", "Test123", "#!@123TEST"]
        for password in passwords:

            encrypted_password = self.security_engine.encrypt(password)
            assert encrypted_password != password

            decrypted_password = self.security_engine.decrypt(encrypted_password)
            assert decrypted_password == password

    def test_pw_hashing(self):
        passwords = ["test", "Test123", "#!@Test123"]
        for password in passwords:
            hashed_password = self.security_engine.hash_password(password)
            assert hashed_password != password

    def test_check_password(self):
        self.security_engine.password = "test"
        assert self.security_engine.check_password("test") is True

        invalid_password = ["test.", "Test", "123", ".test", "TEST"]
        for password in invalid_password:
            assert self.security_engine.check_password(password) is False

    def test_validate_password(self):
        valid_passwords = ["Password123!", "Test123!", "1TEST!test", "!1testTest"]
        for password in valid_passwords:
            assert self.security_engine.validate_password(password) is True

        invalid_passwords = ["", "test", "password", "Password", "Password!", "Password1", "password1!", "!1PASSWORD"]
        for password in invalid_passwords:
            assert self.security_engine.validate_password(password) is False
