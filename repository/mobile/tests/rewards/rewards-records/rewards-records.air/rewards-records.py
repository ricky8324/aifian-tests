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

# CASE1: 有今日回饋且總累積回饋跟回饋數字不一樣
touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
sleep(3)
try:
    assert_equal(poco(text="今日回饋率").exists(), True, "有今日回饋且總累積回饋跟回饋數字不一樣，今日回饋率有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="總累積回饋").exists(), True, "有今日回饋且總累積回饋跟回饋數字不一樣，總累積回饋有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1765174677964.png", record_pos=(-0.001, -0.886), resolution=(1080, 2424)), "有今日回饋且總累積回饋跟回饋數字不一樣，回饋有顯示")
except Exception as e:
    log(e, snapshot=True)

# CASE2: 有今日回饋且總累積回饋跟回饋數字一樣
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

poco("android.widget.EditText").set_text("907070707")
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

touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
sleep(3)
try:
    assert_equal(poco(text="今日回饋率").exists(), True, "有今日回饋且總累積回饋跟回饋數字一樣，今日回饋率有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="總累積回饋").exists(), True, "有今日回饋且總累積回饋跟回饋數字一樣，總累積回饋有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1765174677964.png", record_pos=(-0.001, -0.886), resolution=(1080, 2424)), "有今日回饋且總累積回饋跟回饋數字一樣，回饋有顯示")
except Exception as e:
    log(e, snapshot=True)
    
# CASE3: 沒有今日回饋且總累積回饋跟回饋數字不一樣
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)

poco("android.widget.EditText").set_text("908080808")
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

touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
sleep(3)
try:
    assert_equal(poco(text="今日回饋率").exists(), True, "沒有今日回饋且總累積回饋跟回饋數字不一樣，今日回饋率有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="-").exists(), True, "沒有今日回饋，今日回饋率有顯示\"-\"")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="總累積回饋").exists(), True, "沒有今日回饋且總累積回饋跟回饋數字不一樣，總累積回饋有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1765174677964.png", record_pos=(-0.001, -0.886), resolution=(1080, 2424)), "沒有今日回饋且總累積回饋跟回饋數字不一樣，回饋有顯示")
except Exception as e:
    log(e, snapshot=True)
