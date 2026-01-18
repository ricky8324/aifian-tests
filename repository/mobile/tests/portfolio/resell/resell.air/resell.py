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
poco("android.widget.EditText").set_text("912345612")
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

poco("android.widget.EditText").set_text("Bella5612$")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)    
    
swipe(Template(r"tpl1754548225271.png", record_pos=(-0.21, 0.429), resolution=(1080, 2400)), vector=[-0.1204, -0.5498])
sleep(3)

poco(text="測試威士忌").click()
sleep(3)
touch(Template(r"tpl1764665378047.png", record_pos=(-0.241, 0.929), resolution=(1080, 2424)))

sleep(5)

try:
    assert_equal(poco(text="$0").exists(), True, "確認預設轉售金額為0")
except Exception as e:
    log(e, snapshot=True)

if poco(text="手續費").exists():
    try:
        assert_exists(Template(r"tpl1765425932735.png", record_pos=(0.4, -0.297), resolution=(1080, 2424)), "確認預設手續費為0")
    except Exception as e:
        log(e, snapshot=True)
        
if poco(text="倉儲費").exists():
    try:
        assert_exists(Template(r"tpl1765434262775.png", record_pos=(0.431, -0.156), resolution=(1080, 2424)), "確認預設倉儲費為0")
    except Exception as e:
        log(e, snapshot=True)

try:
    assert_equal(poco(text="0").exists(), True, "確認預設獲得回饋為0")
except Exception as e:
    log(e, snapshot=True)
    
try:
    assert_exists(Template(r"tpl1754472220421.png", record_pos=(-0.006, 0.867), resolution=(1080, 2400)), "確認預設\"確認訂單\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1754467226028.png", record_pos=(0.419, -0.664), resolution=(1080, 2400)))
touch(Template(r"tpl1754467226028.png", record_pos=(0.419, -0.664), resolution=(1080, 2400)))
touch(Template(r"tpl1754467226028.png", record_pos=(0.419, -0.664), resolution=(1080, 2400)))

try:
    assert_equal(poco(text="$300").exists(), True, "確認轉售金額為300")
except Exception as e:
    log(e, snapshot=True)

if poco(text="手續費").exists():
    try:
        assert_exists(Template(r"tpl1765425932735.png", record_pos=(0.4, -0.297), resolution=(1080, 2424)), "確認手續費為0")
    except Exception as e:
        log(e, snapshot=True)
        
if poco(text="倉儲費").exists():
    try:
        assert_exists(Template(r"tpl1765434262775.png", record_pos=(0.431, -0.156), resolution=(1080, 2424)), "確認倉儲費為0")
    except Exception as e:
        log(e, snapshot=True)

try:
    assert_equal(poco(text="300").exists(), True, "確認獲得回饋為300")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1754469519588.png", record_pos=(0.156, -0.661), resolution=(1080, 2400)))

try:
    assert_equal(poco(text="$200").exists(), True, "確認轉售金額為200")
except Exception as e:
    log(e, snapshot=True)

if poco(text="手續費").exists():
    try:
        assert_exists(Template(r"tpl1765425932735.png", record_pos=(0.4, -0.297), resolution=(1080, 2424)), "確認手續費為0")
    except Exception as e:
        log(e, snapshot=True)
        
if poco(text="倉儲費").exists():
    try:
        assert_exists(Template(r"tpl1765434262775.png", record_pos=(0.431, -0.156), resolution=(1080, 2424)), "確認倉儲費為0")
    except Exception as e:
        log(e, snapshot=True)
    
try:
    assert_equal(poco(text="200").exists(), True, "確認獲得回饋為200")
except Exception as e:
    log(e, snapshot=True)
    
touch(Template(r"tpl1754469519588.png", record_pos=(0.156, -0.661), resolution=(1080, 2400)))
touch(Template(r"tpl1764752339888.png", record_pos=(-0.001, 0.964), resolution=(1080, 2424)))

try:
    assert_exists(Template(r"tpl1754471245090.png", record_pos=(-0.008, 0.013), resolution=(1080, 2400)), "確定要送出訂單嗎? bottom sheet 有彈出")
except Exception as e:
    log(e, snapshot=True)
    
touch(Template(r"tpl1754471399746.png", record_pos=(-0.007, 0.799), resolution=(1080, 2400)))
sleep(15)

try:
    assert_equal(poco(text="已成功送出訂單").exists(), True, "確認導到\"已成功送出訂單\"頁面")
except Exception as e:
    log(e, snapshot=True)


