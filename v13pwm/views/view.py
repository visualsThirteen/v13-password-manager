import ttkbootstrap as ttkb
from PIL import Image
from .create_acc_view import CreateAccView
from .create_pw_view import CreatePwView
from .forgot_pw_view import ForgotPwView
from .setup_2fa_view import SetUp2FAView
from .reset_2fa_view import Reset2FAView
from .login_view import LoginView
from .main_page_view import MainPageView
from .settings_view import SettingsView


class AppView(ttkb.Window):
    """
    Initializes app window.
    """
    Image.CUBIC = Image.BICUBIC
    # Time in seconds after security token expires
    SECURITY_TOKEN_EXPIRE = 60

    def __init__(self):
        super().__init__()

        self.geometry("550x760")
        self.logo = ttkb.PhotoImage(file="pwm_data/img/logo.png")
        self.iconphoto(True, self.logo)
        self.resizable(False, False)
        self.config(padx=50, pady=50)
        self.title("V13 Password Manager")
        self.theme = ttkb.Style("cyborg")

        self.container = ttkb.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.initialized_frames: dict = {}

        self.frames: dict = {
            "login": LoginView,
            "create_acc": CreateAccView,
            "create_pw": CreatePwView,
            "forgot_pw": ForgotPwView,
            "setup_2fa": SetUp2FAView,
            "reset_2fa": Reset2FAView,
            "settings": SettingsView,
            "main_page": MainPageView
        }

        self.current_frame: str or None = None
        self.initialize_frames(self.frames)

    def initialize_frames(self, frames: dict):
        """
        Takes dictionary where frame name is a key and frame a value. Initializes frame by passing in parent frame
        and adds to initialized_frames dictionary preserving frame name as key.
        :param dict frames: Dictionary containing frame names as keys and frame objects as values.
        """
        for key, value in frames.items():
            frame = value(self.container)
            self.initialized_frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name: str):
        """
        Takes frame name and shows specified frame.
        :param str frame_name: Frame name.
        """
        self.current_frame = frame_name
        frame_to_show = self.initialized_frames[frame_name]
        frame_to_show.tkraise()
