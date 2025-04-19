# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies for building nvtop
RUN apt-get update && apt-get install -y \
    git cmake build-essential libncurses5-dev libncursesw5-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and build nvtop
RUN git clone https://github.com/Syllo/nvtop.git /tmp/nvtop \
    && mkdir /tmp/nvtop/build \
    && cd /tmp/nvtop/build \
    && cmake .. \
    && make \
    && make install \
    && rm -rf /tmp/nvtop

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run exporter.py when the container launches
CMD ["python", "exporter.py"]