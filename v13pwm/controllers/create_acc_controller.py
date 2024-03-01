from utilities.common_functions import CommonFunctions
from utilities.token_timer import TokenTimer
from models.mail_processor import MailProcessor


class CreateAccController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Create Account page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["create_acc"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Create Account page buttons to functions.
        """
        self.frame.send_email_btn.config(command=self.send_email_pressed)
        self.frame.submit_btn.config(command=self.submit_pressed)

    def send_email_pressed(self):
        """
        Checks if user entered e-mail address is valid, if valid generates and sends security token to
        entered e-mail address, otherwise shows error message.
        """
        email = self.frame.email_entry.get()
        msg = MailProcessor.validate(email)

        if email == "Enter E-mail address":
            self.frame.error_label.config(text="Please enter email address", foreground="red")
        elif msg is not None:
            self.frame.error_label.config(text=msg, foreground="red")
        else:
            self.app_controller.user_email = email
            CommonFunctions.send_token_email(self, email)
            TokenTimer.set_timer(self, self.app_controller.SECURITY_TOKEN_EXPIRE)
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def submit_pressed(self):
        """
        Checks if entered security token is valid, if valid leads user to Create Password page, otherwise
        shows error message.
        """
        if CommonFunctions.check_security_token(self):
            self.security_engine.user_email = self.app_controller.user_email
            self.app_controller.user_email = None
            self.frame.email_entry.set()
            self.security_engine.registration_complete = False
            self.app_view.show_frame("create_pw")
