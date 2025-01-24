import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile, Proxy, Preference, Fingerprint, Consts
from examples import getproxy_wwp
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from imgdetect import grab_shop ,feed_pets,click_skip,find_and_click_eggs,setup_pet,rest_all_pets,import_wallet,capture_and_find_egg


c = IXBrowserClient()
c.show_request_log = True

#copy a profile id first
profile_id = 49
name = 'rcade' + str(int(time.time()))
site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE

result = c.create_profile_by_copying(profile_id, name, site_id=site_id)
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Create Profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'result:', result)

#setup the profile proxy
proxy=getproxy_wwp.get_proxy_info('UK-c972c39e-fb52-42b8-aa06-5c9a45522001')
proxy_type = 'direct'
proxy_ip = proxy['ip']
proxy_port = proxy['port']

data = c.update_profile_to_custom_proxy_mode(result, proxy_type, proxy_ip, proxy_port)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)

#start the profile
open_result = c.open_profile(result, cookies_backup=False, load_profile_info_page=False)
if open_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Open profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
# time.sleep(30)
web_driver_path = open_result['webdriver']
debugging_address = open_result['debugging_address']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugging_address)

# selenium 4 and above
driver = Chrome(service=Service(web_driver_path), options=chrome_options)

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Visit the ixBrowser homepage by default')
driver.get("https://hatchlings.revolvinggames.com/?cache=false")
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Automatically exit after 30 seconds')
time.sleep(15)
window_handles = driver.window_handles
# 切换到新窗口
driver.switch_to.window(window_handles[-1])
# 关闭新窗口
#driver.close()

#driver.switch_to.window(window_handles[1])  # 切换到第二个标签页
print("第二个标签页,start to setup wallet:", driver.title)
time.sleep(3)

#import the wallet
import_wallet(driver,'0x1daf02711d8dd2dfe9470d68fb4800720d5fb98eceb715311cdf001465d4882a')

time.sleep(6)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), '选蛋')
window_handles = driver.window_handles

# 切换到游戏窗口
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(16)  # 等待游戏加载
click_skip(driver, 13)

#下面开始多次循环找图做任务，直到完成500个点数的任务
for i in range(1, 2):
    try:  # 循环找图，直到找到目标并点击成功
        #选择龙蛋点击
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths ={r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\egg.bmp"}
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

        #所有的动作从play开始，如果找不到就让宠物休息，找到以后依次play,喂养，shop领取，egg激活，玩具放置，然后点击下一个页面进去喂养
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
        #检测龙蛋页面，有蛋就激活，并直接释放宠物，如果当前页面有宠物就切换到下一个页面
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\longdanjihuo.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"打开龙蛋界面,开始激活龙蛋")
            setup_pet(driver)

        #所有任务完成以后点击图标进入下一个页面
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 进入下一个宠物界面
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\next.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"找到目标，坐标: next.bmp,进入下一个宠物界面,进入下一个任务循环")
            time.sleep(5)

    except Exception as e:
        print(f"发生错误: {e}")
#所有宠物都设置为休息状态
rest_all_pets(driver)

#关闭浏览器
driver.quit()
print("任务完成，浏览器已关闭")
c.close_profile(result)