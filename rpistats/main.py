import importlib
import socket
import psutil
import json
import time
import argparse
from abc import ABC, abstractmethod

def collect_stats():
    """Collects comprehensive system statistics, including CPU temperature."""
    
    fl = open("/sys/class/thermal/thermal_zone0/temp", "r") 
    cpu_temp = fl.readline()

    # Other stats remain the same as previously mentioned
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    stats = {
        'cpu': {
            'temperature_celsius': cpu_temp,
            'usage_percent': cpu_usage,
            'frequency_ghz': psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else "N/A",
        },
        'memory': {
            'total_gb': memory.total / (1024 ** 3),
            'used_percent': memory.percent,
            'available_gb': memory.available / (1024 ** 3),
        },
        'disk': {
            'total_gb': disk_usage.total / (1024 ** 3),
            'used_percent': disk_usage.percent,
            'free_gb': disk_usage.free / (1024 ** 3),
        },
        'network': {
            'bytes_sent_mb': net_io.bytes_sent / (1024 ** 2),
            'bytes_recv_mb': net_io.bytes_recv / (1024 ** 2),
        }
    }

    return stats


# Define the Collector interface
class Collector(ABC):
    @abstractmethod
    def collect(self):
        """Collect statistics."""
        pass

# Publisher base class
class Publisher(ABC):
    @abstractmethod
    def publish(self, data):
        pass


# Concrete collector classes

class CpuCollector(Collector):
    def collect(self):
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

class MemoryCollector(Collector):
    def collect(self):
        memory = psutil.virtual_memory()
        
        return {
            'total_gb': memory.total / (1024 ** 3),
            'used_percent': memory.percent,
            'available_gb': memory.available / (1024 ** 3),
        }

class DiskCollector(Collector):
    def collect(self):
        disk_usage = psutil.disk_usage('/')


        return {
            'total_gb': disk_usage.total / (1024 ** 3),
            'used_percent': disk_usage.percent,
            'free_gb': disk_usage.free / (1024 ** 3),
        }


# Load configuration from a JSON file
def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    # Check if 'hostname' is provided in the config, otherwise get the system's hostname
    config['hostname'] = config.get('hostname', socket.gethostname())
    config['extended'] = config.get('extended', None)
    print( config.get('custom_attributes', None) )
    return config

# Initialize the appropriate collectors based on configuration
def initialize_collectors(collector_configs):
    collectors = []
    for config in collector_configs:
        if config['type'] == 'cpu':
            collectors.append(CpuCollector())
        elif config['type'] == 'memory':
            collectors.append(MemoryCollector())
        elif config['type'] == 'disk':
            collectors.append(DiskCollector())
    return collectors

def initialize_publishers(publishers_config):
    publishers = []
    for config in publishers_config:
        publisher_module = importlib.import_module(f"publishers.{config['type']}_publisher")
        PublisherClass = getattr(publisher_module, config['class_name'])
        publisher = PublisherClass(**config['params'])
        publishers.append(publisher)
    return publishers

def publish_data(publishers, data):
    for publisher in publishers:
        publisher.publish(data)


# Main function to set up the publisher and collectors and continuously publish data
def main():
    config = load_config()  # Load the configuration
    collectors = initialize_collectors(config['collectors'])  # Initialize collectors
    publishers = initialize_publishers(config['publishers']) # Initialize the publishers

    while True:
        data = {collector.__class__.__name__: collector.collect() for collector in collectors}
        # Add hostname to the data
        data['hostname'] = config['hostname']
        if config['extended'] != None:
            data['extended'] = config['extended']

        publish_data(publishers, data)
        time.sleep(60)  # Sleep for 60 seconds (or any configured interval)

if __name__ == '__main__':
    main()
