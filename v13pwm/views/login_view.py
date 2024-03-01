import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground=style_config.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.password_label = ttkb.Label(
            self,
            text="Enter Master Password to access your passwords",
            justify="center",
            font=style_config.FONT
        )
        self.password_label.grid(row=2, column=0, pady=8, padx=5)

        self.error_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
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
