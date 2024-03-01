class TokenTimer:
    """
    Encapsulates logic for countdown mechanism.
    """
    controller = None
    time = None
    security_token_timer = None

    @classmethod
    def set_timer(cls, controller, time: int):
        """
        Takes current controller class and time in seconds from which to start countdown,
        starts timer.
        :param controller: Current controller class.
        :param int time: Time in seconds.
        """
        cls.time = time
        cls.controller = controller
        cls.start_timer()

    @classmethod
    def start_timer(cls):
        """
        If timer exists, cancels it and starts new timer.
        """
        if cls.security_token_timer is not None:
            cls.controller.frame.after_cancel(cls.security_token_timer)
        cls.timer_logic()

    @classmethod
    def timer_logic(cls):
        """
        Displays time in seconds until security token expires, if time left is less than 0, displays message to
        user and deletes security token. If time left is greater than 0, calls countdown function.
        """
        if cls.time < 0:
            cls.controller.frame.after_cancel(cls.security_token_timer)
            cls.controller.frame.timer_label.config(text="Security token expired!")
            cls.controller.app_controller.delete_token()
        else:
            cls.controller.frame.timer_label.config(
                text=f"Security token will expire after: {cls.time} seconds."
            )
            cls.time -= 1
            cls.countdown()

    @classmethod
    def countdown(cls):
        """
        Calls timer_logic function after 1 second.
        """
        timer = cls.controller.frame.after(1000, cls.timer_logic)
        cls.security_token_timer = timer
