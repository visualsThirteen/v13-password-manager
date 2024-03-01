from models.mail_processor import MailProcessor


class CommonFunctions:

    @staticmethod
    def save_password(controller):
        """
        Verifies that password meets requirements, checks if entered password matches re-entered password,
        hashes and saves password to keyring, creates 2FA QR code and leads user to Set Up 2FA page.
        Shows error message if password is invalid.
        :param controller: Current controller class.
        """
        password = controller.frame.password_entry.get()
        re_password = controller.frame.re_pw_entry.get()
        if password == "Enter Password":
            controller.frame.pw_error_label.config(text="Please enter password", foreground="red")
        elif re_password == "Re-Enter Password":
            controller.frame.pw_error_label.config(text="Please re-enter password", foreground="red")
        elif not controller.security_engine.validate_password(password):
            controller.frame.pw_error_label.config(text="Password does not meet the requirements", foreground="red")
        elif password != re_password:
            controller.frame.pw_error_label.config(text="Passwords does not match", foreground="red")
        else:
            controller.security_engine.password = password
            del password
            del re_password
            controller.frame.pw_error_label.config(text="Password saved!", foreground="green")
            controller.frame.password_entry.set()
            controller.frame.re_pw_entry.set()
            del controller.security_engine.otp_key
            controller.security_engine.create_otp_key()
            controller.security_engine.initialize_totp()
            controller.app_controller.create_2fa_qr()
            controller.app_view.show_frame("setup_2fa")
        controller.frame.after(3000, lambda: controller.frame.pw_error_label.config(text=""))

    @staticmethod
    def send_token_email(controller, email):
        """
        Generates security token and sends to specified e-mail address, deletes token after
        amount of time specified in AppController class.
        :param controller: Current controller class.
        :param email: User e-mail.
        """
        token = controller.security_engine.generate_token()
        controller.app_controller.token = token
        if MailProcessor.send_token(email, token):
            controller.frame.error_label.config(text="E-mail sent", foreground="green")
        else:
            controller.frame.error_label.config(text="E-mail failed to send", foreground="red")
        controller.frame.after(3000, lambda: controller.frame.error_label.config(text=""))

    @staticmethod
    def check_security_token(controller) -> bool:
        """
        Verifies entered security token, if correct returns True, otherwise returns False.
        :param controller: Current controller class.
        :return bool: True or False.
        """
        entered_token = controller.frame.token_entry.get().strip()
        if entered_token == controller.app_controller.token:
            controller.app_controller.token = None
            controller.frame.error_label.config(text="Security code correct!", foreground="green")
            controller.frame.token_entry.set()
            controller.frame.after(3000, lambda: controller.frame.error_label.config(text=""))
            return True
        else:
            controller.frame.error_label.config(text="Invalid or expired security code", foreground="red")
            controller.frame.after(3000, lambda: controller.frame.error_label.config(text=""))
            return False
