"""
File:
    logger.py

Purpose:
    Lightweight debugging utilities.

Responsibilities:
    - Agent lifecycle logging
    - Raw output logging
    - Parsed output logging
"""

import json


LINE = "=" * 80


def log_agent_start(agent_name: str):

    print(LINE)
    print(f"Running Agent : {agent_name}")
    print(LINE)


def log_raw_output(agent_name: str, output):

    print(f"\nRAW OUTPUT ({agent_name})")

    if isinstance(output, (dict, list)):
        print(json.dumps(output, indent=2))
    else:
        print(output)

    print()


def log_parsed_output(agent_name: str, parsed):

    print(f"\nPARSED OUTPUT ({agent_name})")

    print(json.dumps(parsed, indent=2))

    print()


def log_error(agent_name: str, error):

    print(f"\nERROR ({agent_name})")

    print(error)

    print(LINE)
