from email_validator import validate_email, EmailNotValidError
import smtplib
import os


class MailProcessor:
    """
    Encapsulates logic related to sending and validating e-mails.
    """

    EMAIL = os.environ["EMAIL"]
    PASSWORD = os.environ["PASSWORD"]
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    @staticmethod
    def validate(email: str) -> str or None:
        """
        Takes email address, checks if syntax and domain name are correct.
        :param str email: E-mail address to validate
        :return None or str: None if email is valid, otherwise returns user-friendly error message as string.
        """
        try:
            validate_email(email.strip(), check_deliverability=True)
        except EmailNotValidError as error:
            return str(error)
        else:
            return None

    @staticmethod
    def send_token(email: str, token: str) -> bool:
        """
        Takes recipient email address and token to send, sends e-mail.
        :param str email: Recipients e-mail address
        :param str token: Token to send
        :return bool: True if operation was successful, False and prints error message to console if operation failed
        """
        try:
            with smtplib.SMTP(MailProcessor.SMTP_SERVER, MailProcessor.SMTP_PORT) as connection:
                connection.starttls()
                connection.login(user=MailProcessor.EMAIL, password=MailProcessor.PASSWORD)
                connection.sendmail(
                    from_addr=MailProcessor.EMAIL,
                    to_addrs=email,
                    msg=f"Subject: V13 Password Manager authentication token\n\n"
                        f"Your authentication token - {token}"
                )
                return True
        except smtplib.SMTPAuthenticationError:
            print("SMTP authentication error: Invalid username or password.")
            return False
        except smtplib.SMTPException as smtp_error:
            print(f"SMTP error: {smtp_error}")
            return False
        except OSError as os_error:
            print(f"OS error: {os_error}")
            return False
        except KeyError as key_error:
            print(f"Key error {key_error}")
            return False
