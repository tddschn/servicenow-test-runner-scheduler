#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-07-06
Purpose: ServiceNow - Start ATF test runner in browser
"""

import argparse
import sys
from threading import Thread
from time import sleep
from . import __version__, __app_name__
from .utils import start_runner
from .config import (
    get_settings,
    CLIENT_TEST_RUNNER_URL_PATH,
    SCHEDULED_TEST_RUNNER_URL_PATH,
    BROWSER_ACTION_INTERVAL,
    CHECKING_INTERVAL,
    NUM_INSTANCE,
    RESTART_INTERVAL,
    TOLERANCE,
)

counter = 0


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description='ServiceNow - Start ATF test runner in browser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
    )

    parser.add_argument('-n', '--dry-run', help='Dry run', action='store_true')
    parser.add_argument(
        '-s',
        '--scheduled-runner',
        help='Start a scheduled runner (default: Client test runner)',
        action='store_true',
    )
    # parser.add_argument('-e', '--env', help='path to the .env file', default='.env')

    return parser.parse_args()


def main() -> None:
    args = get_args()
    dry_run = args.dry_run
    scheduled_runner = args.scheduled_runner
    threads = []
    global counter
    kwargs = dict(
        dry_run=dry_run,
        scheduled_runner=scheduled_runner,
    )
    fixed_interval_kwargs = kwargs | dict(close_after=RESTART_INTERVAL)
    for initial_close_after in range(
        RESTART_INTERVAL // NUM_INSTANCE,
        RESTART_INTERVAL + 1,
        RESTART_INTERVAL // NUM_INSTANCE,
    ):
        counter += 1
        initial_kwargs = kwargs | dict(close_after=initial_close_after, counter=counter)
        t = Thread(target=start_runner, kwargs=initial_kwargs)
        threads.append(t)
        t.start()

    while 1:
        for t in threads:
            if not t.is_alive():
                threads.remove(t)
                counter += 1
                new_t = Thread(
                    target=start_runner,
                    kwargs=fixed_interval_kwargs | dict(counter=counter),
                )
                threads.append(new_t)
                new_t.start()
        sleep(CHECKING_INTERVAL)


# def main_wrapper():
#     main(counter=counter)


if __name__ == '__main__':
    # main_wrapper()
    main()
