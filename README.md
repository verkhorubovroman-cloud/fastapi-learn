# FastAPI-Learn Project

My daily project for learning and developing with **FastAPI**.

## 🚀 Step-by-Step Launch Guide

### Prerequisites
Before you begin, make sure you have **Python** installed on your system.
* **Check if Python is installed:**
  Open your terminal and run:
  ```bash
  python --version
  ```
  or
  ```bash
  python3 --version
  ```
* **If not installed:** Download and install the latest stable version from the official website: [python.org](https://python.org). *Note for Windows users: Ensure you check the box **"Add python.exe to PATH"** during installation.*

### Step 1. Preparation and Environment Creation
Open a terminal on your computer and run the following commands in sequence:

1. **Navigate to the project folder** (replace with your actual path):
   ```bash
   cd path/to/your/folder/fastapi-learn
   ```
2. **Create a virtual environment** (`venv`):
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment**:
   * For **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   * For **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

### Step 2. Installing Libraries
Once the environment is activated (you will see `(venv)` at the beginning of your terminal line), install FastAPI itself:
```bash
pip install fastapi
```
*(When installing the `fastapi` package in newer versions, the startup tools and the `uvicorn` server are installed automatically).*

### Step 3. Launching the Server
To start the server, use one of the new commands (depending on your needs):

* **For development** (the server will auto-reload whenever the code changes):
  ```bash
  fastapi dev main.py
  ```
* **For standard launch** (without auto-reload):
  ```bash
  fastapi run main.py
  ```

### Step 4. Checking in the Browser
* Main page: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* API Documentation (Swagger): [http://127.0.0](http://127.0.0)


The description inside the code is in Russian because I'm from Russia.
