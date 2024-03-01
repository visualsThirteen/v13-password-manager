class LoginController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Login page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["login"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Login page buttons to functions.
        """
        self.frame.login_btn.config(command=self.login_pressed)
        self.frame.forgot_pw_btn.config(command=self.forgot_pw_pressed)
        self.frame.reset_otp_btn.config(command=self.reset_otp_pressed)

    def login_pressed(self):
        """
        Checks if entered password and OTP are correct, if correct leads user to Main page, otherwise
        shows error message.
        """
        password = self.frame.password_entry.get()
        otp_entered = self.frame.otp_entry.get().strip()
        if self.security_engine.check_password(password):
            del password
            self.frame.password_entry.set()
            if self.security_engine.verify_otp(otp_entered):
                self.frame.otp_entry.set()
                self.app_view.show_frame("main_page")
            else:
                self.frame.password_entry.set()
                self.frame.otp_entry.set()
                self.frame.error_label.config(text="Invalid OTP", foreground="red")
        else:
            self.frame.password_entry.set()
            self.frame.otp_entry.set()
            self.frame.error_label.config(text="Invalid password", foreground="red")
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def forgot_pw_pressed(self):
        """
        Clears widgets and leads user to Login page. Adds reference to previous frame.
        """
        self.frame.password_entry.set()
        self.frame.otp_entry.set()
        self.app_controller.previous_frame = "login"
        self.app_view.show_frame("forgot_pw")

    def reset_otp_pressed(self):
        """
        Clears widgets and leads user to Reset 2FA page. Adds reference to previous frame.
        """
        self.frame.password_entry.set()
        self.frame.otp_entry.set()
        self.app_controller.previous_frame = "login"
        self.app_view.show_frame("reset_2fa")
