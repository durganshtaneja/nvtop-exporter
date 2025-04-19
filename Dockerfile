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
    && cmake .. -DNVIDIA_SUPPORT=ON -DAMDGPU_SUPPORT=ON -DINTEL_SUPPORT=ON \
    && make \
    && make install \
    && rm -rf /tmp/nvtop

# Set the working directory in the container
WORKDIR /app

# Copy the exporter directory contents into the container at /app
COPY ./exporter/* /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE ${PORT}

# Define environment variable
ENV PORT=8000
ENV INTERVAL=5
# Run exporter.py when the container launches
ENTRYPOINT ["python", "exporter.py", "--port", "${PORT}", "--interval", "${INTERVAL}"]