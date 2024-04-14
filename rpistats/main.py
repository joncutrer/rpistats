import asyncio
import signal
import importlib
import socket
import json
import time



default_config = """

"""


# Load configuration from a JSON file
async def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    # Check if 'hostname' override is provided in the config, otherwise get the system's hostname
    config['hostname'] = config.get('hostname', socket.gethostname())
    config['extended'] = config.get('extended', None)
    return config

async def initialize_collectors(collectors_config):
    collectors = []
    for config in collectors_config:
        collector_module = importlib.import_module(f"collectors.{config['type']}_collector")
        CollectorClass = getattr(collector_module, config['class_name'])
        collector = CollectorClass(**config['params'])
        collectors.append(collector)
    return collectors

async def initialize_publishers(publishers_config):
    publishers = []
    for config in publishers_config:
        publisher_module = importlib.import_module(f"publishers.{config['type']}_publisher")
        PublisherClass = getattr(publisher_module, config['class_name'])
        publisher = PublisherClass(**config['params'])
        publishers.append(publisher)
    return publishers

async def publish_data(publishers, data):
    for publisher in publishers:
        await publisher.publish(data)

        
async def main_loop(config, collectors, publishers):
    while True:
        # Collect data from all collectors concurrently
        collector_data = await asyncio.gather(*(collector.collect() for collector in collectors))
        # Combine the collected data into a single dictionary
        data = {collector.__class__.__name__: data for collector, data in zip(collectors, collector_data)}
        # data = {collector.__class__.__name__: await collector.collect() for collector in collectors}
        
        data['hostname'] = config['hostname']
        if config.get('extended'):
            data['extended'] = config['extended']
        
        await publish_data(publishers, data)
        await asyncio.sleep(config.get("update_interval", 60))

def handle_sigint(signum, frame):
    print("Ctrl+C pressed, shutting down.")
    loop.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    signal.signal(signal.SIGINT, handle_sigint)

    config = loop.run_until_complete(load_config())
    collectors = loop.run_until_complete(initialize_collectors(config['collectors']))
    publishers = loop.run_until_complete(initialize_publishers(config['publishers']))

    try:
        loop.run_until_complete(main_loop(config, collectors, publishers))
    finally:
        loop.close()
