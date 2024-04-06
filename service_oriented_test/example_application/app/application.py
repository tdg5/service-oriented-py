from service_oriented.application import BaseApplication, EntryPointSpec
from service_oriented_test.example_application.app.entry_points.printer import (
    PrinterEntryPoint,
)


class Application(
    BaseApplication,
    entry_points={
        "printer": EntryPointSpec(PrinterEntryPoint),
    },
):
    pass
