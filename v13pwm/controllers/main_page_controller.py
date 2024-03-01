import tkinter as tk
from models.data_processor import DataProcessor
from models.password_generator import PasswordGenerator


class MainPageController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Main page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["main_page"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Main page buttons to functions.
        """
        self.frame.app_combox.config(
            postcommand=lambda: self.frame.app_combox.config(
                values=DataProcessor.get_all_apps()
            )
        )
        self.frame.settings_btn.config(command=lambda: self.app_view.show_frame("settings"))
        self.frame.gen_password_btn.config(command=self.gen_pw_pressed)
        self.frame.add_btn.config(command=self.add_pressed)
        self.frame.search_btn.config(command=self.search_pressed)
        self.frame.logout_btn.config(command=self.logout_pressed)

    def show_all_apps(self):
        """
        Populates combox with all apps in database.
        """
        self.frame.app_combox.config(values=lambda: DataProcessor.get_all_apps())

    def gen_pw_pressed(self):
        """
        Generates password, inserts it in password_entry box and copies password to clipboard.
        """
        password = PasswordGenerator.generate_password(self.app_controller.password_length)
        self.frame.password_entry.config(foreground="white")
        self.frame.password_entry.delete(0, tk.END)
        self.frame.password_entry.insert(0, string=password)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(password)

    def add_pressed(self):
        """
        Checks if all required fields are filled, if not, gives user error message.
        Asks user for approval to save credentials, if credentials exists for particular app, aks if
        user wants to update these credentials, if approved, saves details to database clears widgets,
        and gives feedback to user.
        """
        app = self.frame.app_combox.get().strip().lower()
        username = self.frame.username_entry.get().strip().lower()
        password = self.frame.password_entry.get()
        encrypted_password = self.security_engine.encrypt(password)
        if not app:
            self.frame.error_label.config(text="App / Web field is empty!", foreground="red")
        elif not username:
            self.frame.error_label.config(text="Username field is empty!", foreground="red")
        elif not password:
            self.frame.error_label.config(text="Password field is empty!", foreground="red")
        elif self.frame.should_save() == "Yes":
            if DataProcessor.search_record(app):
                if self.frame.should_replace(app) == "No":
                    self.frame.app_combox.delete(0, tk.END)
                    self.frame.username_entry.set()
                    self.frame.password_entry.set()
                    return
                else:
                    DataProcessor.update_record(app, username, encrypted_password)
            else:
                DataProcessor.insert_record(app, username, encrypted_password)
            self.frame.app_combox.delete(0, tk.END)
            self.frame.username_entry.set()
            self.frame.password_entry.set()
            self.frame.error_label.config(text="Data saved successfully!", foreground="green")
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def search_pressed(self):
        """
        Searches for credentials associated with entered app, in case app field is empty or credentials not found
        shows error message to user. If credentials are found, inserts username in
        username_entry box and password to password_entry box, copies password to clipboard and gives
        feedback to user.
        """
        app = self.frame.app_combox.get().strip().lower()
        if not app:
            self.frame.error_label.config(text="App / Web field is empty!", foreground="red")
        else:
            content = DataProcessor.search_record(app)
            if content:
                username, password = content
                password = self.security_engine.decrypt(password)
                self.frame.username_entry.delete(0, tk.END)
                self.frame.username_entry.insert(0, username)
                self.frame.password_entry.delete(0, tk.END)
                self.frame.password_entry.insert(0, password)
                self.frame.clipboard_clear()
                self.frame.clipboard_append(password)
                self.frame.error_label.config(text="Data retrieved successfully!", foreground="green")
            else:
                self.frame.error_label.config(text="Nothing was found!", foreground="red")
        self.frame.after(3000, lambda: self.frame.error_label.config(text=""))

    def logout_pressed(self):
        """
        Clears widgets and leads user to Login page.
        """
        self.app_view.show_frame("login")
        self.frame.app_combox.delete(0, tk.END)
        self.frame.username_entry.set()
        self.frame.password_entry.set()
