import tkinter as tk
import ttkbootstrap as ttkb
import pyautogui
import sys
from PIL import Image, ImageTk
from view import AppView
from password_generator import PasswordGenerator
from mail_processor import MailProcessor
from security_engine import SecurityEngine
from data_processor import DataProcessor


class AppController:

    # Time in milliseconds after user is logged out.
    LOG_OUT_AFTER: int = 1000 * 60 * 5

    # Time in seconds after security token expires.
    SECURITY_TOKEN_EXPIRE: int = 60

    def __init__(self, view: AppView, security_engine: SecurityEngine):
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


class MainPageController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Main page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["main_page"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Main page buttons to functions.
        """
        self.frame.app_combox.config(
            postcommand=lambda: self.frame.app_combox.config(
                values=DataProcessor.get_all_apps()
            )
        )
        self.frame.settings_btn.config(command=lambda: self.app_view.show_frame("settings"))
        self.frame.gen_password_btn.config(command=self.gen_pw_pressed)
        self.frame.add_btn.config(command=self.add_pressed)
        self.frame.search_btn.config(command=self.search_pressed)
        self.frame.logout_btn.config(command=self.logout_pressed)

    def show_all_apps(self):
        """
        Populates combox with all apps in database.
        """
        self.frame.app_combox.config(values=lambda: DataProcessor.get_all_apps())

    def gen_pw_pressed(self):
        """
        Generates password, inserts it in password_entry box and copies password to clipboard.
        """
        password = PasswordGenerator.generate_password(self.app_controller.password_length)
        self.frame.password_entry.config(foreground="white")
        self.frame.password_entry.delete(0, tk.END)
        self.frame.password_entry.insert(0, string=password)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(password)

    def add_pressed(self):
        """
        Checks if all required fields are filled, if not, gives user error message.
        Asks user for approval to save credentials, if credentials exists for particular app, aks if
        user wants to update these credentials, if approved, saves details to database clears widgets,
        and gives feedback to user.
        """
        app = self.frame.app_combox.get().strip().lower()
        username = self.frame.username_entry.get().strip().lower()
        password = self.frame.password_entry.get()
        encrypted_password = self.security_engine.encrypt(password)
        if not app:
            self.frame.error_label.config(text="App / Web field is empty!", foreground="red")
        elif not username:
            self.frame.error_label.config(text="Username field is empty!", foreground="red")
        elif not password:
            self.frame.error_label.config(text="Password field is empty!", foreground="red")
        elif self.frame.should_save() == "Yes":
            if DataProcessor.search_record(app):
                if self.frame.should_replace(app) == "No":
                    self.frame.app_combox.delete(0, tk.END)
                    self.frame.username_entry.set()
                    self.frame.password_entry.set()
                    return
                else:
                    DataProcessor.update_record(app, username, encrypted_password)
            else:
                DataProcessor.insert_record(app, username, encrypted_password)
            self.frame.app_combox.delete(0, tk.END)
            self.frame.username_entry.set()
            self.frame.password_entry.set()
            self.frame.error_label.config(text="Data saved successfully!", foreground="green")
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def search_pressed(self):
        """
        Searches for credentials associated with entered app, in case app field is empty or credentials not found
        shows error message to user. If credentials are found, inserts username in
        username_entry box and password to password_entry box, copies password to clipboard and gives
        feedback to user.
        """
        app = self.frame.app_combox.get().strip().lower()
        if not app:
            self.frame.error_label.config(text="App / Web field is empty!", foreground="red")
        else:
            content = DataProcessor.search_record(app)
            if content:
                username, password = content
                password = self.security_engine.decrypt(password)
                self.frame.username_entry.delete(0, tk.END)
                self.frame.username_entry.insert(0, username)
                self.frame.password_entry.delete(0, tk.END)
                self.frame.password_entry.insert(0, password)
                self.frame.clipboard_clear()
                self.frame.clipboard_append(password)
                self.frame.error_label.config(text="Data retrieved successfully!", foreground="green")
            else:
                self.frame.error_label.config(text="Nothing was found!", foreground="red")
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def logout_pressed(self):
        """
        Clears widgets and leads user to Login page.
        """
        self.app_view.show_frame("login")
        self.frame.app_combox.delete(0, tk.END)
        self.frame.username_entry.set()
        self.frame.password_entry.set()


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


class CreatePwController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Create Password page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["create_pw"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Create Password page buttons to functions.
        """
        self.frame.save_btn.config(command=lambda: CommonFunctions.save_password(self))


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


class SettingsController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Settings page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["settings"]
        self.security_engine = app_controller.security_engine

        self.selected_theme = ttkb.StringVar(None, self.app_controller.theme_name)
        self.selected_pw_length = ttkb.IntVar(None, self.app_controller.password_length)

        self._bind()

        self.frame.password_meter.amountusedvar.trace("w", self.upd_pw_length)

    def _bind(self):
        """
        Binds Settings page buttons to functions.
        """
        self.frame.back_btn.config(command=lambda: self.app_view.show_frame("main_page"))
        self.frame.cyborg_theme_btn.config(
            value="cyborg",
            variable=self.selected_theme,
            command=self.change_theme
        )
        self.frame.morph_theme_btn.config(
            value="morph",
            variable=self.selected_theme,
            command=self.change_theme
        )
        self.frame.vapor_theme_btn.config(
            value="vapor",
            variable=self.selected_theme,
            command=self.change_theme
        )
        self.frame.solar_theme_btn.config(
            value="solar",
            variable=self.selected_theme,
            command=self.change_theme
        )
        self.frame.password_meter.configure(amountused=self.selected_pw_length.get())
        self.frame.change_pw_btn.config(command=self.change_pw_pressed)
        self.frame.delete_acc_btn.config(command=self.delete_acc_pressed)

    def change_pw_pressed(self):
        """
        Sets reference to previous frame and leads user to Forgot Password page.
        """
        self.app_controller.previous_frame = "settings"
        self.app_view.show_frame("forgot_pw")

    def upd_pw_length(self, *args):
        """
        Sets password length using ttkbootstrap meter widget.
        """
        password_length = self.frame.password_meter.amountusedvar.get()
        self.app_controller.set_pw_length(password_length)

    def change_theme(self):
        """
        Changes app theme.
        """
        selected_theme = self.selected_theme.get()
        self.app_controller.set_theme(selected_theme)

    def delete_acc_pressed(self):
        """
        Shows user should_delete messagebox, if answer is "delete", deletes account and wipes all data,
        gives feedback to user and exits app.
        """
        if self.frame.should_delete() == "Delete Account":
            self.security_engine.delete_secrets()
            self.security_engine.delete_qr()
            DataProcessor.delete_table()
            DataProcessor.delete_preferences()
            self.frame.account_deleted()
            sys.exit()


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


class TokenTimer:
    """
    Encapsulates logic for countdown mechanism.
    """
    controller = None
    time = None
    security_token_timer = None

    @classmethod
    def set_timer(cls, controller, time: int):
        """
        Takes current controller class and time in seconds from which to start countdown,
        starts timer.
        :param controller: Current controller class.
        :param int time: Time in seconds.
        """
        cls.time = time
        cls.controller = controller
        cls.start_timer()

    @classmethod
    def start_timer(cls):
        """
        If timer exists, cancels it and starts new timer.
        """
        if cls.security_token_timer is not None:
            cls.controller.frame.after_cancel(cls.security_token_timer)
        cls.timer_logic()

    @classmethod
    def timer_logic(cls):
        """
        Displays time in seconds until security token expires, if time left is less than 0, displays message to
        user and deletes security token. If time left is greater than 0, calls countdown function.
        """
        if cls.time < 0:
            cls.controller.frame.after_cancel(cls.security_token_timer)
            cls.controller.frame.timer_label.config(text="Security token expired!")
            cls.controller.app_controller.delete_token()
        else:
            cls.controller.frame.timer_label.config(
                text=f"Security token will expire after: {cls.time} seconds."
            )
            cls.time -= 1
            cls.countdown()

    @classmethod
    def countdown(cls):
        """
        Calls timer_logic function after 1 second.
        """
        timer = cls.controller.frame.after(1000, cls.timer_logic)
        cls.security_token_timer = timer
