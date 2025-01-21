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
proxy=getproxy_wwp.get_proxy_info('UK-42486f50-cc43-4a01-8190-8e26f2c379ae')
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
time.sleep(30)
window_handles = driver.window_handles
# 切换到新窗口
driver.switch_to.window(window_handles[-1])
# 关闭新窗口
driver.close()

driver.switch_to.window(window_handles[1])  # 切换到第二个标签页
print("第二个标签页,start to setup wallet:", driver.title)
time.sleep(3)
driver.get("chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize")
time.sleep(3)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[3]/div/div[2]/button/span").click() #click the import button
time.sleep(2)

driver.find_element("xpath", "//*[@id='app']/div/div/div/div[3]/div/div[1]/div[2]/div").click() #click the creat button
time.sleep(2)                           #
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]").click() #click the privte key button
time.sleep(2)
driver.find_element("xpath", "//*[@id='app']/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[2]/div/textarea").send_keys('0xa86cbe31a1819533fc4d4a927078cada175c8c453230af2b012c52016b89d155')
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
time.sleep(10)
driver.find_element("xpath", "//*[@id='app']/div/div/div/div[4]/div/button").click()#click start button
time.sleep(3)
driver.switch_to.window(window_handles[0])  # 切换到第1个标签页
#the next step is game automatic,i will test if it work without image recognition.just click
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/button/span").click() #click the play button
time.sleep(3)
driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
time.sleep(3)
driver.find_element("By.css_selector", "wui-wallet-image[name='OKX Wallet']").click()
#driver.find_element("By.css_selector", "document.querySelectorAll('html > body > w3m-modal')[0].shadowRoot.querySelectorAll('wui-flex > wui-card > w3m-router')[0].shadowRoot.querySelectorAll('div > w3m-connect-view')[0].shadowRoot.querySelectorAll('wui-flex > wui-flex > w3m-connector-list')[0].shadowRoot.querySelectorAll('wui-flex > w3m-connect-injected-widget')[0].shadowRoot.querySelectorAll('wui-flex > wui-list-wallet')[0].shadowRoot.querySelectorAll('button')[0]").click()
#driver.find_element("xpath", "/html/body/w3m-modal//wui-flex/wui-card/w3m-router//div/w3m-connect-view//wui-flex/wui-flex/w3m-connector-list//wui-flex/w3m-connect-injected-widget//wui-flex/wui-list-wallet//button").click()
time.sleep(3)
driver.switch_to.window(window_handles[1])
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element("xpath", "//*[@id='app-content']/div/div/div/div[2]/div/div[3]/div/div[2]/button[2]").click()  #click the connect button
time.sleep(6)
driver.switch_to.window(window_handles[0])
time.sleep(3)
driver.find_element("xpath", "/html/body/w3m-modal//wui-flex/wui-card/w3m-router//div/w3m-unsupported-chain-view//wui-flex/wui-flex[2]/wui-list-network//button/wui-flex/wui-text").click()
time.sleep(3)
driver.switch_to.window(window_handles[1])
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element("xpath", "//*[@id='app-content']/div/div/div/div[2]/div/button[2]").click()  #click the connect button
time.sleep(6)
driver.switch_to.window(window_handles[0])
time.sleep(3)
driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
time.sleep(3)
driver.switch_to.window(window_handles[1])
time.sleep(3)
driver.refresh()
time.sleep(3)
driver.find_element("xpath", "//*[@id='app-content']/div/div/div/div/div[3]/button[2]").click()
time.sleep(6)
driver.switch_to.window(window_handles[0])
time.sleep(3)
driver.find_element("xpath", "/html/body/div[5]/div/div/div/div[1]/button").click() #click the close button
time.sleep(3)
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/input").click() #click the input box
time.sleep(3)
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]").click() #click the input box
time.sleep(3)
driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[3]/button").click() #click the accept button
time.sleep(3)
driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/input").send_keys('61eth')
time.sleep(2)
driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/button").click()
time.sleep(6)
# 定位目标元素
driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/div[2]/button").click()

