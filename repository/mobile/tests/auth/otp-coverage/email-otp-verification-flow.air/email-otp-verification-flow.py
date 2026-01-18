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

# 1. 帳號登入
poco("android.widget.EditText").set_text("0961000002")
poco(text="使用手機繼續").click()
sleep(5)

# 2. 發送第一次 SMS OTP 前不顯示 Email OTP，SMS OTP 有 60 秒倒數
try:
    assert_exists(Template(r"tpl1761200202425.png", record_pos=(0.057, -0.393), resolution=(1080, 2400)), "輸入驗證碼頁面，第一次發送 SMS OTP 有正確顯示 60 秒倒數")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_equal(poco(text="改發送到電子信箱").exists(), False, "輸入驗證碼頁面，第一次發送 SMS OTP，不顯示 Email OTP 選項和實際 Email")
except Exception as e:
    log(e, snapshot=True)
sleep(60)

# 3. 第一次 SMS OTP 發送 60 秒後，出現 Email OTP 選項（不顯示實際 Email 位址以符合安全規範）
try:
    assert_equal(poco(text="改發送到電子信箱").exists(), True, "輸入驗證碼頁面，第一次發送 SMS OTP 60 秒後，有顯示 Email OTP 選項，但不顯示實際 Email")
except Exception as e:
    log(e, snapshot=True)

# 4. 點擊「改發送到電子信箱」發送 Email OTP
poco(text="改發送到電子信箱").click()
try:
    assert_exists(Template(r"tpl1761200202425.png", record_pos=(0.057, -0.393), resolution=(1080, 2400)), "輸入驗證碼頁面，有正確顯示 60 秒倒數")
except Exception as e:
    log(e, snapshot=True)
sleep(60)

# 5. 點擊「重新發送」可以再次發送 SMS OTP
poco(text="重新發送").click()
try:
    assert_exists(Template(r"tpl1761200202425.png", record_pos=(0.057, -0.393), resolution=(1080, 2400)), "輸入驗證碼頁面，有正確顯示 60 秒倒數")
except Exception as e:
    log(e, snapshot=True)
sleep(60)

# 6. 非第一次發送 SMS OTP，60 秒倒數後，有顯示 Email OTP 選項
try:
    assert_equal(poco(text="如果仍沒收到代表此帳號沒有綁定的電子信箱").exists(), True, "輸入驗證碼頁面，非第一次發送 SMS OTP 60 秒後，有顯示 Email OTP 選項")
except Exception as e:
    log(e, snapshot=True)

# 7. 點擊左上角返回鍵， 回到帳號登入頁
touch(Template(r"tpl1764646351604.png", record_pos=(-0.407, -0.891), resolution=(1080, 2424)))
sleep(3)
try:
    assert_equal(poco(text="建立帳號或登入").exists(), True, "點擊左上角返回鍵，成功回到帳號登入頁")
except Exception as e:
    log(e, snapshot=True)