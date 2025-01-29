from selenium.webdriver.common.action_chains import ActionChains
import time


def click_position(driver, x, y, delay=1):
    """
    点击指定坐标
    :param driver: WebDriver实例
    :param x: x坐标
    :param y: y坐标
    :param delay: 点击前等待时间(秒)
    """
    try:
        time.sleep(delay)  # 等待指定时间
        canvas = driver.find_element("xpath", "//*[@id='unity-canvas']")  # 替换为实际的canvas元素ID
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(canvas, x, y)
        actions.click()
        actions.perform()
        return True
    except Exception as e:
        print(f"点击失败: {str(e)}")
        return False


def grab_shop(driver):
    # 定义各个按钮的坐标
    PLAY_BUTTON = (800, 600)  # 示例坐标，需要替换为实际坐标
    REST_BUTTON = (750, 600)
    FEED_BUTTON = (850, 600)

    while True:
        # 等待足够长的时间确保状态已更新
        time.sleep(5)

        # 按照游戏逻辑顺序点击
        click_position(driver, *PLAY_BUTTON, delay=2)
        time.sleep(30)  # 假设玩耍需要30秒

        click_position(driver, *REST_BUTTON, delay=2)
        time.sleep(60)  # 假设休息需要60秒

        click_position(driver, *FEED_BUTTON, delay=2)
        time.sleep(10)  # 等待喂食动画完成

def play_pet(driver):
    # 定义各个按钮的坐标
    PLAY_BUTTON = (986, 638)  # 示例坐标，需要替换为实际坐标
    for i in range(1, 11):
        click_position(driver, *PLAY_BUTTON, delay=2)
        time.sleep(12)  # 假设玩耍需要30秒

def feed_pets(driver):
    # 定义各个按钮的坐标
    FEED_BUTTON = (1207, 643)  # 示例坐标，需要替换为实际坐标
    GRAINS_BUTTON = (1207, 643)
    GIVE_BUTTON = (164, 435)
    CLOSE_BUTTON = (1227, 495)
    for i in range(1, 3):
        click_position(driver, *FEED_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *GRAINS_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *GIVE_BUTTON, delay=2)
        time.sleep(6)
        click_position(driver, *CLOSE_BUTTON, delay=2)
        time.sleep(3)

def grab_shop(driver):
    # 定义各个按钮的坐标
    SHOP_BUTTON = (1212, 130)  # 示例坐标，需要替换为实际坐标
    FREE1_BUTTON = (310, 374)
    OK_BUTTON = (644, 524)
    DECORATIONS_BUTTON = (460, 151)
    HABITAT_BUTTON = (460, 151)
    FOOD_BUTTON = (460, 151)
    CURRENCY_BUTTON = (971, 151)
    CLOSE_BUTTON = (1137, 122)
    click_position(driver, *SHOP_BUTTON, delay=2)
    time.sleep(3)
    click_position(driver, *FREE1_BUTTON, delay=2)
    time.sleep(5)
    click_position(driver, *OK_BUTTON, delay=2)
    time.sleep(1)
    click_position(driver, *DECORATIONS_BUTTON, delay=2)
    time.sleep(1)
    click_position(driver, *FREE1_BUTTON, delay=2)
    time.sleep(5)
    click_position(driver, *OK_BUTTON, delay=2)
    time.sleep(1)
    click_position(driver, *HABITAT_BUTTON, delay=2)
    time.sleep(3)
    click_position(driver, *FREE1_BUTTON, delay=2)
    time.sleep(5)
    click_position(driver, *OK_BUTTON, delay=2)
    time.sleep(1)
    click_position(driver, *FOOD_BUTTON, delay=2)
    time.sleep(3)
    click_position(driver, *FREE1_BUTTON, delay=2)
    time.sleep(5)
    click_position(driver, *OK_BUTTON, delay=2)
    time.sleep(1)
    click_position(driver, *CLOSE_BUTTON, delay=2)
    time.sleep(3)


def click_skip(driver):
    # 定义各个按钮的坐标
    FEED_BUTTON = (250, 250)  # 示例坐标，需要替换为实际坐标
    for i in range(1, 20):
        click_position(driver, *FEED_BUTTON, delay=2)
        time.sleep(1)


def setup_pet(driver):
    # 定义各个按钮的坐标
    EGGS_BUTTON = (213, 636)  # 示例坐标，需要替换为实际坐标
    EMBEREGG_BUTTON = (353, 590)
    HATCH_BUTTON = (351, 478)
    NEXT_BUTTON = (864, 35)
    NURSURY_BUTTON = (135, 596)
    HTCH_BUTTON = (212, 437)
    CLOSE_BUTTON = (212, 437)
    for i in range(1, 3):
        click_position(driver, *EGGS_BUTTON, delay=2)
        time.sleep(1)
        click_position(driver, *EMBEREGG_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *HATCH_BUTTON, delay=2)
        time.sleep(6)
        click_position(driver, *NEXT_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *NURSURY_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *HTCH_BUTTON, delay=2)
        time.sleep(3)
        click_position(driver, *CLOSE_BUTTON, delay=2)
        time.sleep(3)

def rest_all_pets(driver):
    # 定义各个按钮的坐标
    REST_BUTTON = (870,639)  # 示例坐标，需要替换为实际坐标
    NEXT_BUTTON = (864, 35)
    for i in range(1, 4):
        click_position(driver, *REST_BUTTON, delay=2)
        time.sleep(1)
        click_position(driver, *NEXT_BUTTON, delay=2)
        time.sleep(1)
