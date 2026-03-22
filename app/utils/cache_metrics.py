"""Lightweight metrics (mirrors logs.api pattern)."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CacheMetrics:
    """In-memory response time samples per endpoint."""

    samples: Dict[str, List[float]] = field(default_factory=dict)

    def record_response_time(
        self, endpoint: str, duration_ms: float, cached: bool = False
    ) -> None:
        if endpoint not in self.samples:
            self.samples[endpoint] = []
        self.samples[endpoint].append(duration_ms)
        # cap list size
        if len(self.samples[endpoint]) > 1000:
            self.samples[endpoint] = self.samples[endpoint][-500:]


_metrics = CacheMetrics()


def get_cache_metrics() -> CacheMetrics:
    return _metrics
