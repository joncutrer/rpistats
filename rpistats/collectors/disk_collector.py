from . import Collector

class DiskCollector(Collector):
    def __init__(self, unit='gigabytes'):
        self.unit = unit
        self.unit_factor = {
            'kilobytes': 1024,
            'megabytes': 1024 ** 2,
            'gigabytes': 1024 ** 3,
            'terabytes': 1024 ** 4,
        }.get(unit, 1024 ** 3)  # Default to gigabytes if unit is not recognized

    async def collect(self):
        import psutil
        disk_usage = psutil.disk_usage('/')

        return {
            'total': disk_usage.total / self.unit_factor,
            'used_percent': disk_usage.percent,
            'free': disk_usage.free / self.unit_factor,
        }
