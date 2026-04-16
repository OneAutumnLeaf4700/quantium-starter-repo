import os
from webdriver_manager.chrome import ChromeDriverManager

def pytest_configure(config):
    driver_path = ChromeDriverManager().install()
    os.environ["PATH"] = os.path.dirname(driver_path) + os.pathsep + os.environ["PATH"]
