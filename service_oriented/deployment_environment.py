class DeploymentEnvironment:
    def __init__(
        self,
        identifier: str,
        region: str,
        stage: str,
        vendor: str,
    ):
        self.identifier: str = identifier
        self.region: str = region
        self.stage: str = stage
        self.vendor: str = vendor
        self.stub: str = f"{self.stage}:{self.vendor}:{self.region}:{self.identifier}"

    @classmethod
    def from_stub(cls, stub: str) -> "DeploymentEnvironment":
        components = stub.split(":")
        return DeploymentEnvironment(
            identifier=components[3],
            region=components[2],
            stage=components[0],
            vendor=components[1],
        )
