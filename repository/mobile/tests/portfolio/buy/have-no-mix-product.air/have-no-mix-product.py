# -*- encoding=utf8 -*-
__author__ = "chris"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.report.report import simple_report
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
auto_setup(__file__)

#adb = device().adb
#adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifian")
start_app("com.adenovo.aifian")
sleep(8)

# 帳號登入
#poco("android.widget.EditText").set_text("906060606")
#poco(text="使用手機繼續").click()
#sleep(3)
# 輸入驗証碼，為了相容 RN 跟 AN 的自動化
#text("1")
#text("2")
#text("3")
#text("4")
#text("5")
#text("6")
#sleep(3)

#poco("android.widget.EditText").set_text("@Ss8654092")
#poco(text="登入").click()
#sleep(3)

#if poco(text="允許").exists():
#    poco("com.android.permissioncontroller:id/permission_allow_button").click()
#sleep(5)

#if exists(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400))):
#    touch(Template(r"tpl1754454689013.png", record_pos=(0.374, -0.549), resolution=(1080, 2400)))
#sleep(3)    
    
# CASE1: 未持有智能選品
try:
    assert_exists(Template(r"tpl1764839611270.png", record_pos=(0.0, -0.563), resolution=(1080, 2424)), "確定增值首頁未持有智能選品畫面正確")
except Exception as e:
    log(e, snapshot=True)

poco(text="智能選品").click()

try:
    assert_exists(Template(r"tpl1764839821555.png", record_pos=(-0.358, -0.157), resolution=(1080, 2424)), "確認未持有智能選品，細節頁持有現值為0")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1764839837186.png", record_pos=(-0.019, -0.156), resolution=(1080, 2424)), "確認未持有智能選品，細節頁持有瓶數為0")
except Exception as e:
    log(e, snapshot=True)

swipe(Template(r"tpl1756450306694.png", record_pos=(-0.334, 0.093), resolution=(1080, 2400)), vector=[0.0115, -0.3505])

try:
    assert_equal(poco(text="回饋計算機").exists(), True, "確認未持有智能選品，細節頁顯示回饋計算機")
except Exception as e:
    log(e, snapshot=True)


