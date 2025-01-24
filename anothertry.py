import sys
import time
import threading
import queue
import csv
from concurrent.futures import ThreadPoolExecutor

import sys

sys.path.insert(0, sys.path[0] + "/../")
from ixbrowser_local_api import IXBrowserClient, Profile, Proxy, Preference, Fingerprint, Consts
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Import your existing game interaction functions
from imgdetect import (
    grab_shop, feed_pets, click_skip, find_and_click_eggs,
    setup_pet, rest_all_pets, import_wallet, capture_and_find_egg
)


def read_wallet_keys(filepath):
    """
    Read wallet private keys from a CSV-like file.
    Expects format: data1,data2,private_key
    """
    private_keys = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                private_keys.append(parts[2])
    return private_keys


def run_game_automation(private_key, profile_id, task_queue):
    """
    Run game automation for a single profile
    """
    c = IXBrowserClient()
    c.show_request_log = True

    name = f'rcade_{int(time.time())}_{hash(private_key)}'
    site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE

    # Create profile
    result = c.create_profile_by_copying(profile_id, name, site_id=site_id)
    if result is None:
        print(f"Profile creation failed: {c.message}")
        return

    # Open profile
    open_result = c.open_profile(result, cookies_backup=False, load_profile_info_page=False)
    if open_result is None:
        print(f"Profile open failed: {c.message}")
        return

    try:
        # Setup Selenium WebDriver
        web_driver_path = open_result['webdriver']
        debugging_address = open_result['debugging_address']
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugging_address)
        driver = Chrome(service=Service(web_driver_path), options=chrome_options)

        # Navigate to game
        driver.get("https://hatchlings.revolvinggames.com/?cache=false")
        time.sleep(15)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])

        # Import wallet
        import_wallet(driver, private_key)
        time.sleep(6)

        # Game automation logic (similar to original script)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        time.sleep(16)
        click_skip(driver, 13)

        # Perform game tasks (your existing logic)
        # 下面开始多次循环找图做任务，直到完成500个点数的任务
        for i in range(1, 2):
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
                    print(f"找到目标，坐标: next.bmp,进入下一个宠物界面,进入下一个任务循环")
                    time.sleep(5)

            except Exception as e:
                print(f"发生错误: {e}")

        # Rest all pets and cleanup
        rest_all_pets(driver)
        driver.quit()
        c.close_profile(result)

    except Exception as e:
        print(f"Automation error for key {private_key}: {e}")


def main(keys_file, profile_id, num_threads):
    """
    Main function to run multi-threaded game automation
    """
    # Read private keys
    private_keys = read_wallet_keys(keys_file)

    # Create a thread-safe queue for tasks if needed
    task_queue = queue.Queue()

    # Use ThreadPoolExecutor for managing threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for each private key
        futures = [
            executor.submit(run_game_automation, key, profile_id, task_queue)
            for key in private_keys
        ]

        # Wait for all tasks to complete
        for future in futures:
            future.result()


if __name__ == "__main__":
    # Example usage
    KEYS_FILE = 'private_keys.txt'  # Path to your keys file
    BASE_PROFILE_ID = 49  # Your base profile ID to copy
    NUM_THREADS = 5  # Number of concurrent threads

    main(KEYS_FILE, BASE_PROFILE_ID, NUM_THREADS)