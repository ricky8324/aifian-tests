# -*- encoding=utf8 -*-
__author__ = "bella"

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

# 1. 在 [註冊登入畫面] 可以更新國碼欄位

poco(text="+886").click()
poco(text="United States").click()
try:
    assert_equal(poco(text="+1").exists(), True, "在註冊登入頁面，可以正常更新國碼欄位")
except Exception as e:
    log(e, snapshot=True)
poco(text="+1").click()
poco(text="Taiwan").click()
poco("android.widget.EditText").set_text("0961000001")
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
poco("android.widget.EditText").set_text("Bella001$")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1761030815566.png", record_pos=(0.384, -0.518), resolution=(1080, 2400))):
    touch(Template(r"tpl1761030815566.png", record_pos=(0.384, -0.518), resolution=(1080, 2400)))
sleep(3)

poco(text="帳號").click()

# 2. 在 [修改手機畫面] 可以更新國碼欄位

poco(text="帳號與安全性").click()
sleep(3)
poco(text="+886961000001").click()
sleep(3)
poco(text="+886").click()
poco(text="United States").click()
try:
    assert_equal(poco(text="+1").exists(), True, "在修改手機頁面，可以正常更新國碼欄位")
except Exception as e:
    log(e, snapshot=True)
poco(text="+1").click()
poco(text="Taiwan").click()
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))

# 3. 在 [忘記密碼流程] 可以更新國碼欄位

poco(text="登入密碼").click()
sleep(3)
poco(text="忘記密碼").click()
sleep(3)
poco(text="+886").click()
poco(text="United States").click()
try:
    assert_equal(poco(text="+1").exists(), True, "在忘記密碼流程中，可以正常更新國碼欄位")
except Exception as e:
    log(e, snapshot=True)
poco(text="+1").click()
poco(text="Taiwan").click()
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))
sleep(1)

touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))

# 4. 在 [刪除帳號流程] 可以更新國碼欄位

poco(text="刪除帳號").click()
sleep(3)
poco(text="仍要刪除帳號").click()
sleep(3)
poco(text="+886").click()
poco(text="United States").click()
try:
    assert_equal(poco(text="+1").exists(), True, "在刪除帳號流程中，可以正常更新國碼欄位")
except Exception as e:
    log(e, snapshot=True)
poco(text="+1").click()
poco(text="Taiwan").click()
touch(Template(r"tpl1764649725774.png", record_pos=(-0.001, -0.885), resolution=(1080, 2424)))
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))

# 5. 登出帳號
poco(text="登出").click()