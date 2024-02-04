import time
from logging import LogRecord
from typing import Any, Dict

from pythonjsonlogger.jsonlogger import JsonFormatter


# Pretty much all of this is taken verbatim from
# https://github.com/madzak/python-json-logger/blob/5f85723f4693c7289724fdcda84cfc0b62da74d4/README.md#customizing-fields
class NormalizedJsonFormatter(JsonFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # This init method exists to reduce the blast radius of type ignores
        # needed when instantiating this class. The GitHub issue to fix the
        # problem that requires this type ignore annotation can be found here:
        # https://github.com/madzak/python-json-logger/issues/173
        super().__init__(*args, **kwargs)  # type: ignore[no-untyped-call]

    def add_fields(
        self, log_record: Dict, record: LogRecord, message_dict: Dict
    ) -> None:
        super(NormalizedJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )

        if not log_record.get("timestamp"):
            log_record["timestamp"] = record.created or self._generate_timestamp()
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

    def _generate_timestamp(self) -> float:
        return time.time()
