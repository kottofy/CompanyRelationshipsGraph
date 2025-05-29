
# Windows PowerShell commands to set up a virtual environment and install dependencies
cd $PSScriptRoot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
