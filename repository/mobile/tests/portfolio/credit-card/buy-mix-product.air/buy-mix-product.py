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
poco("android.widget.EditText").set_text("900752459")
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

poco("android.widget.EditText").set_text("Bella006")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
sleep(3)   

poco(text="智能選品").click()
sleep(3)

touch(Template(r"tpl1756793924662.png", record_pos=(0.232, 0.847), resolution=(1080, 2400)))
sleep(3)

touch(Template(r"tpl1761813161309.png", record_pos=(0.351, 0.397), resolution=(1080, 2424)))
sleep(3)


# CASE 1：信用卡失效，手續費連結，轉帳售優惠中和信用卡達上限
try:
    assert_exists(Template(r"tpl1764745631983.png", record_pos=(0.362, -0.381), resolution=(1080, 2424)), "確認失效的信用卡會顯示已過期")
except Exception as e:
    log(e, snapshot=True) 

try:
    assert_exists(Template(r"tpl1764745740902.png", record_pos=(0.34, 0.471), resolution=(1080, 2424)), "確認信用卡列表儲存五張後顯示已達上限")
except Exception as e:
    log(e, snapshot=True) 

# 信用卡選單從下往上划
swipe((500, 1500), (500, 500))

try:
    assert_exists(Template(r"tpl1764745914202.png", record_pos=(-0.064, 0.415), resolution=(1080, 2424)), "確認智能選品轉帳支付有轉售優惠中的TAG")
except Exception as e:
    log(e, snapshot=True) 

try:
    assert_exists(Template(r"tpl1764745939292.png", record_pos=(0.238, 0.566), resolution=(1080, 2424)), "確認信用卡列表頁有手續費規則連結")
except Exception as e:
    log(e, snapshot=True) 

# 為了相容 AN 和 RN 點擊選擇信用卡事件，所以點擊兩次信用卡    
touch(Template(r"tpl1764748261648.png", record_pos=(-0.255, -0.103), resolution=(1080, 2424)))
touch(Template(r"tpl1764748261648.png", record_pos=(-0.255, -0.103), resolution=(1080, 2424)))
sleep(3)
touch(Template(r"tpl1764747043766.png", record_pos=(-0.001, 0.895), resolution=(1080, 2424)))
sleep(3)

# CASE 2：信用卡購買智能選品
poco(text="繼續").click()
sleep(3)

touch(Template(r"tpl1764747121394.png", record_pos=(-0.004, 0.889), resolution=(1080, 2424)))
sleep(15)

try:
    assert_equal(poco(text="已成功送出訂單").exists(), True, "確認使用信用卡購買智能選品成功")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1764747686971.png", record_pos=(-0.001, 0.963), resolution=(1080, 2424)))
sleep(3)

# CASE 3：切換另一張信用卡購買智能選品
touch(Template(r"tpl1756793924662.png", record_pos=(0.232, 0.847), resolution=(1080, 2400)))
sleep(3)

touch(Template(r"tpl1761813161309.png", record_pos=(0.351, 0.397), resolution=(1080, 2424)))
sleep(3)

touch(Template(r"tpl1764748291050.png", record_pos=(-0.162, -0.209), resolution=(1080, 2424)))
sleep(3)
touch(Template(r"tpl1764747043766.png", record_pos=(-0.001, 0.895), resolution=(1080, 2424)))
sleep(3)

poco(text="繼續").click()
sleep(3)

touch(Template(r"tpl1764747121394.png", record_pos=(-0.004, 0.889), resolution=(1080, 2424)))
sleep(15)

try:
    assert_equal(poco(text="已成功送出訂單").exists(), True, "確認使用另一張信用卡購買智能選品成功")
except Exception as e:
    log(e, snapshot=True)
   