import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.info_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            justify="center",
            text="We will send security code to your e-mail address, "
                 "this e-mail address will be required in order to reset password."
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            foreground=style_config.PRIMARY_COLOR,
            justify="center"
        )
        self.timer_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.error_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
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
