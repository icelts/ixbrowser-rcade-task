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
            time.sleep(3)

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
    safe_offset_x = min(400, canvas_size['width'] - 50)  # 距离边缘保持50px
    safe_offset_y = min(400, canvas_size['height'] - 50)  # 距离边缘保持50px

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
def feed_pets(driver, unity_canvas, template_paths, max_attempts=3):
    for template_path in template_paths:
        attempts = 0
        while attempts < max_attempts:
            # 等待页面稳定
            time.sleep(2)
            found, coordinates = capture_and_find_egg(driver, unity_canvas, template_path)
            if found:
                print(f"找到目标，坐标: {coordinates}")
                if click_egg(driver, unity_canvas, coordinates):
                    print("点击成功")
                    break

            attempts += 1