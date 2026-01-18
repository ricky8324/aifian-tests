# -*- encoding=utf8 -*-
__author__ = "bella"

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

## 1. 在登入頁輸入已經註冊過的手機號碼

# 1-1 檢查註冊登入頁面是否正常顯示
try:
    assert_equal(poco(text="建立帳號或登入").exists(), True, "成功顯示「註冊登入」頁面")
except Exception as e:
    log(e, snapshot=True)

    
# 1-2 輸入手機號碼，點擊繼續
poco("android.widget.EditText").set_text("0900752549")
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


# 1-4 導至「嗨！歡迎回來」頁面（輸入密碼頁面）
try:
    assert_equal(poco(text="嗨！ 歡迎回來").exists(), True, "成功顯示「輸入密碼」頁面")
except Exception as e:
    log(e, snapshot=True)