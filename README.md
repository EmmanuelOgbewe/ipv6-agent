# IPv6 Agent Application

The IPv6 Agent Application is a lightweight tool designed to collect IPv6 addresses from Linux machines and report them to a central server. This README provides an overview of the application, its components, and instructions for installation and usage.

## Overview

The IPv6 Agent Application consists of two main components:

1. **Agent Script (`main.py`):**

   - This script is responsible for collecting IPv6 addresses from Linux machines.
   - It runs on each Linux machine as an agent.
   - The agent periodically reports the collected IPv6 addresses to the central server.

2. **Central Server:**
   - The central server receives IPv6 addresses from multiple agents.
   - It stores the collected IPv6 addresses in a database.


## Installation and run (without Docker)

To install and run the IPv6 Agent Application, follow these steps:

1. **Clone the Repository:**

```
git clone https://github.com/EmmanuelOgbewe/ipv6-agent
```

2. **Navigate to the cloned directory:**

```
cd ipv6-agent
```

3. **Make the script executable:**

```
chmod +x main.py
```

## Prerequisites

Before running the agent script on your Linux machines, ensure you have the prerequisites installed:

You can install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

4. **Run agent**

```
./main.py
```

5. **Create a symbolic link (Optional)**:

To run with `ipv6_agent`. create the symbolic link, use the following command:

```bash
ln -s main.py ipv6_agent
```

6. **Run with symbolic link**

```bash
  ./ipv6_agent
```

## Running the Docker Container

To run the Linux IPv6 Agent in a Docker container, follow these steps:

2. **Preparing the Agent Script**:

- Before building the Docker container, ensure that the main Python script (`main.py` by default) has the symbolic link `ipv6_agent`. This is necessary for the Dockerfile to locate the correct script to run.

- To create the symbolic link, use the following command:

- ```bash
  ln -s main.py ipv6_agent
  ```

1. **Build Docker Image**:

   - Navigate to the directory containing the Dockerfile and the agent script.
   - Run the following command to build the Docker image:
     ```bash
     docker build -t ipv6-agent .
     ```
   - This command will build a Docker image named `ipv6-agent` based on the instructions in the Dockerfile.

2. **Run Docker Container**:

   - Once the Docker image is built, you can run a Docker container using the following command:
     ```bash
     docker run -d ipv6-agent
     ```
   - This command will start a Docker container in detached mode, running the Linux IPv6 Agent script inside the container.

3. **Access Docker Container** (Optional):

   - If you need to access the Docker container to view logs or interact with the running agent, you can use the following command:
     ```bash
     docker exec -it <container-id> /bin/bash
     ```
   - Replace `<container-id>` with the ID or name of the running Docker container.

4. **Monitor Docker Container Logs** (Optional):
   - To monitor the logs generated by the running agent inside the Docker container, use the following command:
     ```bash
     docker logs -f <container-id>
     ```
   - Replace `<container-id>` with the ID or name of the running Docker container.
