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
from imgdetect import grab_shop ,feed_pets,click_skip,find_and_click_eggs



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
proxy=getproxy_wwp.get_proxy_info('UK-11a9245b-5436-45ba-9cd4-4360b2e25ceb')
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

# selenium 3 version
# driver = Chrome(web_driver_path, chrome_options=chrome_options)

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
window_handles = driver.window_handles

# 遍历每个窗口句柄
for handle in window_handles:
    driver.switch_to.window(handle)
    title = driver.title
    print(f"Window Handle: {handle}, Title: {title}")

    # 如果标题是 "OKX Wallet"，则在该窗口中打开指定页面
    if title == "OKX Wallet":
        print("Found OKX Wallet window. Opening the extension page...")
        driver.get("chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize")
        break  # 退出循环

# 如果没有找到标题为 "OKX Wallet" 的窗口
else:
    print("No window with title 'OKX Wallet' found.")
time.sleep(3)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[3]/div/div[2]/button/span").click() #click the import button
time.sleep(2)

driver.find_element("xpath", "//*[@id='app']/div/div/div/div[3]/div/div[1]/div[2]/div").click() #click the creat button
time.sleep(2)                           #
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]").click() #click the privte key button
time.sleep(2)
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[2]/div/textarea").send_keys('0xf9e196e87a0bc3af8b3d325a9e5a307946184dcf18cd94c7a5743225af954163')
time.sleep(6)
time.sleep(2)
driver.find_element("xpath", "//*[@id='app']/div/div[2]/div/button").click() #click the confirm button
time.sleep(3)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/button/span").click() #click the confirm button again
time.sleep(3)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[2]/div[3]/div[2]/div/div[1]").click()   #select password
time.sleep(6)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[2]/div[5]/div/button").click() #click notrecommend button
time.sleep(6)
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
time.sleep(6)
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
time.sleep(6)
driver.find_element("xpath", "//*[@id='app']/div/div[2]/div/button").click()#click confirm button
time.sleep(15)
#driver.find_element("xpath", "//*[@id='app']/div/div/div/div[4]/div/button").click()#click start button
driver.close()
time.sleep(3)
driver.switch_to.window(window_handles[0])  # 切换到第1个标签页
#the next step is game automatic,i will test if it work without image recognition.just click
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/button/span").click() #click the play button
time.sleep(3)
driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
time.sleep(5)
# here is the problem, i can't click the okx wallet button, so i use the action chain to click the okx wallet button
actions = ActionChains(driver)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the okx wallet button')
actions.move_by_offset(606, 411).click().perform()    #click the okx wallet button
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'switch to the wallet window')
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(3)
#print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'refresh the wallet window')
#driver.refresh()
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'now to click the connect button')
driver.find_element("xpath", "//*[@id='app']/div/div/div/div/div[5]/div[2]/button[2]/span/div").click()  #click the connect button
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'switch to the first window')
driver.switch_to.window(window_handles[0])
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the arbitrum one button')
actions.move_by_offset(606, 187).click().perform()    #click the okx wallet button
time.sleep(6)
driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
time.sleep(6)
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the confirm button')
driver.find_element("xpath", "//*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span").click()
time.sleep(6)                          #//*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span
driver.switch_to.window(window_handles[0])
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the close button')
driver.find_element("xpath", "/html/body/div[5]/div/div/div/div[1]/button").click() #click the close button
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the first input box')
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/input").click() #click the input box
time.sleep(3)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the second input box')
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/input").click() #click the input box
time.sleep(10)
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[3]/button/span").click() #click the accept button
time.sleep(10)                           #/html/body/div[4]/div/div/div/div[3]/button/span
driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/input").send_keys('61eth')
time.sleep(2)
driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/button").click()
time.sleep(6)
# 定位目标元素
driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/div[2]/button").click()
time.sleep(6)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), '选蛋')
window_handles = driver.window_handles
# 切换到新窗口
# 前面的导入语句保持不变...

def get_element_center_coordinates(driver, element):
    """获取元素的中心坐标"""
    size = element.size
    location = element.location
    center_x = location['x'] + (size['width'] / 2)
    center_y = location['y'] + (size['height'] / 2)
    return center_x, center_y

# ... (之前的代码保持不变，直到 unity-canvas 交互部分) ...

# 切换到游戏窗口
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(16)  # 等待游戏加载
click_skip(driver, 10)

#下面开始多次循环找图做任务，直到完成500个点数的任务
for i in range(1, 500):
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
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")   #如果找不到就说明该宠物需要休息了，就开始需寻找休息的图标
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\play.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            time.sleep(13)
            ## 开始投喂，如果找不到就说明该宠物需要休息了，就开始需寻找休息的图标
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\feed.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"未能成功点击目标:feed.bmp，开始喂食")
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食，这里要放很多食物的种类图标
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\berries.bmp",r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\feed2.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"找到食物点击以后识别下一步动作。。。")
                    #选择食物投喂
                    feed_pets(driver)
            #检测商店物品，全部收取
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\shop.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                #收取奖品
                grab_shop(driver)
            #所有任务完成以后点击图标进入下一个页面
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 进入下一个宠物界面
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\next.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"找到目标，坐标: next.bmp,进入下一个宠物界面")
        else:
            #没有任务，宠物开始休息
            print(f"未能成功点击目标:play.bmp，开始寻找休息信息")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths={r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\rest.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"找到目标，坐标: rest.bmp")
            else:
                print(f"未能成功点击目标:rest.bmp")
    except Exception as e:
        print(f"发生错误: {e}")

