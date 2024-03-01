from v13pwm.models.mail_processor import MailProcessor


def test_valid_emails():
    emails = [
        " test@gmail.com ",
        "test@gmail.com",
        "test.test@yahoo.com",
        "test123@outlook.com",
        "123test@gmail.com",
        "test_test@gmail.com",
        "test.test@yahoo.com"
    ]

    for email in emails:
        assert MailProcessor.validate(email) is None


def test_invalid_emails():
    emails = [
        "",
        " ",
        "test",
        "test@",
        "test@gmail"
        "test @gmail.com",
        "test@@gmail.com",
        "test@ gmail.com",
        "test@gmail. com",
        "test@gmail..com",
        "test@gmail.con",
        "test@yahoo.cc",
        "test@hotmail.hh"
    ]

    for email in emails:
        assert MailProcessor.validate(email) is not None
