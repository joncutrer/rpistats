import psutil
from . import Collector

class NetworkCollector(Collector):
    async def collect(self):
        """
        Collects basic network statistics.
        """
        stats = psutil.net_io_counters(pernic=True)
        network_data = {}
        for interface, data in stats.items():
            network_data[interface] = {
                'bytes_sent': data.bytes_sent,
                'bytes_recv': data.bytes_recv,
                'packets_sent': data.packets_sent,
                'packets_recv': data.packets_recv,
            }
        return network_data
