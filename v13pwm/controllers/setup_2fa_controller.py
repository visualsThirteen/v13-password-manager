class SetUp2FAController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Set Up 2FA page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["setup_2fa"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Set Up 2FA buttons to functions.
        """
        self.frame.submit_btn.config(command=self.submit_pressed)

    def submit_pressed(self):
        """
        Verifies entered OTP, if correct, marks registration as complete and leads user to Login page.
        """
        otp_entered = self.frame.otp_entry.get().strip()
        self.frame.otp_entry.set()
        if self.security_engine.verify_otp(otp_entered):
            self.security_engine.registration_complete = True
            self.app_view.show_frame("login")
        else:
            self.frame.error_label.config(
                text="Invalid or expired OTP!",
                foreground="red"
            )
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))
