# School Website - Docker Deployment Guide

This guide explains how to install, build, and deploy the frontend and backend of the school portal using Docker and Docker Compose as separate container instances.

---

## 1. Prerequisites

Make sure Docker and Docker Compose are installed on your Linux server:

```bash
# Update packages
sudo apt update

# Install Docker
sudo apt install docker.io -y

# Install Docker Compose
sudo apt install docker-compose -y

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 2. Configuration Setup

Before running the containers, you need to configure the frontend to talk to the backend container's exposed port.

1. Open the file `src/store/auth.js`.
2. Locate the `API_BASE_URL` variable definition:
   ```javascript
   const API_BASE_URL = 'http://192.168.0.103:5000/api'
   ```
3. Update `192.168.0.103` (or `localhost`) with your **public Linux Server IP address** or domain name:
   ```javascript
   const API_BASE_URL = 'http://<YOUR_SERVER_IP>:5000/api'
   ```
*Note: Because the frontend code runs inside the user's browser, it must make network calls to the server's public IP address or hostname.*

---

## 3. Build and Run Containers

Run the following commands in the root directory (where `docker-compose.yml` is located):

```bash
# Build the Docker images for frontend and backend
docker-compose build

# Start the containers in detached (background) mode
docker-compose up -d
```

---

## 4. Managing the Containers

Here are useful commands to manage your running Docker containers:

```bash
# Check the status of running containers
docker-compose ps

# View real-time output logs
docker-compose logs -f

# View logs for a specific service (e.g. backend)
docker-compose logs -f backend

# Stop the running services
docker-compose down

# Stop and remove all volumes (WARNING: This resets the SQLite database)
docker-compose down -v
```

---

## 5. Network & Port Access

Ensure the following ports are open in your server firewall / security group:
- **Port `80`**: For accessing the frontend web application (`http://<YOUR_SERVER_IP>`).
- **Port `5000`**: For receiving API calls from the client's browser (`http://<YOUR_SERVER_IP>:5000`).
