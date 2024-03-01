import ttkbootstrap as ttkb
import sys
from models.data_processor import DataProcessor


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
