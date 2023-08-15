from collections.abc import Sequence

import pytest
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter

from logfire.observe import LogfireConfig, Observe


class TestExporter(SpanExporter):
    def __init__(self) -> None:
        self.exported_spans: Sequence[ReadableSpan] = []

    def export(self, spans: Sequence[ReadableSpan]) -> None:  # type: ignore[override]
        self.exported_spans = spans

    def shutdown(self) -> None:
        pass


@pytest.fixture
def config() -> LogfireConfig:
    return LogfireConfig(auto_initialize_project=False)


@pytest.fixture
def exporter() -> TestExporter:
    return TestExporter()


@pytest.fixture
def observe(config: LogfireConfig, exporter: TestExporter) -> Observe:
    observe = Observe()
    observe.configure(config=config, exporter=exporter)
    return observe