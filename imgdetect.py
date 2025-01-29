import numpy as np
from PIL import Image
import io
import sys
import os
import cv2
import threading
import traceback

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

sys.path.insert(0, sys.path[0]+"/../")
import logging
# 全局锁（可选）
opencv_io_lock = threading.Lock()

def capture_and_find_egg(driver, unity_canvas, template_path, threshold=0.75):
    """截取画布并查找目标蛋的位置"""
    try:
        # 1. 校验模板路径
        if not isinstance(template_path, str):
            raise TypeError(f"模板路径必须是字符串，实际类型：{type(template_path)}")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        # 2. 获取画布截图
        screenshot = unity_canvas.screenshot_as_png
        screenshot = Image.open(io.BytesIO(screenshot))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 3. 读取模板图片（加锁保护）
        with opencv_io_lock:
            template = cv2.imread(template_path)
            if template is None:
                raise ValueError(f"OpenCV无法读取图像: {template_path}")

        # 4. 模板匹配和结果处理
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return True, (center_x, center_y)
        else:
            return False, None

    except Exception as e:
        print(f"图像处理过程出错: {str(e)}")
        traceback.print_exc()
        return False, None

def find_and_click_eggs(driver, unity_canvas, template_paths, max_attempts=3):
    """查找并点击所有目标蛋"""
    # 0. 校验路径列表类型
    if not isinstance(template_paths, (list, tuple)):
        raise TypeError("template_paths 必须是列表或元组")

    for template_path in template_paths:
        for attempt in range(max_attempts):
            try:
                found, coordinates = capture_and_find_egg(driver, unity_canvas, template_path)
                if found and click_egg(driver, unity_canvas, coordinates):
                    return True
            except Exception as e:
                print(f"第 {attempt+1} 次尝试失败: {str(e)}")
            time.sleep(1)
    return False

def click_egg(driver, unity_canvas, coordinates):
    """
    点击指定坐标位置
    """
    try:
        actions = ActionChains(driver)

        # 获取画布位置信息
        canvas_location = unity_canvas.location

        # 计算相对于画布的偏移量
        canvas_size = unity_canvas.size
        offset_x = coordinates[0] - canvas_size['width'] / 2
        offset_y = coordinates[1] - canvas_size['height'] / 2

        # 移动到画布元素后进行相对偏移点击
        actions.move_to_element(unity_canvas) \
            .move_by_offset(offset_x, offset_y) \
            .click() \
            .perform()

        return True
    except Exception as e:
        print(f"点击过程出错: {str(e)}")
        return False


# 主要的执行函数

#设置点击次数，跳过游戏动画
def click_skip(driver,clicknumber):
    # 获取 unity canvas 元素
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")

    # 获取画布尺寸
    canvas_size = unity_canvas.size
    print(f"画布尺寸: {canvas_size}")

    # 计算画布内的安全点击坐标
    safe_offset_x = min(200, canvas_size['width'] - 50)  # 距离边缘保持50px
    safe_offset_y = min(200, canvas_size['height'] - 50)  # 距离边缘保持50px

    actions = ActionChains(driver)
    # 多次点击并进行错误处理
    for i in range(1, clicknumber):
        try:
            # 相对于画布元素移动到安全坐标
            actions.move_to_element(unity_canvas) \
                .move_by_offset(safe_offset_x - canvas_size['width'] / 2,
                                safe_offset_y - canvas_size['height'] / 2) \
                .click() \
                .perform()
            print(f"第 {i} 次点击成功，坐标: ({safe_offset_x}, {safe_offset_y})")
            time.sleep(1)
        except Exception as e:
            print(f"第 {i} 次点击失败: {str(e)}")
            # 发生错误后重置 action chains
            actions = ActionChains(driver)
            time.sleep(1)
#处理宠物喂养
def feed_pets(driver):
    # 查找grains并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/grains.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到grains")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            time.sleep(3)
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/close2.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找berries并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/berries.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到berries")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/close2.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找mushrooms并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/mushrooms.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到mushrooms")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/close2.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找granola并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/granola.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到granola")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = "imgs/close2.bmp"
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找bowl并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/bowl.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到bowl")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/close2.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找medley并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/medley.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到medley")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/give.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/close2.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/close2.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    time.sleep(3)
def setup_pet(driver):
    #先查找是否有新的蛋，有就激活，
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
    template_paths = ["imgs/newegg.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到新龙蛋，激活")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = ["imgs/hatch.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"新宠物激活成功")
    #查找是否有新的宠物，有就释放，窝里面有宠物和没宠物是不一样的，这里只要判断没有宠物的状态就可以了
    time.sleep(5)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
    template_paths = ["imgs/empty.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"没有宠物，退出进行下一个任务")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
        template_paths = ["imgs/close2.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        return
    else:
        print(f"有宠物，开始释放宠物,需要遍历所有的页面是否有空位置，没有的话就跳出，总计最多有三个宠物位")
        for i in range(1, 7):
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
            template_paths = ["imgs/next.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"进到下一页，开始找空位")
                time.sleep(5)
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                template_paths = ["imgs/vacant.bmp"]
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"找到空位置，开始释放宠物")
                    time.sleep(5)
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                    template_paths = ["imgs/nursery.bmp"]
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                    if found:
                        time.sleep(5)
                        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                        template_paths = ["imgs/adopt.bmp"]
                        found = find_and_click_eggs(driver, unity_canvas, template_paths)
                        if found:
                            print(f"找到目标，成功释放宠物,直接10次play任务和5次喂养任务")
                            for i in range(1, 10):
                                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 直接play6次
                                template_paths = ["imgs/play.bmp"]
                                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                                if found:
                                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                                    template_paths = "imgs/full.bmp"
                                    found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths,
                                                                              threshold=0.8)
                                    if found:
                                        break
                                time.sleep(10)
                            for i in range(1, 3):
                                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                                template_paths = ["imgs/feed.bmp"]
                                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                                if found:
                                    print(f"成功点击目标:feed.bmp，开始喂食")
                                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                                    template_paths = "imgs/full2.bmp"
                                    found, coordinates = capture_and_find_egg(driver, unity_canvas, template_paths,
                                                                              threshold=0.8)
                                    if found:
                                        break
                                    feed_pets(driver)
                                    break   # 跳出循环，因为任务已经做完了
                else:
                    print(f"没有找到空位置")


def grab_shop(driver):
    # 默认第一个是egg界面
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/free.bmp","imgs/free2.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到egg，已经领取egg")
        time.sleep(6)
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = ["imgs/ok.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功点击ok按钮")
    #查找decorations界面
    time.sleep(3)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/decorations.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到decorations")
        time.sleep(3)
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找领取免费物品按钮
        template_paths = ["imgs/free.bmp","imgs/free2.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取decorations")
            time.sleep(6)
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = ["imgs/ok.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找habitat界面
    time.sleep(3)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
    template_paths = ["imgs/habitat.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到habitat")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = ["imgs/free.bmp","imgs/free2.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取habitat")
            time.sleep(6)
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = ["imgs/ok.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找food界面
    time.sleep(3)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/food.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到food界面")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/free.bmp","imgs/free2.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取food")
            time.sleep(6)
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/ok.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找currency
    time.sleep(3)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/currency.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到currency")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = ["imgs/free.bmp","imgs/free2.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取currency")
            time.sleep(6)
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = ["imgs/ok.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = ["imgs/close.bmp"]
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到close,关闭商店界面")


#所有宠物设置休眠
def rest_all_pets(driver):
    for i in range(0, 5):
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = ["imgs/next.bmp"]
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = ["imgs/rest.bmp"]
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"成功设置第{i}只宠物休眠")

def import_wallet(driver, wallet_address):
    # 遍历每个窗口句柄
    window_handles = driver.window_handles
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
    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div[3]/div/div[2]/button/span").click()  # click the import button
    time.sleep(2)

    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div[3]/div/div[1]/div[2]/div").click()  # click the creat button
    time.sleep(2)  #
    driver.find_element("xpath",
                        "//*[@id='app']/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]").click()  # click the privte key button
    time.sleep(2)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[2]/div/textarea").send_keys(
        {wallet_address})
    time.sleep(6)
    time.sleep(2)
    driver.find_element("xpath", "//*[@id='app']/div/div[2]/div/button").click()  # click the confirm button
    time.sleep(3)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/button/span").click()  # click the confirm button again
    time.sleep(3)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div[2]/div[3]/div[2]/div/div[1]").click()  # select password
    time.sleep(6)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div[2]/div[5]/div/button").click()  # click notrecommend button
    time.sleep(6)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input").send_keys(
        'Aa2006123!!')
    time.sleep(6)
    driver.find_element("xpath",
                        "//*[@id='app']/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input").send_keys(
        'Aa2006123!!')
    time.sleep(10)
    driver.find_element("xpath", "//*[@id='app']/div/div[2]/div/button").click()  # click confirm button
    time.sleep(25)
    # driver.find_element("xpath", "//*[@id='app']/div/div/div/div[4]/div/button").click()#click start button
    driver.close()
    time.sleep(3)
    driver.switch_to.window(window_handles[0])  # 切换到第1个标签页
    # the next step is game automatic,i will test if it work without image recognition.just click
    time.sleep(3)
    driver.refresh()
    time.sleep(10)
    driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/button/span").click()  # click the play button
    time.sleep(3)
    driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
    time.sleep(5)
    # here is the problem, i can't click the okx wallet button, so i use the action chain to click the okx wallet button
    actions = ActionChains(driver)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the okx wallet button')
    actions.move_by_offset(606, 411).click().perform()  # click the okx wallet button
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'switch to the wallet window')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)
    # print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'refresh the wallet window')
    # driver.refresh()
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'now to click the connect button')
    driver.find_element("xpath",
                        "//*[@id='app']/div/div/div/div/div[5]/div[2]/button[2]/span/div").click()  # click the connect button
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'switch to the first window')
    driver.switch_to.window(window_handles[0])
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the arbitrum one button')
    actions.move_by_offset(606, 187).click().perform()  # click the okx wallet button
    time.sleep(6)
    driver.find_element("xpath", "//*[@id='link-wallet-tooltip']/span").click()
    time.sleep(6)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the confirm button')
    driver.find_element("xpath", "//*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span").click()
    time.sleep(6)  # //*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span
    driver.switch_to.window(window_handles[0])
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the close button')
    driver.find_element("xpath", "/html/body/div[5]/div/div/div/div[1]/button").click()  # click the close button
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the first input box')
    driver.find_element("xpath",
                        "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/input").click()  # click the input box
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'click the second input box')
    driver.find_element("xpath",
                        "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/input").click()  # click the input box
    time.sleep(10)
    driver.find_element("xpath", "/html/body/div[4]/div/div/div/div[3]/button/span").click()  # click the accept button
    time.sleep(10)  # /html/body/div[4]/div/div/div/div[3]/button/span
    driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/input").send_keys('61eth')
    time.sleep(2)
    driver.find_element("xpath", "/html/body/div[7]/div/div/div/div[2]/div/div/button").click()
    time.sleep(6)
    # 定位目标元素
    driver.find_element("xpath", "//*[@id='root']/div[1]/div[2]/div/div[2]/button").click()

def get_element_center_coordinates(driver, element):
    """获取元素的中心坐标"""
    size = element.size
    location = element.location
    center_x = location['x'] + (size['width'] / 2)
    center_y = location['y'] + (size['height'] / 2)
    return center_x, center_y


from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def safe_click(driver, xpath, description=""):
    """
    安全点击元素，如果找不到元素则跳过
    :param driver: WebDriver 实例
    :param xpath: 元素的 XPath
    :param description: 操作描述（用于日志）
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        print(f"{description} 点击成功")
    except Exception as e:
        print(f"{description} 未找到元素，跳过点击操作")

def import_wallet_2(driver, wallet_address):
    # 遍历每个窗口句柄
    window_handles = driver.window_handles
    for handle in window_handles:
        driver.switch_to.window(handle)
        title = driver.title
        print(f"Window Handle: {handle}, Title: {title}")

        # 如果标题是 "OKX Wallet"，则在该窗口中打开指定页面
        if title == "OKX Wallet":
            print("Found OKX Wallet window. Opening the extension page...")
            #driver.get("chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize")
            break  # 退出循环

    # 如果没有找到标题为 "OKX Wallet" 的窗口
    else:
        print("No window with title 'OKX Wallet' found.")

    time.sleep(3)
    safe_click(driver, "//*[@id='app']/div/div/div/div[3]/div/div[2]/button/span", "导入按钮")
    time.sleep(2)

    safe_click(driver, "//*[@id='app']/div/div/div/div[3]/div/div[1]/div[2]/div", "创建按钮")
    time.sleep(2)

    safe_click(driver, "//*[@id='app']/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]", "私钥按钮")
    time.sleep(2)

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[2]/div/textarea").send_keys(wallet_address)
        print("钱包地址输入成功")
    except Exception as e:
        print("钱包地址输入失败，跳过")

    time.sleep(6)
    safe_click(driver, "//*[@id='app']/div/div[2]/div/button", "确认按钮")
    time.sleep(3)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/button/span", "再次确认按钮")
    time.sleep(3)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div[3]/div[2]/div/div[1]", "选择密码")
    time.sleep(6)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div[5]/div/button", "不推荐按钮")
    time.sleep(6)

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
        print("密码输入成功")
    except Exception as e:
        print("密码输入失败，跳过")

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
        print("确认密码输入成功")
    except Exception as e:
        print("确认密码输入失败，跳过")

    time.sleep(10)
    safe_click(driver, "//*[@id='app']/div/div[2]/div/button", "最终确认按钮")
    time.sleep(25)

    driver.close()
    time.sleep(3)
    driver.switch_to.window(window_handles[0])  # 切换到第1个标签页

    time.sleep(3)
    driver.refresh()
    time.sleep(10)
    safe_click(driver, "//*[@id='root']/div[1]/div[2]/div/button/span", "播放按钮")
    time.sleep(3)

    safe_click(driver, "//*[@id='link-wallet-tooltip']/span", "链接钱包按钮")
    time.sleep(5)

    actions = ActionChains(driver)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击 OKX 钱包按钮')
    actions.move_by_offset(606, 411).click().perform()  # 点击 OKX 钱包按钮
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '切换到钱包窗口')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击连接按钮')
    safe_click(driver, "//*[@id='app']/div/div/div/div/div[5]/div[2]/button[2]/span/div", "连接按钮")
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '切换到第一个窗口')
    driver.switch_to.window(window_handles[0])
    time.sleep(3)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击 Arbitrum One 按钮')
    actions.move_by_offset(606, 187).click().perform()  # 点击 Arbitrum One 按钮
    #iframe = driver.find_element(By.ID, "w3m-iframe")
    #driver.switch_to.frame(iframe)
    #driver.switch_to.frame("w3m-iframe")  # id: w3m-iframe    name: w3m-secure-iframe
    #time.sleep(3)
    #safe_click(driver, "//wui-image[@name='Arbitrum One']", "选择网络按钮")
    time.sleep(6)
    #driver.switch_to.default_content()
    safe_click(driver, "//*[@id='link-wallet-tooltip']/span", "链接钱包按钮")
    time.sleep(6)

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击确认按钮')
    safe_click(driver, "//*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span", "确认按钮")
    time.sleep(6)

    driver.switch_to.window(window_handles[0])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击关闭按钮')
    safe_click(driver, "/html/body/div[5]/div/div/div/div[1]/button", "关闭按钮")
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击第一个输入框')
    safe_click(driver, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/input", "第一个输入框")
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击第二个输入框')
    safe_click(driver, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/input", "第二个输入框")
    time.sleep(10)

    safe_click(driver, "/html/body/div[4]/div/div/div/div[3]/button/span", "接受按钮")
    time.sleep(10)

    try:
        driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div/div[2]/div/div/input").send_keys('61eth')
        print("输入 61eth 成功")
    except Exception as e:
        print("输入 61eth 失败，跳过")

    safe_click(driver, "/html/body/div[7]/div/div/div/div[2]/div/div/button", "确认按钮")
    time.sleep(6)

    safe_click(driver, "//*[@id='root']/div[1]/div[2]/div/div[2]/button", "目标元素")


def import_wallet_3(driver, wallet_address):
    # 遍历每个窗口句柄
    window_handles = driver.window_handles
    for handle in window_handles:
        driver.switch_to.window(handle)
        title = driver.title
        print(f"Window Handle: {handle}, Title: {title}")

        # 如果标题是 "OKX Wallet"，则在该窗口中打开指定页面
        if title == "OKX Wallet":
            print("Found OKX Wallet window. Opening the extension page...")
            #driver.get("chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize")
            break  # 退出循环

    # 如果没有找到标题为 "OKX Wallet" 的窗口
    else:
        print("No window with title 'OKX Wallet' found.")

    time.sleep(3)
    safe_click(driver, "//*[@id='app']/div/div/div/div[3]/div/div[2]/button/span", "导入按钮")
    time.sleep(1)

    safe_click(driver, "//*[@id='app']/div/div/div/div[3]/div/div[1]/div[2]/div", "创建按钮")
    time.sleep(1)

    safe_click(driver, "//*[@id='app']/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]", "私钥按钮")
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[2]/div/textarea").send_keys(wallet_address)
        print("钱包地址输入成功")
    except Exception as e:
        print("钱包地址输入失败，跳过")

    time.sleep(6)
    safe_click(driver, "//*[@id='app']/div/div[2]/div/button", "确认按钮")
    time.sleep(1)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/button/span", "再次确认按钮")
    time.sleep(1)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div[3]/div[2]/div/div[1]", "选择密码")
    time.sleep(2)

    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div[5]/div/button", "不推荐按钮")
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
        print("密码输入成功")
    except Exception as e:
        print("密码输入失败，跳过")

    try:
        driver.find_element(By.XPATH, "//*[@id='app']/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input").send_keys('Aa2006123!!')
        print("确认密码输入成功")
    except Exception as e:
        print("确认密码输入失败，跳过")

    time.sleep(5)
    safe_click(driver, "//*[@id='app']/div/div[2]/div/button", "最终确认按钮")
    time.sleep(5)

    driver.close()
    time.sleep(3)
    driver.switch_to.window(window_handles[0])  # 切换到第1个标签页

    time.sleep(3)
    driver.refresh()
    time.sleep(10)
    safe_click(driver, "//*[@id='root']/div[1]/div[2]/div/button/span", "播放按钮")
    time.sleep(3)

    safe_click(driver, "//*[@id='link-wallet-tooltip']/span", "链接钱包按钮")
    time.sleep(5)

    actions = ActionChains(driver)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击 OKX 钱包按钮')
    actions.move_by_offset(606, 411).click().perform()  # 点击 OKX 钱包按钮
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '切换到钱包窗口')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击连接按钮')
    safe_click(driver, "//*[@id='app']/div/div/div/div/div[5]/div[2]/button[2]/span/div", "连接按钮")
    time.sleep(2)
    driver.switch_to.window(window_handles[1])
    time.sleep(1)
    #这里需要打开插件，重新选择arb网络
    driver.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html#/connect-site")
    time.sleep(3)
    safe_click(driver, "//*[@id='app']/div/div/div/div[2]/div[3]/div[2]/div[1]", "点击以太坊主网按钮")
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, "//*[@id='scroll-box']/div/div/div[2]/div/input[2]").send_keys('arb')
        print("输入 arb 成功")
    except Exception as e:
        print("输入 arb 失败，跳过")
    safe_click(driver, "//*[@id='scroll-box']/div/div/div[3]/div[2]/div/div", "选中arb网络")
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '切换到第一个窗口')
    driver.switch_to.window(window_handles[0])
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
    safe_click(driver, "//*[@id='root']/div[1]/div[2]/div/button/span", "点击play now")
    time.sleep(3)
    safe_click(driver, "//*[@id='link-wallet-tooltip']/span", "链接钱包按钮")
    time.sleep(6)

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击确认按钮')
    safe_click(driver, "//*[@id='app']/div/div/div/div/div/div[4]/div/button[2]/span", "确认按钮")
    time.sleep(6)

    driver.switch_to.window(window_handles[0])
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击关闭按钮')
    safe_click(driver, "/html/body/div[5]/div/div/div/div[1]/button", "关闭按钮")
    time.sleep(3)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击第一个输入框')
    safe_click(driver, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/input", "第一个输入框")
    time.sleep(1)

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), '点击第二个输入框')
    safe_click(driver, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/input", "第二个输入框")
    time.sleep(1)

    safe_click(driver, "/html/body/div[4]/div/div/div/div[3]/button/span", "接受按钮")
    time.sleep(10)

    try:
        driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div/div[2]/div/div/input").send_keys('61eth')
        print("输入 61eth 成功")
    except Exception as e:
        print("输入 61eth 失败，跳过")

    safe_click(driver, "/html/body/div[7]/div/div/div/div[2]/div/div/button", "确认按钮")
    time.sleep(6)

    safe_click(driver, "//*[@id='root']/div[1]/div[2]/div/div[2]/button", "目标元素")


