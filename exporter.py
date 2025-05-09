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

def get_nvtop_metrics(interval,verbose=False):
    try:
        # Run nvtop and capture the output
        result = subprocess.check_output(['nvtop', '-s'])
        metrics = json.loads(result.decode('utf-8'))
        
        for metric in metrics:
            # Metrics extraction
            name= metric['device_name']  # Get GPU name

            if metric['gpu_clock']: # Check if GPU clock is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                gpu_clock = int(metric['gpu_clock'][:-3])  # Get GPU clock in MHz
                nvtop_gpu_clock.labels(name).set(gpu_clock)
            else:
                gpu_clock = None

            if metric['mem_clock']: # Check if memory clock is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                mem_clock = int(metric['mem_clock'][:-3])  # Get memory clock in MHz
                nvtop_mem_clock.labels(name).set(mem_clock)
            else:
                mem_clock = None

            if metric['temp']:
                gpu_temp = float(metric['temp'][:-1])
                nvtop_gpu_temp.labels(name).set(gpu_temp)
            else:
                gpu_temp = None

            if metric['fan_speed']: # Check if fan speed is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                fan_speed= int(metric['fan_speed'][:-3])  # Get fan speed in RPM
                nvtop_gpu_fan_speed.labels(name).set(fan_speed)
            else:
                fan_speed = None
                
            if metric['power_draw']: # Check if power draw is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                power_draw = int(metric['power_draw'][:-1])  # Get power draw in Watts
                nvtop_gpu_power_draw.labels(name).set(power_draw)
            else:
                power_draw = None

            if metric['gpu_util']: # Check if GPU utilization is available, currently nvtop returns None in snapshot mode, will remove this check in the future
                gpu_usage = int(metric['gpu_util'][:-1])  # Get GPU usage in percent
                nvtop_gpu_usage.set(gpu_usage)
            else:
                gpu_usage = None
            
            if metric['mem_util']:
                memory_usage = int(metric['mem_util'][:-1])  # Get memory usage in percent
                nvtop_memory_usage.labels(name).set(memory_usage)
            else:
                memory_usage = None
                
            if verbose:    
                print(f"GPU Name: {name}",
                    f"GPU Clock: {gpu_clock} MHz",
                    f"Memory Clock: {mem_clock} MHz",
                    f"GPU Temperature: {gpu_temp} C",
                    f"Fan Speed: {fan_speed} RPM",
                    f"Power Draw: {power_draw} W",
                    f"GPU Usage: {gpu_usage} %",
                    f"Memory Usage: {memory_usage} %")
        
        sleep(interval)  # Sleep for 5 seconds before the next scrape
    except Exception as e:
        print(f"Error scraping nvtop: {e}")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export nvtop metrics to Prometheus.')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Port to run the Prometheus server on.')
    parser.add_argument('--interval', '-i', type=int, default=5, help='Interval in seconds between metric scrapes.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Prints captured data to stdout.')
    #parser.add_argument('-h', '--help', action='store_true', help='Print this help message')
    args = parser.parse_args()

    
    # Start up the server to expose the metrics.
    start_http_server(args.port)
    print(f"Prometheus server started on port {args.port}.")
    print(f"Scraping nvtop metrics every {args.interval} seconds.")
    
    while True:
        get_nvtop_metrics(args.interval,args.verbose)
