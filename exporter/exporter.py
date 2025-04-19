import subprocess
from prometheus_client import start_http_server, Gauge
import json
from time import sleep
import argparse

# Create Gauge metric to store nvtop output
nvtop_gpu_clock = Gauge('nvtop_gpu_clock', 'GPU clock speed in MHz',['gpu'])
nvtop_mem_clock = Gauge('nvtop_memory_clock', 'GPU memory clock speed in MHz',['gpu'])
nvtop_gpu_temp = Gauge('nvtop_gpu_temperature', 'GPU temperature in C',['gpu'])
nvtop_gpu_fan_speed = Gauge('nvtop_gpu_fan_speed', 'GPU fan speed in RPM',['gpu'])
nvtop_gpu_power_draw = Gauge('nvtop_gpu_power_draw', 'GPU power draw in Watts',['gpu'])
nvtop_gpu_usage = Gauge('nvtop_gpu_usage', 'Total GPU usage in percent',['gpu'])
nvtop_memory_usage = Gauge('nvtop_memory_usage', 'Total GPU memory usage in percent',['gpu'])

def get_nvtop_metrics(interval):
    try:
        # Run nvtop and capture the output
        result = subprocess.check_output(['nvtop', '-s']).decode('utf-8')
        if 'No GPU to monitor.' not in result:
            metrics = json.loads(result)
            for metric in metrics:
                # Metrics extraction
                name= metric['device_name']  # Get GPU name

                if metric['gpu_clock']: # Check if GPU clock is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                    gpu_clock = int(metric['gpu_clock'][:-3])  # Get GPU clock in MHz
                    nvtop_gpu_clock.labels(name).set(gpu_clock)
                else:
                    gpu_clock = 0
                    nvtop_gpu_clock.labels(name).set(0)

                if metric['mem_clock']: # Check if memory clock is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                    mem_clock = int(metric['mem_clock'][:-3])  # Get memory clock in MHz
                    nvtop_mem_clock.labels(name).set(mem_clock)
                else:
                    mem_clock = 0
                    nvtop_mem_clock.labels(name).set(0)

                if metric['temp']:
                    gpu_temp = float(metric['temp'][:-1])
                    nvtop_gpu_temp.labels(name).set(gpu_temp)
                else:
                    gpu_temp = 0
                    nvtop_gpu_temp.labels(name).set(0) 

                if metric['fan_speed']: # Check if fan speed is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                    fan_speed= int(metric['fan_speed'][:-3])  # Get fan speed in RPM
                    nvtop_gpu_fan_speed.labels(name).set(fan_speed)
                else:
                    fan_speed = 0
                    nvtop_gpu_fan_speed.labels(name).set(0)
                    
                if metric['power_draw']: # Check if power draw is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                    power_draw = int(metric['power_draw'][:-1])  # Get power draw in Watts
                    nvtop_gpu_power_draw.labels(name).set(power_draw)
                else:
                    power_draw = 0
                    nvtop_gpu_power_draw.labels(name).set(0)

                if metric['gpu_util']: # Check if GPU utilization is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                    gpu_usage = int(metric['gpu_util'][:-1])  # Get GPU usage in percent
                    nvtop_gpu_usage.set(gpu_usage)
                else:
                    gpu_usage = 0
                    nvtop_gpu_usage.labels(name).set(0)
                
                if metric['mem_util']:
                    memory_usage = int(metric['mem_util'][:-1])  # Get memory usage in percent
                    nvtop_memory_usage.labels(name).set(memory_usage)
                else:
                    memory_usage = 0
                    nvtop_memory_usage.labels(name).set(0)
        else:
            print("No GPU found")
            exit(1)
        
        sleep(interval)  # Sleep for 5 seconds before the next scrape
    except Exception as e:
        print(f"Error scraping nvtop: {e}")
        exit(1)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export nvtop metrics to Prometheus.')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Port to run the Prometheus server on.')
    parser.add_argument('--interval', '-i', type=int, default=5, help='Interval in seconds between metric scrapes.')
    args = parser.parse_args()

    
    # Start up the server to expose the metrics.
    start_http_server(args.port)
    print(f"Prometheus server started on port {args.port}.")
    print(f"Scraping nvtop metrics every {args.interval} seconds.")
    
    while True:
        get_nvtop_metrics(args.interval)
