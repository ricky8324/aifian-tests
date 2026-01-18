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
poco("android.widget.EditText").set_text("900753874")
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

poco("android.widget.EditText").set_text("Bella047")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)

touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
touch(Template(r"tpl1764646328516.png", record_pos=(0.432, -0.887), resolution=(1080, 2424)))
sleep(3)
poco(text="轉出回饋").click()

try:
    assert_equal(poco(text="尚未綁定銀行帳號").exists(), True, "確認\"尚未綁定銀行帳號\" Bottom Sheet 有彈出")
except Exception as e:
    log(e, snapshot=True)

poco(text="下次再說").click()

try:
    assert_equal(poco(text="回饋").exists(), True, "點擊\"下次再說\"停留在回饋頁面")
except Exception as e:
    log(e, snapshot=True)

sleep(3)
touch(Template(r"tpl1764646328516.png", record_pos=(0.432, -0.887), resolution=(1080, 2424)))
sleep(3)
poco(text="轉出回饋").click()

poco(text="綁定銀行帳號").click()
sleep(3)

try:
    assert_equal(poco(text="選擇銀行").exists(), True, "點擊\"綁定銀行帳號\"導到綁定銀行頁面")
except Exception as e:
    log(e, snapshot=True)
