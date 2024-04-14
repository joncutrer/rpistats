from . import Collector

# Concrete collector classes
class CpuCollector(Collector):
    def collect(self):
        import psutil
        return {"cpu_usage": psutil.cpu_percent(interval=1)}