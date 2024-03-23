from service_oriented_test.example_application.app.application import Application


def test_api_endpoint_is_defined() -> None:
    assert "api" in Application.default_entry_points
