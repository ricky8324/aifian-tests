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
poco("android.widget.EditText").set_text("906060606")
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

poco(text="帳號").click()
poco(text="帳號與安全性").click()
poco(text="姓名").click()
poco(text="我已經依法改名").click()

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 8}:
        target_button = btn
        break
if target_button:
    target_button.set_text("J")

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 5}:
        target_button = btn
        break
if target_button:
    target_button.set_text("SAMPLEALEXANDER")

poco(text="證件正面").click()
if poco(text="使用應用程式時").exists():
    poco(text="使用應用程式時").click()  
    
touch(Template(r"tpl1757639961187.png", record_pos=(0.001, 0.822), resolution=(1080, 2400)))
sleep(3)

poco(text="上傳").click()
poco(text="證件反面").click()

touch(Template(r"tpl1757639961187.png", record_pos=(0.001, 0.822), resolution=(1080, 2400)))
sleep(3)
poco(text="上傳").click()


poco(text="送出審核").click()
try:
    assert_equal(poco(text="不可與目前姓名相同").exists(), True, "確認\"我已經依法改名\"選項輸入姓名相同時出現提示訊息")
except Exception as e:
    log(e, snapshot=True)

poco(name="com.horcrux.svg.B").click()
poco(text="姓名").click()
poco(text="我已經依法改名").click()

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 8}:
        target_button = btn
        break
if target_button:
    target_button.set_text("Tang")

try:
    assert_exists(Template(r"tpl1757580149919.png", record_pos=(-0.001, 0.882), resolution=(1080, 2400)), "確認\"我已經依法改名\"選項裡，只輸入姓氏，\"送出審核\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 8}:
        target_button = btn
        break
if target_button:
    target_button.set_text("")

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 5}:
        target_button = btn
        break
if target_button:
    target_button.set_text("Chris")

try:
    assert_exists(Template(r"tpl1757580149919.png", record_pos=(-0.001, 0.882), resolution=(1080, 2400)), "確認\"我已經依法改名\"選項，只輸入名字，\"送出審核\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)

button = poco("android.widget.EditText")
for btn in button:
    zorders = btn.attr("zOrders")
    if zorders == {'global': 0, 'local': 8}:
        target_button = btn
        break
if target_button:
    target_button.set_text("Tang")

try:
    assert_exists(Template(r"tpl1757580149919.png", record_pos=(-0.001, 0.882), resolution=(1080, 2400)), "確認\"我已經依法改名\"選項，姓名和名字皆輸入但尚未上傳証件照，\"送出審核\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)
    
poco(text="證件正面").click() 
    
touch(Template(r"tpl1757639961187.png", record_pos=(0.001, 0.822), resolution=(1080, 2400)))
sleep(3)

poco(text="上傳").click()
poco(text="證件反面").click()

touch(Template(r"tpl1757639961187.png", record_pos=(0.001, 0.822), resolution=(1080, 2400)))
sleep(3)
poco(text="上傳").click()    
       
try:
    assert_exists(Template(r"tpl1757580564993.png", record_pos=(0.0, 0.885), resolution=(1080, 2400)), "確認\"我已經依法改名\"選項，姓名和名字皆輸入且上傳完証件照，\"送出審核\"按鈕亮起")
except Exception as e:
    log(e, snapshot=True)

poco(text="送出審核").click()
try:
    assert_equal(poco(text="請確認姓名與銀行帳戶一致").exists(), True, "確認\"我已經依法改名\"選項，送出審核會跳出\"送請確認姓名與銀行帳戶一致\"的視窗")
except Exception as e:
    log(e, snapshot=True)

poco(text="返回修改").click()
try:
    assert_equal(poco(text="上傳證件").exists(), True, "確認\"我已經依法改名\"選項，送出審核後點擊\"返回修改\"按鈕會回到上傳證件頁面")
except Exception as e:
    log(e, snapshot=True)