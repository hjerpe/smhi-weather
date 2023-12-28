#!/usr/bin/env python3

import os
import sys
from typing import Any, Dict

import click
import yaml


def parse_env_file_to_environment_variables(filename: str) -> Dict:
    """
    Parses an environment file and sets the environment variables accordingly.

    Args:
        filename (str): The path to the environment file.

    Returns:
        Dict: A dictionary containing the environment variables parsed from the file.
    """
    data = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            os.environ[key] = value.strip('"')
            data[key] = value.strip('"')
        return data


def parse_yaml_file_to_environment_variables(filename: str) -> Dict:
    """
    Parses a YAML file and sets the environment variables accordingly.

    Args:
        filename (str): The path to the YAML file.

    Returns:
        Dict: A dictionary containing the environment variables parsed from the file.
    """
    with open(filename, "r") as file:
        data: Dict[str, Any] = yaml.safe_load(file)
        for key, value in data.items():
            os.environ[key] = value
        return data


def get_parent_directory():
    # Get the main file's path
    main_file_path = sys.argv[0]
    # Convert to absolute path
    abs_path = os.path.abspath(main_file_path)
    # Get the directory of the main file
    main_file_directory = os.path.dirname(abs_path)
    # Get the parent directory
    parent_directory = os.path.dirname(main_file_directory)
    return parent_directory


@click.command()
@click.option(
    "-f",
    "--file",
    default=f"{get_parent_directory()}/configs/config-ver.yml",
    type=click.Path(exists=True),
    help="Path to the YAML or .env file",
)
def main(file: str) -> None:
    """
    Parses an environment file (either a YAML or .env file) and sets the environment variables accordingly.

    Args:
        file (str): The path to the environment file.

    Returns:
        None
    """
    exports = []

    if file.endswith(".env"):
        with open(file, "r") as f:
            exports = [f"export {line.strip()}" for line in f]
    elif file.endswith(".yaml") or file.endswith(".yml"):
        with open(file, "r") as f:
            data: Dict[str, Any] = yaml.safe_load(f)
            exports = [f"export {key}='{value}'" for key, value in data.items()]
    else:
        click.echo(f"Unsupported file type: {file}")
        return

    for export in exports:
        click.echo(export)


if __name__ == "__main__":
    main()
