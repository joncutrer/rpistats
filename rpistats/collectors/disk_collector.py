from . import Collector

class DiskCollector(Collector):
    def collect(self):
        import psutil
        mem = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')


        return {
            'total_gb': disk_usage.total / (1024 ** 3),
            'used_percent': disk_usage.percent,
            'free_gb': disk_usage.free / (1024 ** 3),
        }

