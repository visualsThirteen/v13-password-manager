import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground=style_config.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.otp_label = ttkb.Label(
            self,
            text="Let's set up 2 factor authentication. "
                 "Open Google Authenticator app and scan QR code to add Password "
                 "Manager to your account",
            font=style_config.FONT,
            justify="center",
            wraplength=350
        )
        self.otp_label.grid(row=2, column=0, pady=8, padx=5)

        self.error_label = ttkb.Label(
            self,
            justify="center",
            font=style_config.SMALL_FONT,
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
