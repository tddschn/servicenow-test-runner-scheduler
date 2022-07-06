#!/usr/bin/env python3

from functools import partial
from threading import Semaphore
from time import sleep
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


def print_append_current_time(counter: int, *args, **kwargs):
    import datetime

    print(f'{datetime.datetime.now()}:', f'Runner #{counter}:', *args, **kwargs)


sem = Semaphore(NUM_INSTANCE)


def start_client_runner(
    close_after: int,
    sem: Semaphore,
    counter: int,
    scheduled_runner: bool = False,
    dry_run: bool = False,
):
    with sem:
        if dry_run:
            print_append_current_time(
                counter,
                f'starting runner and will be running for {close_after} seconds',
            )
            sleep(close_after)
            print_append_current_time(counter, 'exiting')
            return
        print_append_current_time(counter, 'start of login')
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        import time

        sninstance = get_settings().INSTANCE.removesuffix('/')
        sninstanceuser = get_settings().USERID
        # cSpell:disable
        sninstancepwd = get_settings().PASSWORD
        # cSpell:enable
        if any(not x for x in (sninstance, sninstanceuser, sninstancepwd)):
            print_append_current_time(
                counter, 'Please create a .env in the same directory as this file'
            )
            print_append_current_time(
                counter,
                f'required fields for .env: instance, userid, password',
            )
            exit(1)
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(str(sninstance) + "/login.do")
        time.sleep(BROWSER_ACTION_INTERVAL)

        username = browser.find_element(By.ID, "user_name")
        password = browser.find_element(By.ID, "user_password")
        username.send_keys(str(sninstanceuser))
        password.send_keys(str(sninstancepwd))
        login_attempt = browser.find_element(By.ID, "sysverb_login")
        login_attempt.click()
        print_append_current_time(counter, 'end of login')

        print_append_current_time(counter, 'logged in, now starting test runner')
        time.sleep(BROWSER_ACTION_INTERVAL)

        runner_url = sninstance + (
            SCHEDULED_TEST_RUNNER_URL_PATH
            if scheduled_runner
            else CLIENT_TEST_RUNNER_URL_PATH
        )
        # start runner
        print_append_current_time(counter, f'navigating to runner url: {runner_url}')
        browser.get(runner_url)

        # close browser after close_after seconds
        time.sleep(close_after)
        browser.close()


start_runner = partial(start_client_runner, sem=sem)
