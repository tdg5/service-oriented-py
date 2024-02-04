import json
import logging
import time
from io import StringIO
from logging import Logger, StreamHandler
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from service_oriented.logging.normalized_json_formatter import NormalizedJsonFormatter


class TestNormalizedJsonFormatter:
    def initialize_logger(self, formatter: NormalizedJsonFormatter) -> None:
        identifier = uuid4()
        self.logger: Logger = logging.getLogger(f"{__name__}-{identifier}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        self.stream: StringIO = StringIO()
        self.handler: StreamHandler = StreamHandler(self.stream)
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def test_basic_normalization(self, mocker: MockerFixture) -> None:
        formatter = NormalizedJsonFormatter()
        self.initialize_logger(formatter=formatter)
        message = "Hello, world!"
        time_before_log = time.time()
        self.logger.info(message)
        log_record = json.loads(self.stream.getvalue())
        assert message == log_record["message"]
        assert "INFO" == log_record["level"]
        assert time_before_log <= log_record["timestamp"]

    @pytest.mark.usefixtures("mocker")
    def test_generate_timestamp_is_not_typically_invoked(
        self,
        mocker: MockerFixture,
    ) -> None:
        formatter = NormalizedJsonFormatter()
        spy = mocker.spy(formatter, "_generate_timestamp")
        self.initialize_logger(formatter=formatter)
        self.logger.info("Hello, world!")
        log_record = json.loads(self.stream.getvalue())
        assert log_record
        assert 0 == spy.call_count
