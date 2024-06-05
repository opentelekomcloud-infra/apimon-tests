# latest_rds_version2.py

import json
import sys


def find_latest_version(datastores):
    max_version = max(datastores, key=lambda x: float(x['name']))
    return max_version['name']


if __name__ == "__main__":
    try:
        # Check if there are at least two command-line arguments
        # (script name + JSON data)
        if len(sys.argv) > 1:
            # Load JSON data from the command-line arguments
            rds_datastores = json.loads(sys.argv[1])

            # Find the latest version
            latest_version = find_latest_version(rds_datastores)

            # Print the result
            print(latest_version, end='')
        else:
            raise ValueError(
                "Error: Missing JSON data as a command-line argument.")
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error - {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
