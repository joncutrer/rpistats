from . import Collector

class MemoryCollector(Collector):
    def collect(self):
        import psutil
        mem = psutil.virtual_memory()
        return {"memory_usage": mem.percent}

