from os import path
from pathlib import Path

from service_oriented import DeploymentEnvironment


TEST_DEPLOYMENT_ENVIRONMENT = DeploymentEnvironment(
    identifier="test",
    region="test",
    stage="test",
    vendor="test",
)


def fixture_path(fixture_path: str) -> str:
    fixtures_path = Path(__file__).parent
    fixture_file_path = fixtures_path.joinpath(fixture_path)
    if not path.exists(fixture_file_path):
        raise ValueError(f"Could not find fixture file: '{fixture_path}'")

    return str(fixture_file_path.absolute())


def read_fixture_file(fixture_file_path: str) -> str:
    with open(fixture_path(fixture_file_path), encoding="utf-8", mode="r") as file:
        return file.read()
