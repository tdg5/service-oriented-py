from service_oriented.application import BaseApplication, EntryPointSpec
from service_oriented_test.example_application.app.entry_points.api import ApiEntryPoint


class Application(
    BaseApplication,
    entry_points={
        "api": EntryPointSpec(ApiEntryPoint),
    },
):
    pass
