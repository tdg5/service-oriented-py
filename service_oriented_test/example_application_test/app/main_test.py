from service_oriented_test.example_application.app.application import Application
from service_oriented_test.example_application.app.config import Config
from service_oriented_test.example_application.main import Main


def test_application_class_is_application() -> None:
    assert Application == Main.application_class()


def test_config_class_is_config() -> None:
    assert Config == Main.config_class()
