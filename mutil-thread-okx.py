import sys
import time
import threading
import queue
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import json

from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Consts
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)


class AutomationTask:
    def __init__(self, proxy_key: str, private_key: str):
        self.proxy_key = proxy_key
        self.private_key = private_key
        self.client = IXBrowserClient()
        self.client.show_request_log = True
        self.logger = logging.getLogger(__name__)

    def setup_profile(self) -> dict:
        profile_id = 49
        name = f'rcade_{int(time.time())}_{threading.current_thread().name}'
        site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE

        result = self.client.create_profile_by_copying(profile_id, name, site_id=site_id)
        if result is None:
            raise Exception(f"Failed to create profile: {self.client.message}")

        return result

    def setup_proxy(self, profile_result: str):
        proxy = self._get_proxy_info(self.proxy_key)
        data = self.client.update_profile_to_custom_proxy_mode(
            profile_result,
            'direct',
            proxy['ip'],
            proxy['port']
        )
        if data is None:
            raise Exception(f"Failed to update proxy: {self.client.message}")
        return data

    def _get_proxy_info(self, proxy_key: str) -> Dict:
        # Implement your proxy info retrieval logic here
        # This is a placeholder - replace with actual implementation
        return {'ip': 'proxy_ip', 'port': 'proxy_port'}

    def automate_browser(self):
        try:
            profile_result = self.setup_profile()
            self.setup_proxy(profile_result)

            open_result = self.client.open_profile(
                profile_result,
                cookies_backup=False,
                load_profile_info_page=False
            )

            if open_result is None:
                raise Exception(f"Failed to open profile: {self.client.message}")

            driver = self._setup_driver(open_result)
            self._perform_automation(driver)

        except Exception as e:
            self.logger.error(f"Automation failed: {str(e)}")
            self._save_failed_key()
            raise

    def _setup_driver(self, open_result: dict) -> Chrome:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", open_result['debugging_address'])
        return Chrome(service=Service(open_result['webdriver']), options=chrome_options)

    def _perform_automation(self, driver: Chrome):
        # Implementation of all the browser automation steps
        # This is where you'll put all the existing automation code
        # Breaking it down into smaller methods would be beneficial
        pass

    def _save_failed_key(self):
        with open('failed_keys.txt', 'a') as f:
            f.write(f"{self.private_key}\n")


class AutomationManager:
    def __init__(self, num_threads: int):
        self.num_threads = num_threads
        self.proxy_keys = self._load_proxy_keys()
        self.private_keys = self._load_private_keys()
        self.task_queue = queue.Queue()

    def _load_proxy_keys(self) -> List[str]:
        with open('proxy_keys.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def _load_private_keys(self) -> List[str]:
        with open('private_keys.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def prepare_tasks(self):
        for proxy_key, private_key in zip(self.proxy_keys, self.private_keys):
            self.task_queue.put((proxy_key, private_key))

    def run_task(self, proxy_key: str, private_key: str):
        task = AutomationTask(proxy_key, private_key)
        try:
            task.automate_browser()
        except Exception as e:
            logging.error(f"Task failed with proxy {proxy_key}: {str(e)}")

    def start(self):
        self.prepare_tasks()

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            while not self.task_queue.empty():
                proxy_key, private_key = self.task_queue.get()
                executor.submit(self.run_task, proxy_key, private_key)
                self.task_queue.task_done()


def main():
    # Create necessary files if they don't exist
    Path('failed_keys.txt').touch(exist_ok=True)

    # Number of threads to run simultaneously
    NUM_THREADS = 3  # Adjust this number based on your needs

    manager = AutomationManager(NUM_THREADS)
    manager.start()


if __name__ == "__main__":
    main()