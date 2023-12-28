#!/bin/bash

# Set the path to your virtual environment
SCRIPT_DIR_PARENT=$( cd -- "$( dirname -- "$(dirname -- "${BASH_SOURCE[0]}")" )" &> /dev/null && pwd )
venv_path="$SCRIPT_DIR_PARENT/venvs"
default_venv="default_venv"
echo "$venv_path/$default_venv"
# Check if the virtual environment directory does not exists
if [ ! -d "$venv_path/$default_venv" ] ; then
    echo "Virtual environment does not exist"
    echo "Create environment $venv_path/$default_venv"
    python3 -m venv $venv_path/$default_venv --system-site-packages --upgrade-deps
    source "$venv_path/$default_venv/bin/activate"
    echo "Installing requirements.txt"
    pip3 install -r requirements.txt
    echo "Install pre-commit hooks"
    pre-commit install
    pip3 install ipykernel
    echo "Create ipykernel $default_venv"
    # Install ipykernel
    python3 -m ipykernel install --user --name=$default_venv
fi
echo "Activating environment: $venv_path/$default_venv/bin/activate"
source "$venv_path/$default_venv/bin/activate"
