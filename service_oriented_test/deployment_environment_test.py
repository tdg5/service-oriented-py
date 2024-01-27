import pytest

from service_oriented.deployment_environment import DeploymentEnvironment


@pytest.mark.parametrize(
    "identifier,region,stage,vendor",
    [
        ("identifier", "region", "stage", "vendor"),
        ("IDENTIFIER", "REGION", "STAGE", "VENDOR"),
    ],
)
def test_constructor(identifier: str, region: str, stage: str, vendor: str) -> None:
    deployment_environment = DeploymentEnvironment(
        identifier=identifier,
        region=region,
        stage=stage,
        vendor=vendor,
    )
    assert identifier == deployment_environment.identifier
    assert region == deployment_environment.region
    assert stage == deployment_environment.stage
    assert vendor == deployment_environment.vendor
    stub = f"{stage}:{vendor}:{region}:{identifier}"
    assert stub == deployment_environment.stub


def test_equality_with_other_deployment_environment() -> None:
    deployment_environment = DeploymentEnvironment(
        identifier="identifier",
        region="region",
        stage="stage",
        vendor="vendor",
    )
    assert deployment_environment == deployment_environment
    equal_deployment_environment = DeploymentEnvironment(
        identifier="identifier",
        region="region",
        stage="stage",
        vendor="vendor",
    )
    assert deployment_environment == equal_deployment_environment
    unequal_deployment_environment = DeploymentEnvironment(
        identifier="IDENTIFIER",
        region="REGION",
        stage="STAGE",
        vendor="VENDOR",
    )
    assert deployment_environment != unequal_deployment_environment


def test_equality_with_non_deployment_environment() -> None:
    deployment_environment = DeploymentEnvironment(
        identifier="identifier",
        region="region",
        stage="stage",
        vendor="vendor",
    )
    assert deployment_environment != {}
    assert deployment_environment != 42
    assert deployment_environment != 3.14


def test_hash_with_other_deployment_environment() -> None:
    deployment_environment = DeploymentEnvironment(
        identifier="identifier",
        region="region",
        stage="stage",
        vendor="vendor",
    )
    assert hash(deployment_environment) == hash(deployment_environment)
    equal_deployment_environment = DeploymentEnvironment(
        identifier="identifier",
        region="region",
        stage="stage",
        vendor="vendor",
    )
    assert hash(deployment_environment) == hash(equal_deployment_environment)
    unequal_deployment_environment = DeploymentEnvironment(
        identifier="IDENTIFIER",
        region="REGION",
        stage="STAGE",
        vendor="VENDOR",
    )
    assert hash(deployment_environment) != hash(unequal_deployment_environment)
