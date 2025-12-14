"""OpenTelemetry tracing setup for the Ollama agent"""

import os
from typing import Optional
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

try:
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    HAS_REQUESTS_INSTRUMENTATION = True
except ImportError:
    HAS_REQUESTS_INSTRUMENTATION = False


def setup_tracing(
    service_name: str = "ollama-agent",
    otlp_endpoint: str = "http://localhost:4317",
    enabled: bool = True,
) -> tuple[Optional[trace.Tracer], Optional[metrics.Meter]]:
    """Set up OpenTelemetry tracing and metrics.
    
    Args:
        service_name: Name of the service for tracing
        otlp_endpoint: OTLP collector endpoint
        enabled: Whether to enable tracing
        
    Returns:
        Tuple of (tracer, meter) or (None, None) if disabled
    """
    if not enabled:
        return None, None
    
    try:
        # Set up trace exporter
        trace_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        trace_provider = TracerProvider()
        trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
        trace.set_tracer_provider(trace_provider)
        
        # Set up metrics exporter
        metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint)
        metric_reader = PeriodicExportingMetricReader(metric_exporter)
        meter_provider = MeterProvider(metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        
        # Instrument requests library if available
        if HAS_REQUESTS_INSTRUMENTATION:
            RequestsInstrumentor().instrument()
        
        # Get tracer and meter
        tracer = trace.get_tracer(__name__)
        meter = metrics.get_meter(__name__)
        
        return tracer, meter
    except Exception as e:
        print(f"Warning: Could not set up tracing: {e}")
        return None, None


class TracedAgent:
    """Wrapper for agent with tracing support."""
    
    def __init__(self, agent, tracer: Optional[trace.Tracer] = None, meter: Optional[metrics.Meter] = None):
        """Initialize traced agent.
        
        Args:
            agent: The agent instance to wrap
            tracer: OpenTelemetry tracer
            meter: OpenTelemetry meter
        """
        self.agent = agent
        self.tracer = tracer
        self.meter = meter
        
        # Create metrics if meter is available
        if self.meter:
            self.tool_calls_counter = self.meter.create_counter(
                "agent.tool_calls",
                description="Number of tool calls",
                unit="1"
            )
            self.tool_errors_counter = self.meter.create_counter(
                "agent.tool_errors",
                description="Number of tool errors",
                unit="1"
            )
            self.response_time_histogram = self.meter.create_histogram(
                "agent.response_time",
                description="Response generation time",
                unit="ms"
            )
    
    def stream_response(self, message: str, **kwargs):
        """Stream response with tracing.
        
        Args:
            message: User message
            **kwargs: Additional arguments for stream_response
            
        Yields:
            Response chunks
        """
        if not self.tracer:
            yield from self.agent.stream_response(message, **kwargs)
            return
        
        with self.tracer.start_as_current_span("agent.stream_response") as span:
            span.set_attribute("user.message", message[:100])  # Limit attribute size
            
            import time
            start_time = time.time()
            
            try:
                for chunk in self.agent.stream_response(message, **kwargs):
                    yield chunk
                
                elapsed_ms = (time.time() - start_time) * 1000
                if self.meter:
                    self.response_time_histogram.record(elapsed_ms)
                span.set_attribute("response.time_ms", elapsed_ms)
                
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("error", True)
                raise
    
    def get_response(self, message: str, **kwargs) -> str:
        """Get response with tracing.
        
        Args:
            message: User message
            **kwargs: Additional arguments
            
        Returns:
            Response text
        """
        if not self.tracer:
            return self.agent.get_response(message, **kwargs)
        
        with self.tracer.start_as_current_span("agent.get_response") as span:
            span.set_attribute("user.message", message[:100])
            
            import time
            start_time = time.time()
            
            try:
                response = self.agent.get_response(message, **kwargs)
                
                elapsed_ms = (time.time() - start_time) * 1000
                if self.meter:
                    self.response_time_histogram.record(elapsed_ms)
                span.set_attribute("response.time_ms", elapsed_ms)
                span.set_attribute("response.length", len(response))
                
                return response
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("error", True)
                raise
    
    def __getattr__(self, name):
        """Delegate other methods to the agent."""
        return getattr(self.agent, name)
