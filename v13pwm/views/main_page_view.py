import ttkbootstrap as ttkb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox
from utilities.entry_mod import EntryMod
from utilities import style_config


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
            font=style_config.SMALL_FONT,
            foreground="red"
        )
        self.error_label.grid(row=1, column=1, pady=(0, 8), padx=5)

        self.app_label = ttkb.Label(
            self,
            text="App / Web:",
            font=style_config.FONT,
            foreground=style_config.PRIMARY_COLOR
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
            font=style_config.FONT,
            foreground=style_config.PRIMARY_COLOR
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
            font=style_config.FONT,
            foreground=style_config.PRIMARY_COLOR
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
