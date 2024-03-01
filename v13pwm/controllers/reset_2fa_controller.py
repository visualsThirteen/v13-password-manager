from utilities.common_functions import CommonFunctions
from utilities.token_timer import TokenTimer


class Reset2FAController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Reset 2FA page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["reset_2fa"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Reset 2FA page buttons to functions.
        """
        self.frame.back_btn.config(command=lambda: self.app_view.show_frame(self.app_controller.previous_frame))
        self.frame.send_email_btn.config(command=self.send_email_pressed)
        self.frame.reset_otp_btn.config(command=self.reset_pressed)

    def send_email_pressed(self):
        """
        Generates security token and sends to registered e-mail.
        """
        email = self.security_engine.user_email
        CommonFunctions.send_token_email(self, email)
        TokenTimer.set_timer(self, self.app_controller.SECURITY_TOKEN_EXPIRE)

    def reset_pressed(self):
        """
        Verifies entered security token, if correct, leads user to Set Up 2FA page, otherwise shows
        error message.
        """
        if CommonFunctions.check_security_token(self):
            del self.security_engine.otp_key
            self.security_engine.create_otp_key()
            self.security_engine.initialize_totp()
            self.app_controller.create_2fa_qr()
            self.app_view.show_frame("setup_2fa")
        self.frame.token_entry.set()
