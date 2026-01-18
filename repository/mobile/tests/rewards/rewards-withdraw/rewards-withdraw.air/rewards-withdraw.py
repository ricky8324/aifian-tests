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

touch(Template(r"tpl1755505252531.png", record_pos=(0.232, -0.975), resolution=(1080, 2400)))
touch(Template(r"tpl1764646328516.png", record_pos=(0.432, -0.887), resolution=(1080, 2424)))
sleep(3)
poco(text="轉出回饋").click()

try:
    assert_equal(poco(text="最小轉出數量為 500").exists(), True, "確認最小轉出數量為500的訊息有顯示")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1755505367223.png", record_pos=(-0.006, 0.069), resolution=(1080, 2400)), "確認預設\"下一步\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)

poco("android.widget.EditText").set_text("1234567890")
poco("android.widget.EditText").click()
text("8") #輸入第11位數

try:
    assert_equal(poco(text="1,234,567,890").exists(), True, "確認輸入回饋金額上限為10位數")
except Exception as e:
    log(e, snapshot=True)

poco("android.widget.EditText").set_text("499")
try:
    assert_exists(Template(r"tpl1755505367223.png", record_pos=(-0.006, 0.069), resolution=(1080, 2400)), "確認輸入499,\"下一步\"按鈕反灰")
except Exception as e:
    log(e, snapshot=True)

poco("android.widget.EditText").set_text("500")
try:
    assert_exists(Template(r"tpl1755505439376.png", record_pos=(-0.004, 0.074), resolution=(1080, 2400)), "確認輸入500,\"下一步\"按鈕亮起")
except Exception as e:
    log(e, snapshot=True)        

poco("android.widget.EditText").set_text("501")
try:
    assert_exists(Template(r"tpl1755505439376.png", record_pos=(-0.004, 0.074), resolution=(1080, 2400)), "確認輸入501,\"下一步\"按鈕亮起")
except Exception as e:
    log(e, snapshot=True) 
    
poco(text="下一步").click()
   
try:
    assert_equal(poco(text="501").exists(), True, "確認轉出數量為501")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_equal(poco(text="NT$501").exists(), True, "確認入帳金額為NT$501")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_equal(poco(text="Bella Hugh").exists(), True, "確認姓名為Bella Hugh")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_equal(poco(text="臺灣土地銀行 - 南港分行").exists(), True, "確認轉入銀行為臺灣土地銀行 - 南港分行")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="1111-1111-1111-11").exists(), True, "確認轉入帳號為1111-1111-1111-11")
except Exception as e:
    log(e, snapshot=True)

poco(text="確認轉出").click()
sleep(2)

try:
    assert_equal(poco(text="已成功送出回饋轉出申請").exists(), True, "確認 snackbar 顯示「已成功送出回饋轉出申請」")
except Exception as e:
    log(e, snapshot=True) 

poco(text="回饋轉出處理中").click() #讓 snackbar 顯示消失
sleep(3)
poco(text="回饋轉出處理中").click()
try:
    assert_equal(poco(text="501").exists(), True, "確認回饋紀錄表顯示該501的紀錄")
except Exception as e:
    log(e, snapshot=True)

