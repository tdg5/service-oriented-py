from service_oriented.application import GenericMain
from service_oriented_test.example_application.app.application import Application
from service_oriented_test.example_application.app.config import Config


class Main(GenericMain[Config, Application]):
    pass


if __name__ == "__main__":
    Main().run()  # pragma: no cover
