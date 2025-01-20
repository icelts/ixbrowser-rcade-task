# ixBrowser Local API

ixBrowser本地API V2.0 Python版本

## README.md
rcade要求参与空投的用户完成https://hatchlings.revolvinggames.com/?cache=false 的养殖任务可以才拿到空投
这个任务要求用户使用参与任务的钱包授权登录进去，然后拿到至少500点养殖点数，最后再在任务界面认证就可以了，这个任务我需要用
ix自动化来完成，全程靠坐标点击，不做图像识别

So im working on develop a ixBrowser automation for https://hatchlings.revolvinggames.com/?cache=false
the test file is run.py

Note: 20250121
测试了phantom和metamask以及okx三个钱包，基本上要做自动化的时候使用okx是最好的选择，步骤少，支持的网络比较多
浏览器打开的时候会插件会弹出窗口，这个可以通过设置chrome的参数来屏蔽(我没有测试)，
也可以通过代码来关闭：
window_handles = driver.window_handles
# 切换到新窗口
driver.switch_to.window(window_handles[-1])
# 关闭新窗口
driver.close()
同时要操作OKX插件可以在新的标签页里面加载插件的初始化界面：chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize
这个界面的地址可以在弹窗上面获得，但是要注意每一次调用插件的时候都需要切换到插件所在的标签页刷新页面重新加载才可以‘’


简单参考
```python
import random
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
data = c.get_profile_list()
if data is None:
    print('获取窗口列表错误:')
    print('错误代码=', c.code)
    print('错误描述=', c.message)
else:
	item = random.choice(data)

	profile_id = item['profile_id']
	print('随机打开窗口，窗口ID=', profile_id)

	open_result = c.open_profile(profile_id, cookies_backup=False, load_profile_info_page=False)
	if open_result is None:
		print('打开窗口错误:')
		print('错误代码=', c.code)
		print('错误描述=', c.message)
	else:
		print(open_result)
```

/examples 目录中有更多使用范例

