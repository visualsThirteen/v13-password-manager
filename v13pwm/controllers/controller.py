import ttkbootstrap as ttkb
import pyautogui
from PIL import Image, ImageTk
from models.data_processor import DataProcessor
from .login_controller import LoginController
from .create_acc_controller import CreateAccController
from .create_pw_controller import CreatePwController
from .forgot_pw_controller import ForgotPwController
from .setup_2fa_controller import SetUp2FAController
from .reset_2fa_controller import Reset2FAController
from .settings_controller import SettingsController
from .main_page_controller import MainPageController


class AppController:

    # Time in milliseconds after user is logged out.
    LOG_OUT_AFTER: int = 1000 * 60 * 5

    # Time in seconds after security token expires.
    SECURITY_TOKEN_EXPIRE: int = 60

    def __init__(self, view, security_engine):
        """
        Initializes app controller.
        :param view: AppView class.
        :param security_engine: SecurityEngine class.
        """
        self.app_view = view
        self.security_engine = security_engine

        self.previous_frame: str or None = None
        self.token: str or None = None
        self.user_email: str or None = None

        preferences = DataProcessor.load_preferences()
        if preferences is not None:
            self.password_length: int = preferences["pw_length"]
            self.theme_name: str = preferences["theme"]
        else:
            self.password_length: int = 20
            self.theme_name: str = "cyborg"

        self.login_controller = LoginController(app_controller=self, app_view=self.app_view)
        self.create_acc_controller = CreateAccController(app_controller=self, app_view=self.app_view)
        self.create_pw_controller = CreatePwController(app_controller=self, app_view=self.app_view)
        self.forgot_pw_controller = ForgotPwController(app_controller=self, app_view=self.app_view)
        self.setup_2fa_controller = SetUp2FAController(app_controller=self, app_view=self.app_view)
        self.reset_2fa_controller = Reset2FAController(app_controller=self, app_view=self.app_view)
        self.settings_controller = SettingsController(app_controller=self, app_view=self.app_view)
        self.main_page_controller = MainPageController(app_controller=self, app_view=self.app_view)

        self.cursor_pos: tuple or None = None
        self.afk_check()
        self.set_theme(self.theme_name)
        self.set_pw_length(self.password_length)
        self.set_starting_page()

    def delete_token(self):
        """
        Resets token value to None.
        """
        self.token = None

    def detect_afk(self):
        """
        Gets cursor position and compares to last cursor position, if cursor position is the same and
        user is logged in, logs out user, otherwise calls function to re-check after specified amount of time.
        """
        pos: tuple = pyautogui.position()
        if self.app_view.current_frame == "main_page" or self.app_view.current_frame == "settings":
            if pos == self.cursor_pos:
                self.app_view.show_frame("login")
            else:
                self.cursor_pos = pos
        self.afk_check()

    def afk_check(self):
        """
        Calls AFK detection after specified amount of time.
        """
        self.app_view.after(self.LOG_OUT_AFTER, self.detect_afk)

    def create_2fa_qr(self):
        """
        Generates 2FA QR code image and sets it to corresponding widget in Set Up 2FA page.
        """
        self.security_engine.create_otp_qr()
        img = Image.open("pwm_data/qr.png").resize((300, 300))
        qr = ImageTk.PhotoImage(img)
        self.app_view.initialized_frames["setup_2fa"].qr_label.config(image=qr)
        self.app_view.initialized_frames["setup_2fa"].qr_label.image = qr

    def set_starting_page(self):
        """
        Checks if user password exists, if not initializes new account and leads user to Create Account page, if
        password exists, initializes account with saved keys and leads user to Login page.
        """
        if self.security_engine.password is None:
            DataProcessor.create_database()
            self.security_engine.initialize_new_acc()
            self.app_view.show_frame("create_acc")
        else:
            self.security_engine.load_acc()
            self.app_view.show_frame("login")

    def set_theme(self, theme: str):
        """
        Takes ttkbootstrap theme name and sets app theme, saves chosen theme to user preferences.
        :param str theme: ttkbootstrap theme name.
        """
        self.app_view.theme = ttkb.Style(theme)
        self.theme_name = theme
        preferences = {
            "theme": theme
        }
        DataProcessor.save_preferences(preferences)

    def set_pw_length(self, length: int):
        """
        Takes length as integer and sets user preferred password length to its value and saves to preferences.
        Password length can not be less than 4 and must be even number, if odd number given, function will add 1
        to it, all numbers which are less than 4 will be set to 4.
        :param int length: Integer which is greater than 4 and even.
        """
        length = 4 if length < 4 else length
        self.password_length = length if length % 2 == 0 else length + 1
        preferences = {
            "pw_length": length
        }
        DataProcessor.save_preferences(preferences)
