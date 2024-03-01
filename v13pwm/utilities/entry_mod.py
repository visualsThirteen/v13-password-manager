import tkinter as tk
import ttkbootstrap as ttkb
from . import style_config


class EntryMod(ttkb.Entry):
    """
    Encapsulates entry box set-up and bindings.
    """

    def __init__(self, master: ttkb.Frame, box_width: int = 20, placeholder: str = "", show: str = ""):
        """
        Initializes Entry object.
        :param master: Parent or root (Frame container)
        :param box_width: Width for entry box, default value is 20
        :param placeholder: Placeholder for entry
        :param show: Hides input in entry by specified character, for example "*"
        """
        super().__init__(master)
        self.show = show
        self.config(font=style_config.FONT, width=box_width)
        self.placeholder = placeholder
        self.set()

    def set(self):
        """
        Sets up Entry widget. Inserts placeholder and binds to focus-in and focus out events.
        Everytime when function is called clears and resets Entry box.
        """
        self.delete(0, tk.END)
        if self.placeholder:
            self.insert(0, self.placeholder)
            self.config(foreground="gray")
            self.bind("<FocusIn>", self.on_entry_focus_in)
            self.bind("<FocusOut>", self.on_entry_focus_out)
            if self.get() == self.placeholder:
                self.config(show="")

    def on_entry_focus_in(self, event):
        """
        When entry box gains focus, removes placeholder and changes text color to white, if "show parameter" is
        different from empty string, replaces characters by specified character, for example * to hide passwords.
        :param event: Focus-in event
        """
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            if self.show:
                self.config(show=self.show)
            self.config(foreground="")

    def on_entry_focus_out(self, event):
        """
        If entry box is empty and loses focus, places placeholder in it and changes text color to grey.
        :param event: Focus-out event
        """
        if self.get() == "":
            self.insert(0, self.placeholder)
            self.config(foreground="gray", show="")
