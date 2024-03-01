import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        self.info_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            justify="center",
            text='Click "Send Security Code" button to send security code to your registered e-mail, '
                 'enter received code and click "Reset 2FA"'
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            foreground=style_config.PRIMARY_COLOR,
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
            font=style_config.SMALL_FONT,
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
