import argparse

from build import __all__
from build import *


def main():
    parser = argparse.ArgumentParser(
        description=f"Build and format files. Selectable commands: {', '.join(__all__)}"
    )
    parser.add_argument("command", help="Command to execute")
    args = parser.parse_args()

    if args.command in __all__:
        globals()[args.command]()
    else:
        print(f"Error: '{args.command}' is not a valid command.")


if __name__ == "__main__":
    main()
