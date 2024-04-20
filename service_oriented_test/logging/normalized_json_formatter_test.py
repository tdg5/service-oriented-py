import json
import logging
import time
from io import StringIO
from logging import Logger, StreamHandler
from typing import Dict
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

    def test_directly_logging_a_dict_of_data(self) -> None:
        formatter = NormalizedJsonFormatter()
        self.initialize_logger(formatter=formatter)
        message = "Hello, world!"
        other = "other stuff"
        time_before_log = time.time()
        self.logger.info({"message": message, "other": other})
        time_after_log = time.time()
        log_record = json.loads(self.stream.getvalue())
        assert message == log_record["message"]
        assert other == log_record["other"]
        assert "INFO" == log_record["level"]
        assert time_before_log <= log_record["timestamp"] <= time_after_log

    def test_basic_normalization(self) -> None:
        formatter = NormalizedJsonFormatter()
        self.initialize_logger(formatter=formatter)
        message = "Hello, world!"
        time_before_log = time.time()
        self.logger.info(message)
        time_after_log = time.time()
        log_record = json.loads(self.stream.getvalue())
        assert message == log_record["message"]
        assert "INFO" == log_record["level"]
        assert time_before_log <= log_record["timestamp"] <= time_after_log

    def test_explicit_level_is_normalized(self) -> None:
        formatter = NormalizedJsonFormatter()
        self.initialize_logger(formatter=formatter)
        expected_level = "DEBUG"
        self.logger.info({"level": expected_level.lower()})
        log_record = json.loads(self.stream.getvalue())
        assert expected_level == log_record["level"]

    def test_explicit_timestamp_is_honored(self) -> None:
        formatter = NormalizedJsonFormatter()
        self.initialize_logger(formatter=formatter)
        expected_timestamp = time.time()
        self.logger.info("message", extra={"timestamp": expected_timestamp})
        log_record = json.loads(self.stream.getvalue())
        assert expected_timestamp == log_record["timestamp"]

    @pytest.mark.usefixtures("mocker")
    def test_timestamp_is_generated_when_absent_and_missing_from_log_record(
        self,
        mocker: MockerFixture,
    ) -> None:
        formatter = NormalizedJsonFormatter()
        record = logging.makeLogRecord(
            {
                "created": None,
                "levelno": logging.INFO,
                "levelname": "INFO",
                "lineno": 56,
                "msg": "message",
                "name": __name__,
                "pathname": __file__,
            }
        )
        log_record: Dict = {}
        message_dict: Dict = {}
        expected_timestamp = time.time()
        mocker.patch.object(time, "time", return_value=expected_timestamp)
        formatter.add_fields(
            log_record=log_record,
            message_dict=message_dict,
            record=record,
        )
        assert expected_timestamp == log_record["timestamp"]

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
