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
