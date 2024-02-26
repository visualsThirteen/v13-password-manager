import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox
from PIL import Image


class AppView(ttkb.Window):
    """
    Initializes app window.
    """
    Image.CUBIC = Image.BICUBIC
    SMALL_FONT: tuple = ("Ariel", 12)
    FONT: tuple = ("Ariel", 15)
    TITLE_FONT: tuple = ("Ariel", 30, "bold")
    PRIMARY_COLOR: str = "#38b6ff"
    # Time in seconds after security token expires
    SECURITY_TOKEN_EXPIRE = 60

    def __init__(self):
        super().__init__()

        self.geometry("550x760")
        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.iconphoto(True, self.logo)
        self.resizable(False, False)
        self.config(padx=50, pady=50)
        self.title("V13 Password Manager")
        self.theme = ttkb.Style("cyborg")

        self.container = ttkb.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.initialized_frames: dict = {}

        self.frames: dict = {
            "login": LoginView,
            "create_acc": CreateAccView,
            "create_pw": CreatePwView,
            "forgot_pw": ForgotPwView,
            "setup_2fa": SetUp2FAView,
            "reset_2fa": Reset2FAView,
            "settings": SettingsView,
            "main_page": MainPageView
        }

        self.current_frame: str or None = None
        self.initialize_frames(self.frames)

    def initialize_frames(self, frames: dict):
        """
        Takes dictionary where frame name is a key and frame a value. Initializes frame by passing in parent frame
        and adds to initialized_frames dictionary preserving frame name as key.
        :param dict frames: Dictionary containing frame names as keys and frame objects as values.
        """
        for key, value in frames.items():
            frame = value(self.container)
            self.initialized_frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name: str):
        """
        Takes frame name and shows specified frame.
        :param str frame_name: Frame name.
        """
        self.current_frame = frame_name
        frame_to_show = self.initialized_frames[frame_name]
        frame_to_show.tkraise()


class MainPageView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Main Page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.settings_btn = ttkb.Button(
            self,
            text="S E T T I N G S",
            width=10,
            style="primary-outline"
        )
        self.settings_btn.grid(row=0, column=2, pady=(0, 0), sticky="n")

        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.logo_label = ttkb.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=3)

        self.error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            foreground="red"
        )
        self.error_label.grid(row=1, column=1, pady=(0, 8), padx=5)

        self.app_label = ttkb.Label(
            self,
            text="App / Web:",
            font=AppView.FONT,
            foreground=AppView.PRIMARY_COLOR
        )
        self.app_label.grid(row=3, column=0, pady=8, padx=(0, 5))

        self.app_combox = ttkb.Combobox(self, width=23)
        self.app_combox.grid(row=3, column=1)
        self.app_combox.focus()
        ToolTip(
            self.app_combox,
            text="Type to add or search app or choose from saved apps.",
            bootstyle="primary"
        )

        self.username_label = ttkb.Label(
            self,
            text="Username:",
            font=AppView.FONT,
            foreground=AppView.PRIMARY_COLOR
        )
        self.username_label.grid(row=4, column=0, pady=8, padx=(0, 5))

        self.username_entry = EntryMod(
            self,
            box_width=34,
            placeholder=""
        )
        self.username_entry.grid(row=4, column=1, columnspan=2)
        ToolTip(
            self.username_entry,
            text="Type username.",
            bootstyle="primary"
        )

        self.password_label = ttkb.Label(
            self,
            text="Password:",
            font=AppView.FONT,
            foreground=AppView.PRIMARY_COLOR
        )
        self.password_label.grid(row=5, column=0, pady=8, padx=(0, 5))

        self.password_entry = EntryMod(
            self,
            box_width=22,
            placeholder=""
        )
        self.password_entry.grid(row=5, column=1)
        ToolTip(
            self.password_entry,
            text="Type or generate safe password.",
            bootstyle="primary"
        )

        self.gen_password_btn = ttkb.Button(
            self,
            text="Generate",
            width=10,
            style="primary-outline"
        )
        self.gen_password_btn.grid(row=5, column=2)

        self.add_btn = ttkb.Button(
            self,
            text="Add",
            width=37,
            style="success"
        )
        self.add_btn.grid(row=6, column=1, columnspan=2, pady=3)

        self.search_btn = ttkb.Button(
            self, text="Search",
            width=10,
            style="primary-outline"
        )
        self.search_btn.grid(row=3, column=2)

        self.logout_btn = ttkb.Button(
            self,
            text="Log Out",
            width=37,
            style="primary-outline"
        )
        self.logout_btn.grid(row=7, column=1, columnspan=2, pady=(30, 0))

    def should_save(self) -> str:
        """
        Shows messagebox with question.
        :return str: "Yes" or "No"
        """
        return Messagebox.show_question(
            "Do you want to save these credentials?",
            parent=self
        )

    def should_replace(self, app: str) -> str:
        """
        Shows messagebox with question.
        :param str app: App to be updated.
        :return: "Update" or "No"
        """
        return Messagebox.show_question(
            f"Credentials for {app} already exists!\n"
            f"Do you want to update these credentials?",
            buttons=["No:secondary", "Update:primary"],
            parent=self
        )


class LoginView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Login page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.logo_label = ttkb.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, pady=(0, 30))

        self.title_label = ttkb.Label(
            self,
            text="Login",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground=AppView.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.password_label = ttkb.Label(
            self,
            text="Enter Master Password to access your passwords",
            justify="center",
            font=AppView.FONT
        )
        self.password_label.grid(row=2, column=0, pady=8, padx=5)

        self.error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            justify="center",
            foreground="red"
        )
        self.error_label.grid(row=3, column=0, pady=8, padx=5)

        self.password_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter Master password",
            show="*"
        )
        self.password_entry.grid(row=4, column=0)
        ToolTip(
            self.password_entry,
            text="Enter Master Password",
            bootstyle="primary"
        )

        self.otp_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter OTP",
            show=""
        )
        self.otp_entry.grid(row=5, column=0, pady=(5, 0))
        ToolTip(
            self.otp_entry,
            text="Enter One Time Password from authenticator app",
            bootstyle="primary"
        )

        self.login_btn = ttkb.Button(
            self,
            text="Login",
            width=37
        )
        self.login_btn.grid(row=6, column=0, pady=5)

        self.forgot_pw_btn = ttkb.Button(
            self,
            text="Forgot password",
            width=37,
            style="primary-outline"
        )
        self.forgot_pw_btn.grid(row=7, column=0)

        self.reset_otp_btn = ttkb.Button(
            self,
            text="Reset 2FA",
            width=37,
            style="primary-outline"
        )
        self.reset_otp_btn.grid(row=8, column=0, pady=5)


class CreateAccView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Create Account page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.logo_label = ttkb.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        self.title_label = ttkb.Label(
            self,
            text="Create Account",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.info_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            justify="center",
            text="We will send security code to your e-mail address, "
                 "this e-mail address will be required in order to reset password."
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            foreground=AppView.PRIMARY_COLOR,
            justify="center"
        )
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            foreground="red",
            justify="center",
            wraplength=370
        )
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(5, 10))

        self.email_entry = EntryMod(
            self,
            box_width=22,
            placeholder="Enter E-mail address"
        )
        ToolTip(
            self.email_entry,
            text="Enter e-mail address.",
            bootstyle="primary"
        )
        self.email_entry.grid(row=5, column=0, pady=5, padx=(50, 5))

        self.send_email_btn = ttkb.Button(
            self,
            text="Send",
            width=10)
        self.send_email_btn.grid(row=5, column=1, pady=5, padx=(0, 50))

        self.token_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter received code"
        )
        ToolTip(
            self.token_entry,
            text="Enter received security code.",
            bootstyle="primary"
        )
        self.token_entry.grid(row=6, column=0, columnspan=2)

        self.submit_btn = ttkb.Button(
            self,
            text="Submit",
            width=37
        )
        self.submit_btn.grid(row=7, column=0, columnspan=2, pady=5)


class CreatePwView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Create Password page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.logo_label = ttkb.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, pady=(0, 30))

        self.title_label = ttkb.Label(
            self,
            text="Create Master Password",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.password_label = ttkb.Label(
            self,
            text="Password must be 8-72 characters long and must contain at least 1 uppercase letter,"
                 " 1 lowercase letter, 1 number and 1 special character",
            font=AppView.SMALL_FONT,
            justify="center",
            wraplength=350
        )
        self.password_label.grid(row=2, column=0, pady=8, padx=5)

        self.pw_error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            justify="center",
            wraplength=360
        )
        self.pw_error_label.grid(row=3, column=0)

        self.password_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter Password",
            show="*"
        )
        ToolTip(
            self.password_entry,
            text="Create Master Password.",
            bootstyle="primary"
        )
        self.password_entry.grid(row=4, column=0, pady=5)

        self.re_pw_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Re-Enter Password",
            show="*"
        )
        ToolTip(
            self.re_pw_entry,
            text="Re-type Master Password.",
            bootstyle="primary"
        )
        self.re_pw_entry.grid(row=5, column=0)

        self.save_btn = ttkb.Button(
            self,
            text="Save",
            width=37
        )
        self.save_btn.grid(row=6, column=0, pady=5)


class ForgotPwView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Forgot Password page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.back_btn = ttkb.Button(
            self,
            text="B A C K",
            width=5,
            style="primary-outline"
        )
        self.back_btn.grid(row=0, column=0, pady=(0, 0), sticky="nw")

        self.title_label = ttkb.Label(
            self,
            text="Reset Password",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 50))

        self.info_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            justify="center",
            text='Click "Send Security Code" button to send security code to your registered e-mail, '
                 'enter received code and click "Submit"'
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            foreground=AppView.PRIMARY_COLOR,
            justify="center"
        )
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        self.send_email_btn = ttkb.Button(
            self,
            text="Send Security Code",
            width=15,
            style="primary-outline",
        )
        self.send_email_btn.grid(row=4, column=0, columnspan=2, pady=(20, 0), ipady=10)

        self.error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            justify="center",
            wraplength=370
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.token_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter received code"
        )
        ToolTip(
            self.token_entry,
            text="Enter received security code.",
            bootstyle="primary"
        )
        self.token_entry.grid(row=6, column=0, columnspan=2)

        self.submit_btn = ttkb.Button(
            self,
            text="Submit",
            width=37
        )
        self.submit_btn.grid(row=7, column=0, columnspan=2, pady=5)

        seperator = ttkb.Separator(self, style="primary")
        seperator.grid(row=8, column=0, sticky="we", pady=40)

        self.password_label = ttkb.Label(
            self,
            text="Create new password",
            font=AppView.FONT,
            justify="center",
            wraplength=350
        )
        self.password_label.grid(row=9, column=0, pady=(0, 10))

        self.pw_error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            justify="center",
            wraplength=360
        )
        self.pw_error_label.grid(row=10, column=0)

        self.password_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter Password",
            show="*"
        )
        ToolTip(
            self.password_entry,
            text="Password must be 8-72 characters long and must contain at least 1 uppercase letter, "
                 "1 lowercase letter, 1 number and 1 special character",
            bootstyle="primary"
        )
        self.password_entry.grid(row=11, column=0, pady=5)
        self.password_entry.config(state="disabled")

        self.re_pw_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Re-Enter Password",
            show="*"
        )
        ToolTip(
            self.re_pw_entry,
            text="Re-enter password",
            bootstyle="primary"
        )
        self.re_pw_entry.grid(row=12, column=0)
        self.re_pw_entry.config(state="disabled")

        self.save_btn = ttkb.Button(
            self,
            text="Save",
            width=37
        )
        self.save_btn.grid(row=13, column=0, pady=5)
        self.save_btn.config(state="disabled")


class SetUp2FAView(ttkb.Frame):

    def __init__(self, master):
        """
        Displays Set Up 2FA page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.qr_label = ttkb.Label(self)
        self.qr_label.grid(row=0, column=0, pady=(0, 30))

        self.title_label = ttkb.Label(
            self,
            text="Set Up 2FA",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground=AppView.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.otp_label = ttkb.Label(
            self,
            text="Let's set up 2 factor authentication. "
                 "Open Google Authenticator app and scan QR code to add Password "
                 "Manager to your account",
            font=AppView.FONT,
            justify="center",
            wraplength=350
        )
        self.otp_label.grid(row=2, column=0, pady=8, padx=5)

        self.error_label = ttkb.Label(
            self,
            justify="center",
            font=AppView.SMALL_FONT,
        )
        self.error_label.grid(row=3, column=0, pady=8, padx=5)

        self.otp_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter OTP",
            show=""
        )
        ToolTip(
            self.otp_entry,
            text="Enter One Time Password from authenticator app.",
            bootstyle="primary"
        )
        self.otp_entry.grid(row=4, column=0)

        self.submit_btn = ttkb.Button(
            self,
            text="Submit",
            width=37
        )
        self.submit_btn.grid(row=5, column=0, pady=5)


class Reset2FAView(ttkb.Frame):

    def __init__(self, master: ttkb.Frame):
        """
        Displays Reset 2FA page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.back_btn = ttkb.Button(
            self,
            text="B A C K",
            width=5,
            style="primary-outline"
        )
        self.back_btn.grid(row=0, column=0, pady=(0, 0), sticky="nw")

        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.logo_label = ttkb.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        self.title_label = ttkb.Label(
            self,
            text="Reset 2FA",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        self.info_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            justify="center",
            text='Click "Send Security Code" button to send security code to your registered e-mail, '
                 'enter received code and click "Reset 2FA"'
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            wraplength=350,
            foreground=AppView.PRIMARY_COLOR,
            justify="center"
        )
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))

        self.send_email_btn = ttkb.Button(
            self,
            text="Send Security Code",
            width=15,
            style="primary-outline",
        )
        self.send_email_btn.grid(row=4, column=0, columnspan=2, pady=(20, 0), ipady=10)

        self.error_label = ttkb.Label(
            self,
            font=AppView.SMALL_FONT,
            foreground="red",
            justify="center",
            wraplength=370
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.token_entry = EntryMod(
            self,
            box_width=34,
            placeholder="Enter received code"
        )
        ToolTip(
            self.token_entry,
            text="Enter received security code.",
            bootstyle="primary"
        )
        self.token_entry.grid(row=6, column=0, columnspan=2)

        self.reset_otp_btn = ttkb.Button(
            self,
            text="Reset 2FA",
            width=37
        )
        self.reset_otp_btn.grid(row=7, column=0, columnspan=2, pady=5)


class SettingsView(ttkb.Frame):

    def __init__(self, master):
        """
        Displays Settings page.
        :param master: ttkb.Frame (container from AppView)
        """
        super().__init__(master)

        self.cyborg_img = ttkb.PhotoImage(file="pwm_data/img/cyborg.png")
        self.morph_img = ttkb.PhotoImage(file="pwm_data/img/morph.png")
        self.vapor_img = ttkb.PhotoImage(file="pwm_data/img/vapor.png")
        self.solar_img = ttkb.PhotoImage(file="pwm_data/img/solar.png")

        self.back_btn = ttkb.Button(
            self,
            text="B A C K",
            width=5,
            style="primary-outline"
        )
        self.back_btn.grid(row=0, column=0, pady=(0, 0), sticky="w")

        self.title_label = ttkb.Label(
            self,
            text="Settings",
            font=AppView.TITLE_FONT,
            justify="center",
            foreground=AppView.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, columnspan=4, pady=10)

        self.theme_label = ttkb.Label(
            self,
            text="Select theme:",
            justify="center",
            font=AppView.FONT
        )
        self.theme_label.grid(row=2, column=0, columnspan=4, pady=30)

        self.cyborg_theme_btn = ttkb.Radiobutton(
            self,
            image=self.cyborg_img,
        )
        ToolTip(
            self.cyborg_theme_btn,
            text="Cyborg Theme",
            bootstyle="primary"
        )
        self.cyborg_theme_btn.grid(row=3, column=0, padx=7)

        self.morph_theme_btn = ttkb.Radiobutton(
            self,
            image=self.morph_img,
        )
        ToolTip(
            self.morph_theme_btn,
            text="Morph Theme",
            bootstyle="primary"
        )
        self.morph_theme_btn.grid(row=3, column=1, padx=7)

        self.vapor_theme_btn = ttkb.Radiobutton(
            self,
            image=self.vapor_img,
        )
        ToolTip(
            self.vapor_theme_btn,
            text="Vapor Theme",
            bootstyle="primary"
        )
        self.vapor_theme_btn.grid(row=3, column=2, padx=7)

        self.solar_theme_btn = ttkb.Radiobutton(
            self,
            image=self.solar_img,
        )
        ToolTip(
            self.solar_theme_btn,
            text="Solar Theme",
            bootstyle="primary"
        )
        self.solar_theme_btn.grid(row=3, column=3, padx=7)

        seperator = ttkb.Separator(self, style="primary")
        seperator.grid(row=4, column=0, columnspan=4, sticky="we", pady=(30, 10))

        self.theme_label = ttkb.Label(
            self,
            text="Preferred password length:",
            justify="center",
            font=AppView.FONT
        )
        self.theme_label.grid(row=5, column=0, columnspan=4, pady=20)

        self.password_meter = ttkb.Meter(
            self,
            amounttotal=50,
            bootstyle="primary",
            showtext=True,
            interactive=True,
            stripethickness=10,
            metertype="semi",
            stepsize=4,
            meterthickness=20,
        )
        self.password_meter.grid(row=6, column=0, columnspan=4)

        seperator = ttkb.Separator(self, style="primary")
        seperator.grid(row=7, column=0, columnspan=4, sticky="we", pady=10)

        self.change_pw_btn = ttkb.Button(
            self,
            text="Change Password",
            width=37,
            style="primary-outline"
        )
        self.change_pw_btn.grid(row=8, column=0, columnspan=4, pady=(30, 10))

        self.delete_acc_btn = ttkb.Button(
            self,
            text="Delete Account",
            width=37,
            style="danger-outline"
        )
        self.delete_acc_btn.grid(row=9, column=0, columnspan=4, pady=5)

    def should_delete(self) -> str:
        """
        Shows messagebox with question.
        :return str: "Delete" or "No"
        """
        return Messagebox.show_question(
            "Do you really want to delete account and wipe all related data?"
            " This process cannot be undone!",
            buttons=["No:secondary", "Delete Account:danger"],
            parent=self
        )

    def account_deleted(self):
        """
        Shows info messagebox.
        """
        Messagebox.show_info("Account has been deleted!", parent=self)


class EntryMod(ttkb.Entry):
    """
    Encapsulates entry box set-up and bindings.
    """

    def __init__(self, master: ttkb.Frame, box_width: int = 20, placeholder: str = "", show: str = ""):
        """
        Initializes Entry object.
        :param master: Parent or root (Frame container)
        :param box_width: Width for entry box, default value is 20
        :param placeholder: Placeholder for entry
        :param show: Hides input in entry by specified character, for example "*"
        """
        super().__init__(master)
        self.show = show
        self.config(font=AppView.FONT, width=box_width)
        self.placeholder = placeholder
        self.set()

    def set(self):
        """
        Sets up Entry widget. Inserts placeholder and binds to focus-in and focus out events.
        Everytime when function is called clears and resets Entry box.
        """
        self.delete(0, tk.END)
        if self.placeholder:
            self.insert(0, self.placeholder)
            self.config(foreground="gray")
            self.bind("<FocusIn>", self.on_entry_focus_in)
            self.bind("<FocusOut>", self.on_entry_focus_out)
            if self.get() == self.placeholder:
                self.config(show="")

    def on_entry_focus_in(self, event):
        """
        When entry box gains focus, removes placeholder and changes text color to white, if "show parameter" is
        different from empty string, replaces characters by specified character, for example * to hide passwords.
        :param event: Focus-in event
        """
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            if self.show:
                self.config(show=self.show)
            self.config(foreground="")

    def on_entry_focus_out(self, event):
        """
        If entry box is empty and loses focus, places placeholder in it and changes text color to grey.
        :param event: Focus-out event
        """
        if self.get() == "":
            self.insert(0, self.placeholder)
            self.config(foreground="gray", show="")
