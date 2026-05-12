try:
    from prometheus_client import Counter, Histogram
    
    ORDERS_CREATED = Counter("orders_created_total", "Total orders created")
    ORDER_DURATION = Histogram("order_processing_duration_ms", "Order processing duration in ms")
    ORDER_ERRORS = Counter("order_errors_total", "Total order processing errors", ["type"])
except ImportError:
    # Fallback/Dummy metrics for development environment
    class DummyMetric:
        def inc(self, *args, **kwargs): pass
        def observe(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        
    ORDERS_CREATED = DummyMetric()
    ORDER_DURATION = DummyMetric()
    ORDER_ERRORS = DummyMetric()
