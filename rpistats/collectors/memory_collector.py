import psutil
from . import Collector


class MemoryCollector(Collector):
    async def collect(self):
        memory = psutil.virtual_memory()
        
        return {
            'total_gb': memory.total / (1024 ** 3),
            'used_percent': memory.percent,
            'available_gb': memory.available / (1024 ** 3),
        }