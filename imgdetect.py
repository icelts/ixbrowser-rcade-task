import cv2
import numpy as np
from PIL import Image
import io
import time
from selenium.webdriver.common.action_chains import ActionChains


def capture_and_find_egg(driver, unity_canvas, template_path, threshold=0.8):
    """
    截取画布并查找目标蛋的位置
    """
    try:
        # 获取画布截图
        screenshot = unity_canvas.screenshot_as_png
        screenshot = Image.open(io.BytesIO(screenshot))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 读取模板图片（目标蛋的图片）
        template = cv2.imread(template_path)

        # 进行模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # 获取模板图片的尺寸
            h, w = template.shape[:2]

            # 计算中心点位置
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            # 保存调试图片（可选）
            debug_img = screenshot.copy()
            cv2.rectangle(debug_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.circle(debug_img, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.imwrite('debug_find_egg.png', debug_img)

            return True, (center_x, center_y)
        else:
            return False, None

    except Exception as e:
        print(f"图像处理过程出错: {str(e)}")
        return False, None


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
def find_and_click_eggs(driver, unity_canvas, template_paths, max_attempts=3):
    """
    查找并点击所有目标蛋
    """
    for template_path in template_paths:
        attempts = 0
        while attempts < max_attempts:
            # 等待页面稳定
            time.sleep(2)

            # 查找目标
            found, coordinates = capture_and_find_egg(driver, unity_canvas, template_path)

            if found:
                print(f"找到目标，坐标: {template_path}")
                if click_egg(driver, unity_canvas, coordinates):
                    print("点击成功")
                    return True

            attempts += 1
            if attempts == max_attempts:
                print(f"未能成功点击目标: {template_path}")
            time.sleep(1)
    return False
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
            time.sleep(3)
        except Exception as e:
            print(f"第 {i} 次点击失败: {str(e)}")
            # 发生错误后重置 action chains
            actions = ActionChains(driver)
            time.sleep(1)
#处理宠物喂养
def feed_pets(driver):
    # 查找grains并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\grains.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到grains")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找berries并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\berries.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到berries")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找mushrooms并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\mushrooms.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到mushrooms")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找granola并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\granola.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到granola")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找bowl并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\bowl.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到bowl")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    #查找medley并喂食
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\medley.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到medley")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\give.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功喂食，下一步关闭界面")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            return
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close2.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)



def setup_pet(driver):
    #先查找是否有新的蛋，有就激活，
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\newegg.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到新龙蛋，激活")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\hatch.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"新宠物激活成功")
    #查找是否有新的宠物，有就释放，窝里面有宠物和没宠物是不一样的，这里只要判断没有宠物的状态就可以了
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\empty.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"没有宠物，退出进行下一个任务")
        return
    else:
        print(f"有宠物，开始释放宠物,需要遍历所有的页面是否有空位置，没有的话就跳出，总计最多有三个宠物位")
        for i in range(1, 7):
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\next.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"进到下一页，开始找空位")
                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\vacant.bmp"}
                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                if found:
                    print(f"找到空位置，开始释放宠物")
                    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\nursery.bmp"}
                    found = find_and_click_eggs(driver, unity_canvas, template_paths)
                    if found:
                        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 如果商店
                        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\adopt.bmp"}
                        found = find_and_click_eggs(driver, unity_canvas, template_paths)
                        if found:
                            print(f"找到目标，成功释放宠物,直接10次play任务和5次喂养任务")
                            for i in range(1, 10):
                                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 直接play6次
                                template_paths = {
                                    r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\play.bmp"}
                                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                                time.sleep(10)
                            for i in range(1, 3):
                                unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
                                template_paths = {
                                    r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\feed.bmp"}
                                found = find_and_click_eggs(driver, unity_canvas, template_paths)
                                if found:
                                    print(f"成功点击目标:feed.bmp，开始喂食")
                                    feed_pets(driver)
                else:
                    print(f"没有找到空位置")







def grab_shop(driver):
    # 默认第一个是egg界面
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\free.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到egg，已经领取egg")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\ok.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功点击ok按钮")
    #查找decorations界面
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\decorations.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到decorations")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找领取免费物品按钮
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\free.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取decorations")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\ok.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找habitat界面
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\habitat.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到habitat")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\free.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取habitat")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\ok.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找food界面
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\food.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到food界面")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\free.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取food")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\ok.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    #查找currency
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\currency.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到currency")
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\free.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            print(f"成功领取currency")
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\ok.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
    unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 寻找食物，开始喂食
    template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\close.bmp"}
    found = find_and_click_eggs(driver, unity_canvas, template_paths)
    if found:
        print(f"找到close,关闭商店界面")


#所有宠物设置休眠
def rest_all_pets(driver):
    for i in range(0, 5):
        unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
        template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\next.bmp"}
        found = find_and_click_eggs(driver, unity_canvas, template_paths)
        if found:
            unity_canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")
            template_paths = {r"C:\Users\a2720\PycharmProjects\ixbrowser-local-api-python\imgs\rest.bmp"}
            found = find_and_click_eggs(driver, unity_canvas, template_paths)
            if found:
                print(f"成功设置第{i}只宠物休眠")
