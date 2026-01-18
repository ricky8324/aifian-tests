# -*- encoding=utf8 -*-
__author__ = "chris"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.report.report import simple_report
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
auto_setup(__file__)

adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

# 帳號登入
poco("android.widget.EditText").set_text("911111111")
poco(text="使用手機繼續").click()
sleep(3)
# 輸入驗証碼，為了相容 RN 跟 AN 的自動化
text("1")
text("2")
text("3")
text("4")
text("5")
text("6")
sleep(3)

poco("android.widget.EditText").set_text("@Ss8654092")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)

# CASE1：首頁跳出 Alert
try:
    assert_equal(poco(text="身分審核中").exists(), True, "確認首頁有跳出身分審核中的 Alert")
except Exception as e:
    log(e, snapshot=True)

# CASE2：帳號為驗證中
poco(text="帳號").click()

try:
    assert_equal(poco(text="驗證中").exists(), True, "確認身分驗證狀態為驗證中")
except Exception as e:
    log(e, snapshot=True)

poco(text="驗證中").click()
sleep(3)

try:
    assert_equal(poco(text="你的身分正在驗證中").exists(), True, "點擊驗證中，\"你的身分正在驗證中\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

poco(text="知道了").click()
sleep(3)

# CASE3：點擊我的禮物
poco(text="我的禮物").click()

try:
    assert_equal(poco(text="你的身分正在驗證中").exists(), True, "點擊我的禮物，\"你的身分正在驗證中\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

poco(text="知道了").click()
poco(text="收藏").click()
sleep(3)

# CASE4：點擊轉出回饋
touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
touch(Template(r"tpl1764646328516.png", record_pos=(0.432, -0.887), resolution=(1080, 2424)))
sleep(3)
poco(text="轉出回饋").click()

try:
    assert_equal(poco(text="你的身分正在驗證中").exists(), True, "點擊轉出回饋，\"你的身分正在驗證中\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

poco(text="知道了").click()
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))

# CASE5：購買智能選品
poco(text="智能選品").click()
sleep(3)
touch(Template(r"tpl1764647072781.png", record_pos=(0.274, 0.923), resolution=(1080, 2424)))

try:
    assert_equal(poco(text="你的身分正在驗證中").exists(), True, "購買智能選品，\"你的身分正在驗證中\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

poco(text="知道了").click()
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))
sleep(3)
poco(text="全部").swipe([0, -4.0])
sleep(3)

# CASE6：購買單品酒品
poco(text="測試威士忌").click()
touch(Template(r"tpl1764647072781.png", record_pos=(0.274, 0.923), resolution=(1080, 2424)))

try:
    assert_equal(poco(text="你的身分正在驗證中").exists(), True, "購買單品酒品，\"你的身分正在驗證中\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)
