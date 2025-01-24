import sys
import time
import threading
import queue
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List

import sys

sys.path.insert(0, sys.path[0] + "/../")

from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Consts
from examples import getproxy_wwp
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Import image recognition functions
from imgdetect import (
    grab_shop, feed_pets, click_skip, find_and_click_eggs,
    setup_pet, rest_all_pets, import_wallet, capture_and_find_egg
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game_automation.log'),
        logging.StreamHandler()
    ]
)


class GameAutomationTask:
    def __init__(self, private_key: str, proxy_info: dict):
        self.private_key = private_key
        self.proxy_info = proxy_info
        self.client = IXBrowserClient()
        self.client.show_request_log = True
        self.logger = logging.getLogger(threading.current_thread().name)

    def setup_profile(self):
        """Create a new browser profile"""
        profile_id = 49
        name = f'rcade_{int(time.time())}_{threading.current_thread().name}'
        site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE

        result = self.client.create_profile_by_copying(profile_id, name, site_id=site_id)
        if result is None:
            raise Exception(f"Failed to create profile: {self.client.message}")

        return result

    def setup_proxy(self, profile_result):
        """Configure proxy for the profile"""
        data = self.client.update_profile_to_custom_proxy_mode(
            profile_result,
            'direct',
            self.proxy_info['ip'],
            self.proxy_info['port']
        )
        if data is None:
            raise Exception(f"Failed to update proxy: {self.client.message}")
        return data

    def run_game_automation(self):
        """Main automation workflow"""
        try:
            # Create profile
            profile_result = self.setup_profile()

            # Setup proxy
            #self.setup_proxy(profile_result)

            # Open profile
            open_result = self.client.open_profile(
                profile_result,
                cookies_backup=False,
                load_profile_info_page=False
            )
            if open_result is None:
                raise Exception(f"Failed to open profile: {self.client.message}")

            # Setup WebDriver
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", open_result['debugging_address'])
            driver = Chrome(service=Service(open_result['webdriver']), options=chrome_options)

            # Navigate to game
            driver.get("https://hatchlings.revolvinggames.com/?cache=false")
            time.sleep(15)
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[-1])

            # Import wallet
            import_wallet(driver, self.private_key)
            time.sleep(6)
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[-1])
            time.sleep(16)  # 等待游戏加载
            click_skip(driver, 13)
            # Run game automation
            self._run_game_loop(driver)

            # Close everything
            driver.quit()
            self.client.close_profile(profile_result)
            self.logger.info("Game automation completed successfully")

        except Exception as e:
            self.logger.error(f"Automation failed: {str(e)}")
            self._save_failed_key()
            raise

    def _run_game_loop(self, driver):
        """Implement the game loop from the original script"""

        try:  # 循环找图，直到找到目标并点击成功
            # 选择龙蛋点击
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\egg.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\hatch.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    time.sleep(5)
                    click_skip(driver, 20)  # 连续点击20次才会进入交互界面
                else:
                    print(f"未能成功点击目标:hatch.bmp")
            else:
                print(f"未能成功点击目标:egg.bmp")

            # 所有的动作从play开始，如果找不到就让宠物休息，找到以后依次play,喂养，shop领取，egg激活，玩具放置，然后点击下一个页面进去喂养
            for i in range(1, 10):
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 直接play6次
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\play.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\full.bmp"}
                    found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                    if found:
                        break
                time.sleep(10)
            ## 开始清洗
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\clean.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            ## 开始投喂
            for i in range(1, 3):
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\feed.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"成功点击目标:feed.bmp，开始喂食")
                    feed_pets(driver)
            # 检测商店物品，全部收取
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\shop.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                # 收取奖品
                grab_shop(driver)
            # 检测龙蛋页面，有蛋就激活，并直接释放宠物，如果当前页面有宠物就切换到下一个页面
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\longdanjihuo.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"打开龙蛋界面,开始激活龙蛋")
                setup_pet(driver)

            # 所有任务完成以后点击图标进入下一个页面
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 进入下一个宠物界面
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\next.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"找到目标，坐标: next.bmp,进入下一个宠物界面")
            else:
                # 没有任务，宠物开始休息
                print(f"未能成功点击目标:play.bmp，开始寻找休息信息")
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\rest.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"找到目标，坐标: rest.bmp")
                else:
                    print(f"未能成功点击目标:rest.bmp")
        except Exception as e:
            print(f"发生错误: {e}")

        # Rest all pets at the end
        rest_all_pets(driver)

    def _save_failed_key(self):
        """Save failed private keys to a file"""
        with open('failed_keys.txt', 'a') as f:
            f.write(f"{self.private_key}\n")


class AutomationManager:
    def __init__(self, num_threads: int):
        self.num_threads = num_threads
        self.private_keys = self._load_private_keys()
        self.proxies = self._load_proxies()
        self.task_queue = queue.Queue()

    def _load_private_keys(self) -> List[str]:
        """
        Load private keys from a file where each line is comma-separated,
        and the private key is the third element.

        Example line format:
        data1,data2,0x1234567890abcdef,data4
        """
        private_keys = []
        with open('private_keys.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        private_keys.append(parts[2])
                    else:
                        logging.warning(f"Skipping invalid line: {line}")
        return private_keys

    def _load_proxies(self) -> List[dict]:
        """Load proxy information"""
        # You'll need to modify this based on your proxy loading mechanism
        # This is a placeholder that uses getproxy_wwp
        #return [getproxy_wwp.get_proxy_info(f'UK-proxy-{i}') for i in range(len(self.private_keys))]

    def prepare_tasks(self):
        """Prepare tasks for threading"""
        for key, proxy in zip(self.private_keys, self.proxies):
            self.task_queue.put((key, proxy))

    def run_task(self, private_key: str, proxy: dict):
        """Run a single task"""
        task = GameAutomationTask(private_key, proxy)
        try:
            task.run_game_automation()
        except Exception as e:
            logging.error(f"Task failed for key {private_key}: {str(e)}")

    def start(self):
        """Start the automation process"""
        self.prepare_tasks()

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            while not self.task_queue.empty():
                private_key, proxy = self.task_queue.get()
                executor.submit(self.run_task, private_key, proxy)
                self.task_queue.task_done()


def main():
    # Create necessary files if they don't exist
    Path('failed_keys.txt').touch(exist_ok=True)
    Path('private_keys.txt').touch(exist_ok=True)

    # Number of threads to run simultaneously
    NUM_THREADS = 5  # Adjust this number based on your needs and system capabilities

    manager = AutomationManager(NUM_THREADS)
    manager.start()


if __name__ == "__main__":
    main()