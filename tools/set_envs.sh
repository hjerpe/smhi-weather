#!/bin/bash

# Parse and set the environment variables, and capture the variable names
SCRIPT_DIR_PARENT=$( cd -- "$( dirname -- "$(dirname -- "${BASH_SOURCE[0]}")" )" &> /dev/null && pwd )
VARS=$($SCRIPT_DIR_PARENT/tools/parse_environment_variables.py)

# Evaluate the export commands to set the environment variables
eval "$VARS"

# Strip away the 'export' keyword and store the result in EXPORTS
# Extract the variable names (the strings before the '=' sign)
VAR_NAMES=$(echo "$VARS" | awk -F'=' '{print $1}' | sed 's/export //')

# Dynamically echo the environment variables
echo "Echo the added/updated environment variables:"
for var_name in $VAR_NAMES; do
    echo "$var_name=${!var_name}"
done
