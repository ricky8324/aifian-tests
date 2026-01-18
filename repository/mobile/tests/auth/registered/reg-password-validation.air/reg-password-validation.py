# -*- encoding=utf8 -*-
__author__ = "bella"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.report.report import simple_report
from airtest.core.assertions import assert_true
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
GRAY_CHECKS = Template(r"tpl1764749918270.png", record_pos=(-0.442, -0.152), resolution=(1080, 2424))
RED_CHECKS = Template("red_checks.png")
RED_DIG_CHECK = Template("red_digital_check.png")
RED_LEN_CHECK = Template("red_len_check.png")
RED_SPE_CHECK = Template("red_special_check.png")
RED_UPP_CHECK = Template("red_upper_check.png")
RED_LOW_CHECK = Template("red_lower_check.png")
RED_CONFIRM_BTN = Template(r"tpl1764749474623.png", record_pos=(0.0, 0.163), resolution=(1080, 2424))


auto_setup(__file__)
adb = device().adb
adb.shell("pm clear com.adenovo.aifianstg")

stop_app("com.adenovo.aifianstg")
start_app("com.adenovo.aifianstg")
sleep(8)


## 1. 在登入頁輸入未註冊過的手機號碼


# 1-1 檢查註冊登入頁面是否正常顯示

try:
    assert_equal(poco(text="建立帳號或登入").exists(), True, "成功顯示「註冊登入」頁面")
except Exception as e:
    log(e, snapshot=True)

# 1-2 輸入手機號碼，點擊繼續

poco("android.widget.EditText").set_text("0922123123")
poco(text="使用手機繼續").click()
sleep(3)

# 1-3 導至「輸入驗證碼」頁面

try:
    assert_equal(poco(text="輸入驗證碼").exists(), True, "成功顯示「輸入驗證碼」頁面")
except Exception as e:
    log(e, snapshot=True)

# 1-3-1 輸入驗證碼：123456

# 輸入驗証碼，為了相容 RN 跟 AN 的自動化
text("1")
text("2")
text("3")
text("4")
text("5")
text("6")
sleep(3)

# 1-4 導至「設定你的密碼」頁面

try:
    assert_equal(poco(text="設定你的密碼").exists(), True, "成功顯示「設定你的密碼」頁面")
    assert_equal(poco(text="長度 8-60 字元").exists(), True, "成功顯示設定密碼需滿足條件「長度 8-60 字元」")
    assert_equal(poco(text="至少 1 個特殊符號").exists(), True, "成功顯示設定密碼需滿足條件「至少 1 個特殊符號」")
    assert_equal(poco(text="至少 1 個數字").exists(), True, "成功顯示設定密碼需滿足條件「至少 1 個數字」")
    assert_equal(poco(text="至少 1 個大寫字母").exists(), True, "成功顯示設定密碼需滿足條件「至少 1 個大寫字母」")
    assert_equal(poco(text="至少 1 個小寫字母").exists(), True, "成功顯示設定密碼需滿足條件「至少 1 個小寫字母」")
except Exception as e:
    log(e, snapshot=True)
    
    
## 2. 於設定密碼頁面驗證密碼規則


# 2-1 沒有輸入密碼的狀況下，所有密碼符合條件皆反灰

try:
    assert exists(GRAY_CHECKS), "沒有輸入密碼的狀況下，所有密碼符合條件皆反灰"
except Exception as e:
    log(e, snapshot=True)
    
# 2-2 只輸入數字並到達字串長度 ->「長度 8-60 字元」及「至少 1 個數字」條件皆亮燈（打勾）

poco("android.widget.EditText").set_text("12345678")
assert_true(exists(RED_DIG_CHECK), "符合「至少 1 個數字」條件且有正確亮燈")
assert_true(exists(RED_LEN_CHECK), "符合「長度 8-60 字元」條件且有正確亮燈")

# 2-3 只輸入特殊符號，沒到達字串長度 -> 只有「至少 1 個特殊符號」條件亮燈（打勾）

poco("android.widget.EditText").set_text("")
poco("android.widget.EditText").set_text("$$$")
assert_true(exists(RED_SPE_CHECK), "符合「至少 1 個特殊符號」條件且有正確亮燈")

# 2-4 只輸入數字，沒到達字串長度 -> 只有「至少 1 個數字」條件亮燈（打勾）

poco("android.widget.EditText").set_text("")
poco("android.widget.EditText").set_text("123")
assert_true(exists(RED_DIG_CHECK), "符合「至少 1 個數字」條件且有正確亮燈")

# 2-5 只輸入大寫字母，沒到達字串長度 -> 只有「至少 1 個大寫字母」條件亮燈（打勾）

poco("android.widget.EditText").set_text("")
poco("android.widget.EditText").set_text("B")
assert_true(exists(RED_UPP_CHECK), "符合「至少 1 個大寫字母」條件且有正確亮燈")

# 2-6 只輸入小寫字母，沒到達字串長度 -> 只有「至少 1 個小寫字母」條件亮燈（打勾）

poco("android.widget.EditText").set_text("")
poco("android.widget.EditText").set_text("b")
assert_true(exists(RED_LOW_CHECK), "符合「至少 1 個小寫字母」條件且有正確亮燈")

# 2-7 輸入密碼全部條件都符合 -> 全部條件皆亮燈（打勾）

poco("android.widget.EditText").set_text("")
poco("android.widget.EditText").set_text("Bella222$")
assert_true(exists(RED_CHECKS), "滿足輸入密碼全部條件，且皆有正確亮燈")

# 2-8 輸入密碼全部條件都符合，「確定」CTA 從 disabled 更新為 clickable，但不執行 click

assert_true(exists(RED_CONFIRM_BTN), "「確定」按鈕已可點擊")

# 2-9 確認點擊眼睛之後，可以看到密碼
if exists(Template(r"tpl1759306993258.png", record_pos=(0.39, -0.494), resolution=(1080, 2400))):
    touch(Template(r"tpl1759306993258.png", record_pos=(0.39, -0.494), resolution=(1080, 2400)))
try:
    assert_equal(poco(text="Bella222$").exists(), True, "確認點擊眼睛之後，可以看到輸入之密碼")
except Exception as e:
    log(e, snapshot=True)
    
if exists(Template(r"tpl1759307056957.png", record_pos=(0.39, -0.493), resolution=(1080, 2400))):
    touch(Template(r"tpl1759307056957.png", record_pos=(0.39, -0.493), resolution=(1080, 2400)))
try:
    assert_equal(poco(text="•••••••••").exists(), True, "密碼有被正確隱碼")
except Exception as e:
    log(e, snapshot=True)
