import threading
import comtypes.client
from selenium import webdriver
import time

# 大漠插件功能封装
class DmAutomation:
    def __init__(self):
        self.dm = comtypes.client.CreateObject('dm.dmsoft')
        print("大漠插件版本:", self.dm.Ver())

    def find_and_click(self, image_path):
        """查找图片并点击"""
        x, y = self.dm.FindPic(0, 0, 1920, 1080, image_path, "000000", 0.8, 0)
        if x >= 0 and y >= 0:
            print(f"找到图片，位置: ({x}, {y})")
            self.dm.MoveTo(x, y)
            self.dm.LeftClick()
        else:
            print("未找到图片")

# 线程任务函数
def task(thread_id, url, image_path):
    """每个线程的任务"""
    print(f"线程 {thread_id} 启动")

    # 启动 iXBrowser
    options = webdriver.ChromeOptions()
    options.debugger_address = f"127.0.0.1:{9222 + thread_id}"  # 每个线程使用不同的调试端口
    driver = webdriver.Chrome(options=options)

    # 打开目标网页
    driver.get(url)
    print(f"线程 {thread_id} 打开网页: {url}")

    # 初始化大漠插件
    dm_auto = DmAutomation()

    # 查找图片并点击
    time.sleep(5)  # 等待页面加载
    dm_auto.find_and_click(image_path)

    # 关闭浏览器
    time.sleep(2)
    driver.quit()
    print(f"线程 {thread_id} 完成")

# 主程序
if __name__ == "__main__":
    # 配置参数
    num_threads = 3  # 线程数量
    url = "https://www.example.com"  # 目标网页
    image_path = "target.bmp"  # 目标图片路径

    # 创建并启动线程
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=task, args=(i, url, image_path))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("所有任务完成！")