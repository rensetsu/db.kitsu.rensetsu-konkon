from sys import exit as sysexit
from time import time
from traceback import print_exc

from consts import Status, pprint
from librensetsu.humanclock import convert_float_to_time
from loops import do_loop


def main() -> None:
    """Main process of the util"""
    start = time()
    ex = 0
    pprint.print(Status.INFO, "Starting...")
    try:
        do_loop()
    except Exception as e:
        pprint.print(Status.ERR, f"An error occurred: {e}")
        print_exc()
        ex = 1
    end = time()
    pprint.print(
        Status.INFO, f"Time elapsed: {convert_float_to_time(end - start)}"
    )
    sysexit(ex)


if __name__ == "__main__":
    main()
