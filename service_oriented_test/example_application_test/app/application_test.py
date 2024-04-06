from service_oriented_test.example_application.app.application import Application


def test_printer_endpoint_is_defined() -> None:
    assert "printer" in Application.default_entry_points
