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
window_handles = driver.window_handles    #获取所有窗口的句柄
driver.switch_to.window(window_handles[-1])  #切换到最后一个打开的窗口
driver.close()    #关闭当前窗口
同时要操作OKX插件可以在新的标签页里面加载插件的初始化界面：chrome-extension://gniabnkpabeeokgnkcfnlbgdnngddeeb/notification.html#/initialize
这个界面的地址可以在弹窗上面获得，但是要注意每一次调用插件的时候都需要切换到插件所在的标签页刷新页面重新加载才可以‘’

Note: 20250122
插件的欢迎页面和弹窗打开的顺序并不是固定的，所以有时候会把欢迎页面关闭掉，所以这个时候需要在遍历所有的窗口句柄以后跟根据窗口的标题来关闭对应的窗口
这样就能精确的定位到要关闭或者操作的任何一个窗口
selenium的坐标计算是相对坐标，这个需要根据窗口的尺寸来计算，这个需要自己计算，参考：https://www.cnblogs.com/zhangxiaoyang/p/11479601.html
预计明天能完成整个脚本

Note: 20250123
今天完成了识图部分的操作，任务流程还需要优化，现在费时间比较久，效率很低。需要测试多线程模式下的工作稳定性，接下来要做的工作
1，排查bug
2,改成多线程运行
迭代了一个新版本
优化了任务流程，时间更短了，但是在考虑要不要把宠物玩具的放置任务也做了，防止项目方后面要求habitat points的点数。
多线程部分不用代码硬改，直接把现有的文件复制成5份然后命名 同时引入不同的钱包文件应该就可以跑起来，目前待测试，
导入钱包之前的任务流程需要优化，出错中断的任务需要记录，嗯，目前就这些
先出去吃饭，下午去博物馆给你拍照，(:




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

