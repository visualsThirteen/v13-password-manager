from utilities.common_functions import CommonFunctions


class CreatePwController:

    def __init__(self, app_controller, app_view):
        """
        Initializes Create Password page controller.
        :param app_controller: AppController class.
        :param app_view: AppView class.
        """
        self.app_controller = app_controller
        self.app_view = app_view
        self.frame = app_view.initialized_frames["create_pw"]
        self.security_engine = app_controller.security_engine
        self._bind()

    def _bind(self):
        """
        Binds Create Password page buttons to functions.
        """
        self.frame.save_btn.config(command=lambda: CommonFunctions.save_password(self))
