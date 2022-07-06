from functools import cache
from pydantic import BaseSettings

# cSpell:disable
SCHEDULED_TEST_RUNNER_URL_PATH = '/now/nav/ui/classic/params/target/atf_test_runner.do%3Fsysparm_nostack%3Dtrue%26sysparm_scheduled_tests_only%3Dtrue'
CLIENT_TEST_RUNNER_URL_PATH = (
    "/now/nav/ui/classic/params/target/atf_test_runner.do%3Fsysparm_nostack%3Dtrue"
)
# cSpell:enable


class Settings(BaseSettings):
    INSTANCE: str = ''
    USERID: str = ''
    PASSWORD: str = ''
    RESTART_INTERVAL: int = 7200
    TOLERANCE: int = 300
    NUM_INSTANCE: int = 6
    CHECKING_INTERVAL: int = 300
    BROWSER_ACTION_INTERVAL: int = 5

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings from .env:")
    print(f'    Instance: {settings.INSTANCE}')
    print(f'    userid: {settings.USERID}')
    return settings


RESTART_INTERVAL = get_settings().RESTART_INTERVAL
TOLERANCE = get_settings().TOLERANCE
NUM_INSTANCE = get_settings().NUM_INSTANCE
CHECKING_INTERVAL = get_settings().CHECKING_INTERVAL
BROWSER_ACTION_INTERVAL = get_settings().BROWSER_ACTION_INTERVAL

# counter = 0
