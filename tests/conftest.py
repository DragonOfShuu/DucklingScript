from platform import system
from pytest import Session
import os

def pytest_sessionstart(session: Session):
    # We need to set the display here because
    # when testing occurs on github workflows,
    # the display variable is non-existent
    if system() == "Linux":
        os.environ['DISPLAY'] = ":0"
