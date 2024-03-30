import logging

from service_oriented_test.example_application.app.config import Config


logger = logging.getLogger(__name__)


class ApiEntryPoint:
    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> None:
        print("hello world")
