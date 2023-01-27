# Bitnode (under-development)

## Setup the Development Environment

Steps to setup the developer environment are given below,
git and python (3.8+ recommended) are required.

1. Clone this repository
   ```bash
   git clone <repository-url>
   cd bitnode
   ```

2. Create a Virtual Environment (Optional)
   ```bash
   python3 -m venv .venv

   source .venv/bin/activate  # Linux or MacOS
   source .venv/bin/activate.bat  # Windows
   ```

3. Install requirements
   ```bash
   pip install -r requirements-dev.txt
   ```

4. To run the web app, run the following command inside bitnode folder
   ```bash
   cd bitnode
   uvicorn main:app
   ```
   or use aditional options
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 5000
   ```
