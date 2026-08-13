# School Website - Deployment Guide for Linux Server

This guide explains how to install, configure, and run both the Flask backend and the Vue.js frontend on a temporary Linux server (e.g., Ubuntu 20.04/22.04 LTS).

---

## 1. System Prerequisites

Connect to your server via SSH and install the required system packages:

```bash
# Update package list and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install Python 3, pip, venv, SQLite3, and Git
sudo apt install python3 python3-pip python3-venv sqlite3 git curl -y

# Install Node.js (NodeSource repository method)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Verify installations
python3 --version
pip3 --version
node -v
npm -v
```

---

## 2. Setting Up the Backend

Navigate to the project root directory where you uploaded the school website files.

### Step 2.1: Initialize Python Virtual Environment
Creating a virtual environment ensures Python packages are isolated:
```bash
# Navigate to backend directory
cd backend

# Create virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Step 2.2: Install Python Dependencies
Install the required packages within the active virtual environment:
```bash
pip install --upgrade pip
pip install Flask flask-cors Flask-SQLAlchemy
```

### Step 2.3: Initialize the Database
Run the database seed script to initialize schema tables and default values:
```bash
python init_db.py
```

### Step 2.4: Start the Backend Server (Development Mode)
You can start the backend directly to test it:
```bash
python app.py
```
*Note: The server will start on port `5000`.*

---

## 3. Setting Up the Frontend

Open a new terminal session or keep the backend running in the background.

### Step 3.1: Configure API Base URL
Before building the frontend, configure it to connect to the backend server.
1. Open the file `src/store/auth.js`.
2. Locate the `API_BASE_URL` variable definition:
   ```javascript
   const API_BASE_URL = 'http://192.168.0.103:5000/api'
   ```
3. Change `192.168.0.103` (or `localhost`) to your **public Linux Server IP address** or domain name:
   ```javascript
   const API_BASE_URL = 'http://<YOUR_SERVER_IP>:5000/api'
   ```

### Step 3.2: Install Node Dependencies
Go back to the root of the project folder:
```bash
# Navigate to the main directory containing package.json
cd ..

# Install packages
npm install
```

### Step 3.3: Build production assets
Compile the application to highly optimized static assets:
```bash
npm run build
```
This generates a `dist/` directory containing all optimized HTML, CSS, and JS assets.

### Step 3.4: Serve the Frontend
For a temporary server setup, you can quickly host the compiled folder using `serve`:
```bash
# Install serve globally
sudo npm install -g serve

# Serve the build folder on port 3000
serve -s dist -l 3000
```
Open a web browser and navigate to `http://<YOUR_SERVER_IP>:3000` to access the site.

---

## 4. Keeping Servers Running in Background (Optional)

If you close your SSH connection, the servers will stop running. To keep them alive in the background:

### Option A: Using Screen or Tmux
```bash
# Install screen
sudo apt install screen -y

# Start a screen session for the backend
screen -S backend
cd backend
source venv/bin/activate
python app.py
# Press Ctrl + A followed by D to detach screen

# Start a screen session for the frontend
screen -S frontend
serve -s dist -l 3000
# Press Ctrl + A followed by D to detach screen
```

### Option B: Run in Background with nohup
```bash
# For backend (run from backend folder with activated venv)
nohup python app.py > backend.log 2>&1 &

# For frontend (run from root directory)
nohup serve -s dist -l 3000 > frontend.log 2>&1 &
```
