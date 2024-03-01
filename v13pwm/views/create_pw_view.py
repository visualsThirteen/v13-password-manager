import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, pady=10)

        self.password_label = ttkb.Label(
            self,
            text="Password must be 8-72 characters long and must contain at least 1 uppercase letter,"
                 " 1 lowercase letter, 1 number and 1 special character",
            font=style_config.SMALL_FONT,
            justify="center",
            wraplength=350
        )
        self.password_label.grid(row=2, column=0, pady=8, padx=5)

        self.pw_error_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
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
