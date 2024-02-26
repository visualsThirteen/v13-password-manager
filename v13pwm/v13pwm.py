from view import AppView
from controller import AppController
from security_engine import SecurityEngine


def main():
    security_engine = SecurityEngine()
    app = AppView()
    AppController(app, security_engine)
    app.mainloop()


if __name__ == "__main__":
    main()
