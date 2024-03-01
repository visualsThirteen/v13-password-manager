import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground="#38b6ff"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 50))

        self.info_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            justify="center",
            text='Click "Send Security Code" button to send security code to your registered e-mail, '
                 'enter received code and click "Submit"'
        )
        self.info_label.grid(row=2, column=0, columnspan=2)

        self.timer_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
            wraplength=350,
            foreground=style_config.PRIMARY_COLOR,
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
            font=style_config.SMALL_FONT,
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
            font=style_config.FONT,
            justify="center",
            wraplength=350
        )
        self.password_label.grid(row=9, column=0, pady=(0, 10))

        self.pw_error_label = ttkb.Label(
            self,
            font=style_config.SMALL_FONT,
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
