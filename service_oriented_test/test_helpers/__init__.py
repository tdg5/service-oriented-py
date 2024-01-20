from service_oriented import DeploymentEnvironment


TEST_DEPLOYMENT_ENVIRONMENT = DeploymentEnvironment(
    identifier="test",
    region="test",
    stage="test",
    vendor="test",
)


TEST_ENTRY_POINT = "test"


__all__ = [
    "TEST_DEPLOYMENT_ENVIRONMENT",
    "TEST_ENTRY_POINT",
]
