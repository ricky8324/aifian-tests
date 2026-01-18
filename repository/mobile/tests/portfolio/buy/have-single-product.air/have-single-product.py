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
    
poco(text="威士忌新酒").swipe([0, -0.5])
sleep(3)

poco(text="測試威士忌").click()
sleep(3)

touch(Template(r"tpl1764647072781.png", record_pos=(0.274, 0.923), resolution=(1080, 2424)))
sleep(3)

touch(Template(r"tpl1761813161309.png", record_pos=(0.351, 0.397), resolution=(1080, 2424)))
sleep(3)
    
try:
    assert_exists(Template(r"tpl1761723842071.png", record_pos=(-0.261, -0.037), resolution=(1080, 2400)), "確認購買單品酒品有新增信用卡選項")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1756798285363.png", threshold=0.5999999999999999, record_pos=(-0.273, -0.025), resolution=(1080, 2400)), "確認購買單品酒品有銀行轉帳支付選項")
except Exception as e:
    log(e, snapshot=True)

touch(Template(r"tpl1756798271104.png", record_pos=(-0.005, 0.797), resolution=(1080, 2400)))
sleep(3)

touch(Template(r"tpl1756794548654.png", record_pos=(-0.132, 0.239), resolution=(1080, 2400)))

poco(text="繼續").click()
sleep(3)

touch(Template(r"tpl1764747121394.png", record_pos=(-0.004, 0.889), resolution=(1080, 2424)))
sleep(15)

try:
    assert_equal(poco(text="已成功送出訂單").exists(), True, "確認使用回饋購買單品酒品，最終導到\"已成功送出訂單\"頁面")
except Exception as e:
    log(e, snapshot=True)