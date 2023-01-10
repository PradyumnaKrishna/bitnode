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

3. Install requirmenets and bitnode tool
   ```bash
   pip install -r requirements-dev.txt

   pip install -e .
   ```

4. Start testing the tool
   ```bash
   bitnode
   ```
