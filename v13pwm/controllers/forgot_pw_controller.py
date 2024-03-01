from utilities.common_functions import CommonFunctions
from utilities.token_timer import TokenTimer


class ForgotPwController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Forgot Password page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["forgot_pw"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Forgot Password page buttons to functions.
        """
        self.frame.back_btn.config(command=self.back_pressed)
        self.frame.send_email_btn.config(command=self.send_email_pressed)
        self.frame.submit_btn.config(command=self.submit_pressed)
        self.frame.save_btn.config(command=self.save_pressed)

    def send_email_pressed(self):
        """
        Generates security token and sends to registered e-mail address.
        """
        email = self.security_engine.user_email
        CommonFunctions.send_token_email(self, email)
        TokenTimer.set_timer(self, self.app_controller.SECURITY_TOKEN_EXPIRE)

    def submit_pressed(self):
        """
        Verifies entered security token, if correct enables password entry fields, otherwise shows error message.
        """
        if CommonFunctions.check_security_token(self):
            self.enable_pw_entry()
        self.frame.token_entry.set()

    def save_pressed(self):
        """
        Calls save_password function and disables password entry fields.
        """
        CommonFunctions.save_password(self)
        self.disable_pw_entry()

    def back_pressed(self):
        """
        Leads user to previous frame, disables password entry fields and clears widgets.
        """
        self.app_view.show_frame(self.app_controller.previous_frame)
        self.frame.token_entry.set()
        self.disable_pw_entry()

    def disable_pw_entry(self):
        """
        Disables all fields related to password reset.
        """
        self.frame.password_entry.set()
        self.frame.re_pw_entry.set()
        self.frame.password_entry.config(state="disabled")
        self.frame.re_pw_entry.config(state="disabled")
        self.frame.save_btn.config(state="disabled")

    def enable_pw_entry(self):
        """
        Enables all fields related to password reset.
        """
        self.frame.password_entry.config(state="enabled")
        self.frame.re_pw_entry.config(state="enabled")
        self.frame.save_btn.config(state="enabled")
