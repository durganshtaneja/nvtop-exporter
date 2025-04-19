# nvtop Exporter

Prometheus exporter for nvtop metrics written in Python.

## About

NVTOP stands for Neat Videocard TOP, a (h)top-like task monitor for GPUs and accelerators. It can handle multiple GPUs and print information about them in a htop-familiar way. This exporter captures metrics from NVTOP and exposes them to Prometheus for monitoring and visualization.

### NVTOP Repository
For more information about NVTOP, visit the official repository: [NVTOP GitHub Repository](https://github.com/Syllo/nvtop)

## Prerequisites

- Python 3.x
- Prometheus client library for Python (`prometheus_client`)
- NVTOP installed on your system

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd nvtop-exporter
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure NVTOP is installed and accessible from the command line. Follow the instructions in the [NVTOP GitHub Repository](https://github.com/Syllo/nvtop) to install NVTOP.

## Usage

Run the exporter with the following command:
```bash
python exporter.py --port <port> --interval <interval> [--verbose]
```

### Arguments
- `--port` or `-p`: Port to run the Prometheus server on (default: 8000).
- `--interval` or `-i`: Interval in seconds between metric scrapes (default: 5).
- `--verbose` or `-v`: Prints captured data to stdout (optional).

### Example
```bash
python exporter.py --port 8000 --interval 5 --verbose
```

## Running in a Docker Container

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t nvtop-exporter .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 nvtop-exporter
   ```

### Using Docker Compose
1. Start the container using Docker Compose:
   ```bash
   docker-compose up
   ```

2. Access the Prometheus metrics at `http://localhost:8000/metrics`.

### Notes
- Ensure NVTOP is installed on the host system and accessible to the container if required.
- Modify the `docker-compose.yml` file to customize the setup as needed.

## Sample Outputs

### NVTOP Output
Below is an example of NVTOP's output:
```bash
sudo nvtop -s
[
  {
   "device_name": "DG2 (Arc A380)",
   "gpu_clock": "2450MHz",
   "mem_clock": null,
   "temp": "42C",
   "fan_speed": "938RPM",
   "power_draw": null,
   "gpu_util": null,
   "mem_util": "4%"
  }
]
```

### Exporter Output (Verbose Mode)
When running the exporter with `--verbose`, you might see output like this:
```
Prometheus server started on port 8000.
Scraping nvtop metrics every 5 seconds.
GPU Name: NVIDIA GTX GPU Clock: 1500 MHz Memory Clock: 7000 MHz GPU Temperature: 65 C Fan Speed: 40 RPM Power Draw: 20 W GPU Usage: 10 % Memory Usage: 5 %
```

### Prometheus Metrics
The following metrics are exposed by the exporter:
- `nvtop_gpu_clock`: GPU clock speed in MHz
- `nvtop_memory_clock`: GPU memory clock speed in MHz
- `nvtop_gpu_temperature`: GPU temperature in Celsius
- `nvtop_gpu_fan_speed`: GPU fan speed in RPM
- `nvtop_gpu_power_draw`: GPU power draw in Watts
- `nvtop_gpu_usage`: Total GPU usage in percent
- `nvtop_memory_usage`: Total GPU memory usage in percent

## Monitoring with Prometheus

1. Add the exporter to your Prometheus configuration file:
   ```yaml
   scrape_configs:
     - job_name: 'nvtop_exporter'
       static_configs:
         - targets: ['localhost:8000']
   ```

2. Restart Prometheus to apply the changes.

3. Access Prometheus at `http://<prometheus-server>:9090` and query the metrics exposed by the exporter.

## Troubleshooting

- Ensure NVTOP is installed and accessible from the command line.
- If you encounter errors, run the exporter with the `--verbose` flag to debug.
- Check that the specified port is not already in use.

## License
This project is licensed under the MIT License.