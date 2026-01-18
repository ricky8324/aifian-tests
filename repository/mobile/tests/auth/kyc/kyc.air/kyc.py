__author__ = "chris"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.report.report import simple_report
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
auto_setup(__file__)

# CASE1：帳號為己驗證
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

# 帳號登入
poco("android.widget.EditText").set_text("900752434")
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

poco("android.widget.EditText").set_text("Bella005")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)

poco(text="帳號").click()

try:
    assert_equal(poco(text="已驗證").exists(), True, "確認身分驗證狀態為已驗證")
except Exception as e:
    log(e, snapshot=True)

# CASE2：帳號為尚未完成驗証
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

# 帳號登入
poco("android.widget.EditText").set_text("912137356")
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

poco("android.widget.EditText").set_text("Bella088$")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)

poco(text="帳號").click()

try:
    assert_equal(poco(text="尚未完成").exists(), True, "確認身分驗證狀態為尚未完成")
except Exception as e:
    log(e, snapshot=True)

poco(text="尚未完成").click()
sleep(3)

try:
    assert_equal(poco(text="開始使用").exists(), True, "點擊尚未完成導到 Persona 身分驗證流程")
except Exception as e:
    log(e, snapshot=True)

poco("com.adenovo.aifianstg:id/nav_bar_cancel_button").click()
poco("com.adenovo.aifianstg:id/close_button").click()
poco(text="收藏").click()
poco(text="智能選品").click()
touch(Template(r"tpl1764647072781.png", record_pos=(0.274, 0.923), resolution=(1080, 2424)))

try:
    assert_equal(poco(text="完成安全驗證，開啟交易功能").exists(), True, "購買智能選品，\"完成安全驗證\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1756279164790.png", record_pos=(0.235, 0.861), resolution=(1080, 2400)))
sleep(5)

try:
    assert_equal(poco(text="開始使用").exists(), True, "點擊 Bottom Sheet 的身分驗證會導到 Persona 身分驗證流程")
except Exception as e:
    log(e, snapshot=True)

poco("com.adenovo.aifianstg:id/nav_bar_cancel_button").click()
poco("com.adenovo.aifianstg:id/close_button").click()
touch(Template(r"tpl1756278807731.png", record_pos=(-0.41, -0.959), resolution=(1080, 2400)))
sleep(3)
poco(text="全部").swipe([0, -4.0])
sleep(3)
poco(text="測試威士忌").click()
touch(Template(r"tpl1764647072781.png", record_pos=(0.274, 0.923), resolution=(1080, 2424)))

try:
    assert_equal(poco(text="完成安全驗證，開啟交易功能").exists(), True, "購買單品酒品，\"完成安全驗證\"的 Bottom Sheet 會彈出")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1756279164790.png", record_pos=(0.235, 0.861), resolution=(1080, 2400)))
sleep(5)

try:
    assert_equal(poco(text="開始使用").exists(), True, "點擊 Bottom Sheet 的身分驗證會導到 Persona 身分驗證流程")
except Exception as e:
    log(e, snapshot=True)

# CASE3：帳號未通過驗証
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

# 帳號登入
poco("android.widget.EditText").set_text("900010127")
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

poco("android.widget.EditText").set_text("Bella127")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)

poco(text="帳號").click()

try:
    assert_equal(poco(text="未通過").exists(), True, "確認身分驗證狀態為未通過")
except Exception as e:
    log(e, snapshot=True)
    
poco(text="未通過").click()

try:
    assert_equal(poco(text="身分安全驗證尚未通過").exists(), True, "確確認\"身分安全驗證尚未通過\" Bottom Sheet 有彈出")
except Exception as e:
    log(e, snapshot=True)
