from . import Collector
import psutil


class CpuCollector(Collector):
    async def collect(self):
        fl = open("/sys/class/thermal/thermal_zone0/temp", "r") 
        cpu_temp = int(fl.readline().strip()) / 1000

        # Other stats remain the same as previously mentioned
        cpu_usage = psutil.cpu_percent(interval=1)
        core_usage = psutil.cpu_percent(interval=1, percpu=True)
        core_count = psutil.cpu_count()
        stats = psutil.cpu_times_percent(interval = 1)
        return {
            'temp': cpu_temp,
            'usage': cpu_usage,
            'speed': int(psutil.cpu_freq().current) if psutil.cpu_freq() else "N/A",
            'cores_usage': core_usage,
            'cores': core_count,
            'stats': stats
        }