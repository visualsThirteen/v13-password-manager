import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox
from utilities import style_config


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
            font=style_config.TITLE_FONT,
            justify="center",
            foreground=style_config.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, columnspan=4, pady=10)

        self.theme_label = ttkb.Label(
            self,
            text="Select theme:",
            justify="center",
            font=style_config.FONT
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
            font=style_config.FONT
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
