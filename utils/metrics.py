"""
Bot Stats Dashboard - Prometheus/Grafana metrics export
"""
import time
import logging
from typing import Dict, Optional, List
from collections import defaultdict
from aiohttp import web

logger = logging.getLogger(__name__)


class MetricType:
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


class Metric:
    """Represents a single metric."""
    
    def __init__(self, name: str, metric_type: str, description: str, labels: Optional[List[str]] = None):
        self.name = name
        self.type = metric_type
        self.description = description
        self.labels = labels or []
        self.value = 0.0
        self._samples: List[float] = []  # For histograms
    
    def inc(self, value: float = 1.0, label_values: Optional[Dict[str, str]] = None):
        """Increment counter."""
        self.value += value
    
    def dec(self, value: float = 1.0):
        """Decrement gauge."""
        self.value -= value
    
    def set(self, value: float):
        """Set gauge value."""
        self.value = value
    
    def observe(self, value: float):
        """Observe value (for histograms)."""
        self._samples.append(value)
        self.value += value
    
    def format_prometheus(self) -> str:
        """Format metric for Prometheus exposition."""
        lines = []
        
        # HELP
        lines.append(f"# HELP {self.name} {self.description}")
        # TYPE
        lines.append(f"# TYPE {self.name} {self.type}")
        
        if self.type == MetricType.HISTOGRAM and self._samples:
            # Simple histogram buckets
            lines.append(f"{self.name}_sum {self.value}")
            lines.append(f"{self.name}_count {len(self._samples)}")
        else:
            lines.append(f"{self.name} {self.value}")
        
        return "\n".join(lines)


class BotMetrics:
    """
    Collects and exports bot metrics for Prometheus/Grafana.
    
    Usage:
        metrics = BotMetrics()
        
        # In handlers:
        metrics.inc_messages()
        metrics.inc_users(user_id)
        metrics.observe_response_time(duration)
        
        # Expose /metrics endpoint:
        app.router.add_get('/metrics', metrics.get_metrics_handler())
    """
    
    def __init__(self):
        self._metrics: Dict[str, Metric] = {}
        self._active_users: set = set()
        self._message_counts: Dict[int, int] = defaultdict(int)
        
        # Register default metrics
        self._register_default_metrics()
    
    def _register_default_metrics(self):
        """Register default bot metrics."""
        self._metrics['messages_received'] = Metric(
            'messages_received',
            MetricType.COUNTER,
            'Total number of messages received'
        )
        
        self._metrics['messages_sent'] = Metric(
            'messages_sent',
            MetricType.COUNTER,
            'Total number of messages sent'
        )
        
        self._metrics['active_users'] = Metric(
            'active_users',
            MetricType.GAUGE,
            'Number of unique active users'
        )
        
        self._metrics['commands_executed'] = Metric(
            'commands_executed',
            MetricType.COUNTER,
            'Total number of commands executed'
        )
        
        self._metrics['callback_queries'] = Metric(
            'callback_queries',
            MetricType.COUNTER,
            'Total number of callback queries'
        )
        
        self._metrics['response_time'] = Metric(
            'response_time_seconds',
            MetricType.HISTOGRAM,
            'Response time in seconds'
        )
        
        self._metrics['errors'] = Metric(
            'errors_total',
            MetricType.COUNTER,
            'Total number of errors'
        )
        
        self._metrics['api_calls'] = Metric(
            'api_calls_total',
            MetricType.COUNTER,
            'Total number of API calls'
        )
        
        self._metrics['uptime'] = Metric(
            'uptime_seconds',
            MetricType.GAUGE,
            'Bot uptime in seconds'
        )
        
        self._start_time = time.time()
    
    def inc_messages(self):
        """Increment messages received counter."""
        self._metrics['messages_received'].inc()
    
    def inc_messages_sent(self):
        """Increment messages sent counter."""
        self._metrics['messages_sent'].inc()
    
    def inc_user(self, user_id: int):
        """Track active user."""
        if user_id not in self._active_users:
            self._active_users.add(user_id)
            self._metrics['active_users'].set(len(self._active_users))
        self._message_counts[user_id] += 1
    
    def inc_commands(self):
        """Increment commands counter."""
        self._metrics['commands_executed'].inc()
    
    def inc_callbacks(self):
        """Increment callback queries counter."""
        self._metrics['callback_queries'].inc()
    
    def observe_response_time(self, duration: float):
        """Record response time."""
        self._metrics['response_time'].observe(duration)
    
    def inc_errors(self):
        """Increment errors counter."""
        self._metrics['errors'].inc()
    
    def inc_api_calls(self):
        """Increment API calls counter."""
        self._metrics['api_calls'].inc()
    
    def update_uptime(self):
        """Update uptime metric."""
        self._metrics['uptime'].set(time.time() - self._start_time)
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get metric by name."""
        return self._metrics.get(name)
    
    def format_all(self) -> str:
        """Format all metrics for Prometheus."""
        self.update_uptime()
        
        lines = []
        for metric in self._metrics.values():
            lines.append(metric.format_prometheus())
            lines.append("")  # Empty line between metrics
        
        return "\n".join(lines)
    
    async def metrics_handler(self, request: web.Request) -> web.Response:
        """Aiohttp handler for /metrics endpoint."""
        return web.Response(
            text=self.format_all(),
            content_type='text/plain; version=0.0.4; charset=utf-8'
        )
    
    def get_metrics_handler(self, path: str = '/metrics'):
        """Get configured metrics handler."""
        async def handler(request: web.Request) -> web.Response:
            return await self.metrics_handler(request)
        return handler
    
    def reset(self):
        """Reset all metrics (for testing)."""
        for metric in self._metrics.values():
            metric.value = 0.0
            metric._samples.clear()
        self._active_users.clear()
        self._message_counts.clear()
        self._start_time = time.time()
