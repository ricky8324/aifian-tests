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
sleep(10)
      
# 1. 選擇用 Google 帳號（SSO）登入
poco(text="用 Google 繼續").click()
sleep(3)

# 2. 彈出視窗，選擇帳戶
poco(text="product_qa@aifian.com").click()
sleep(3)

# 3. 此 Google 帳號已經註冊過 AIFIAN
try:
    assert_equal(poco(text="此電子信箱已經註冊過，請使用註冊時的手機號碼與密碼登入。").exists(), True, "有正確顯示「帳號已存在，請直接登入」頁面")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_exists(Template(r"tpl1764906443875.png", record_pos=(-0.002, 0.059), resolution=(1080, 2424)), "有正確顯示帳號註冊時的末三碼：001")
except Exception as e:
    log(e, snapshot=True)

# 4. 點擊「使用手機號碼登入」CTA 回到註冊登入頁
poco(text="使用手機號碼登入").click()
try:
    assert_equal(poco(text="建立帳號或登入").exists(), True, "有正確顯示註冊登入頁")
except Exception as e:
    log(e, snapshot=True)