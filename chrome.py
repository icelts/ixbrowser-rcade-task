import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from imgdetect import (
    grab_shop, feed_pets, click_skip, find_and_click_eggs,
    setup_pet, rest_all_pets, import_wallet, capture_and_find_egg, import_wallet_3, safe_click
)


def read_wallet_keys(filepath):
    """Read wallet keys from file"""
    keys_data = []
    with open(filepath, 'r') as file:
        for line in file:
            keys_data.append(line.strip())
    return keys_data


def log_failed_key(key_data, error_msg=''):
    """Log failed key data to a file"""
    with open('failed_keys.txt', 'a') as f:
        f.write(f"{key_data},{error_msg}\n")


def run_game_automation(key_data, task_queue):
    """Run game automation for a single profile"""
    driver = None

    try:
        parts = key_data.split(',')
        private_key = parts[2] if len(parts) >= 3 else None

        if not private_key:
            raise ValueError("Invalid key data format")

        # Setup Selenium WebDriver with proxy and extensions
        chrome_options = Options()

        # 1. 设置固定分辨率
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--disable-extensions-http-throttling")
        # 2. 加载钱包插件（例如 MetaMask）
        extension_path = r"C:\Users\a2720\Desktop\okx.crx"  # 替换为你的 MetaMask 插件路径
        chrome_options.add_extension(extension_path)

        # 3. 设置代理
        #proxy = "http://ip.mproxy.vn:12318"  # 替换为你的代理地址和端口
        #username = "cashbag"  # 替换为你的代理用户名
        #password = "bfLMEm6kMlgZ34E"  # 替换为你的代理密码
        #chrome_options.add_argument(f"--proxy-server={proxy}")

        # 其他 Chrome 选项
        chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
        chrome_options.add_argument("--disable-infobars")  # 禁用信息栏
        #chrome_options.add_argument("--disable-notifications")  # 禁用通知

        # 设置 ChromeDriver 路径
        web_driver_path = r"C:\Users\a2720\AppData\Roaming\ixBrowser-Resources\chrome\130-0003\chromedriver.exe"  # 替换为你的 ChromeDriver 路径
        driver = Chrome(service=Service(web_driver_path), options=chrome_options)

        # Navigate to game and perform automation
        driver.get("https://hatchlings.revolvinggames.com/?cache=false")
        time.sleep(15)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])

        # Import wallet
        import_wallet_3(driver, private_key)
        time.sleep(6)

        # Game automation logic (similar to original script)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        time.sleep(20)
        safe_click(driver, "//*[@id='unity-fullscreen-button']", "打开全屏")
        #需要判断flash页面是否完全加载，才能连续点击，循环20次，每次等待6秒
        time.sleep(6)
        click_skip(driver, 20)
        print(f"进入游戏")
        # [Rest of the original game automation logic]
        # ... (copy the entire game automation block from the previous script)
        # 下面开始多次循环找图做任务，直到完成500个点数的任务
        for i in range(1, 3):
            try:  # 循环找图，直到找到目标并点击成功
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = "imgs/wallet.bmp"
                found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                if found:  # 钱包没有导入成功
                    print(f"钱包没有导入成功，结束当前任务线程")
                    driver.quit()
                    return
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = "imgs/evolve.bmp"
                found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                if found:  # 满级，需要付费升级宠物
                    print(f"已经满级，需要付费升级宠物,查看下一个页面的宠物状态")
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                    template_paths = ["imgs/next.bmp"]
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                # 游戏初始化，选择并激活宠物
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = ["imgs/egg.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                    template_paths = ["imgs/hatch.bmp"]
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                    if found:
                        print(f"新宠物激活成功")
                        time.sleep(5)
                        click_skip(driver, 20)  # 连续点击20次才会进入交互界面
                    else:
                        print(f"未能成功点击目标:hatch.bmp")
                else:
                    print(f"未能成功点击目标:egg.bmp")
                print(f"进入任务，开始循环找图")
                # 所有的动作从play开始，如果找不到就让宠物休息，找到以后依次play,喂养，shop领取，egg激活，玩具放置，然后点击下一个页面进去喂养
                for i in range(1, 10):
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 直接play6次
                    template_paths = ["imgs/play.bmp"]
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                    if found:
                        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                        template_paths = "imgs/full.bmp"
                        found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                        if found:
                            time.sleep(5)
                            break
                        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                        template_paths = "imgs/nohatch.bmp"   #当前页面没有宠物
                        found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                        if found:
                            time.sleep(5)
                            break
                    time.sleep(10)
                ## 开始清洗
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                template_paths = ["imgs/clean.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                time.sleep(10)
                ## 开始投喂
                for i in range(1, 3):
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                    template_paths = ["imgs/feed.bmp"]
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                    if found:
                        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                        template_paths = "imgs/nohatch.bmp"   #当前页面没有宠物
                        found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths, threshold=0.8)
                        if found:
                            time.sleep(5)
                            break
                        print(f"成功点击目标:feed.bmp，开始喂食")
                        feed_pets(driver) # 喂养宠物
                # 检测商店物品，全部收取
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                template_paths = ["imgs/shop.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    # 收取奖品
                    grab_shop(driver)
                else:
                    print(f"没有找到目标:shop.bmp")
                # 检测龙蛋页面，有蛋就激活，并直接释放宠物，如果当前页面有宠物就切换到下一个页面
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                template_paths = ["imgs/longdanjihuo.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"打开龙蛋界面,开始激活龙蛋")
                    setup_pet(driver)
                else:
                    print(f"没有找到目标:longdanjihuo.bmp")

                # 所有任务完成以后点击图标进入下一个页面
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 进入下一个宠物界面
                template_paths = ["imgs/next.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"找到目标，坐标: next.bmp,进入下一个宠物界面,进入下一个任务循环")
                    time.sleep(5)

            except Exception as e:
                print(f"发生错误: {e}")
        # Rest all pets and cleanup
        rest_all_pets(driver)
        return True

    except Exception as e:
        print(f"Automation error for key {private_key}: {e}")
        log_failed_key(key_data, str(e))
        traceback.print_exc()
        return False

    finally:
        # Ensure cleanup happens regardless of success or failure
        try:
            if driver:
                driver.quit()
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")


def main(keys_file, num_threads):
    """Run multi-threaded game automation"""
    # Read private keys
    private_keys = read_wallet_keys(keys_file)

    # Use ThreadPoolExecutor for managing threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for each private key with a delay
        for key in private_keys:
            executor.submit(run_game_automation, key, None)
            time.sleep(20)  # 3-second delay between thread starts


if __name__ == "__main__":
    KEYS_FILE = 'private_keys.txt'
    NUM_THREADS = 10

    main(KEYS_FILE, NUM_THREADS)