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

# 1. 帳號登入
poco("android.widget.EditText").set_text("0963000001")
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
poco("android.widget.EditText").set_text("Bella001$")
poco(text="登入").click()
sleep(3)

if poco(text="允許").exists():
    poco("com.android.permissioncontroller:id/permission_allow_button").click()
sleep(5)

# 1-1 若有公告卡，點擊「X」關閉公告卡
if exists(Template(r"tpl1761720140599.png", record_pos=(0.385, -0.513), resolution=(1080, 2400))):
    touch(Template(r"tpl1761720140599.png", record_pos=(0.385, -0.513), resolution=(1080, 2400)))
sleep(3)
          
# 2. 點擊小鈴鐺，進入通知中心畫面，預設在「全部」tab
touch(Template(r"tpl1764658800111.png", record_pos=(-0.447, -0.884), resolution=(1080, 2424)))
sleep(5)

try:
    assert_equal(poco(text="通知").exists(), True, "成功進入通知中心頁面")
except Exception as e:
    log(e, snapshot=True)

try:
    assert_exists(Template(r"tpl1761720483543.png", record_pos=(0.079, -0.48), resolution=(1080, 2400)), "進入通知中心畫面，且預設在「帳戶動態」tab")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_exists(Template(r"tpl1761724393476.png", record_pos=(-0.43, 0.085), resolution=(1080, 2400)), "「帳戶動態」tab 有正常顯示推播通知訊息")
except Exception as e:
    log(e, snapshot=True)
          
# 3. 可以切換至「產品新訊」tab，畫面只出現公告卡片訊息（用圖示區別：大聲公）
poco(text="產品新訊").click()
try:
    assert_exists(Template(r"tpl1761720460762.png", record_pos=(-0.171, -0.481), resolution=(1080, 2400)), "成功切換至「產品新訊」tab")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_exists(Template(r"tpl1761724267057.png", record_pos=(-0.43, 0.398), resolution=(1080, 2400)), "「產品新訊」tab 有正常顯示公告卡片訊息")
except Exception as e:
    log(e, snapshot=True)
          
# 4. 可以切換至「客服訊息」tab，無通知時會有「Cheers！所有訊息都被你接住了。」提示
poco(text="客服訊息").click()
try:
    assert_exists(Template(r"tpl1765179530970.png", record_pos=(0.124, -0.649), resolution=(1080, 2424)), "成功切換至「客服訊息」tab")
except Exception as e:
    log(e, snapshot=True)
try:
    assert_equal(poco(text="Cheers！所有訊息都被你接住了。").exists(), True, "客服訊息無通知時會有「Cheers！所有訊息都被你接住了。」提示")
except Exception as e:
    log(e, snapshot=True)

# 5. 開啟「僅顯示未讀」開關，會出現「全部已讀」按鈕並判斷是 React 還是 Android native 介面
poco(text="帳戶動態").click()
if poco("android.widget.Switch").exists():
    poco("android.widget.Switch").click()
    try:
        assert_exists(Template(r"tpl1761721104108.png", record_pos=(0.415, -0.346), resolution=(1080, 2400)), "成功打開「僅顯示未讀」toggle")
    except Exception as e:
        log(e, snapshot=True)
else:
    touch(Template(r"tpl1764660842926.png", record_pos=(0.394, -0.497), resolution=(1080, 2424)))
    try:
        assert_exists(Template(r"tpl1764660901206.png", record_pos=(0.396, -0.497), resolution=(1080, 2424)), "成功打開「僅顯示未讀」toggle")
    except Exception as e:
        log(e, snapshot=True)
                  
btn = poco(text="全部已讀")
assert_true(btn.exists() and btn.attr("enabled"), "開啟「僅顯示未讀」開關，會出現「全部已讀」按鈕，「全部已讀」按鈕為可點擊")
  
# 6. 確認「僅顯示未讀」開啟時，切換 tab，該頁面也會出現「全部已讀」按鈕
poco(text="產品新訊").click()
assert_true(btn.exists() and btn.attr("enabled"), "切換到「產品新訊」tab，有顯示「全部已讀」按鈕，且為可點擊")
poco(text="帳戶動態").click()
assert_true(btn.exists() and btn.attr("enabled"), "切換到「帳戶動態」tab，有顯示「全部已讀」按鈕，且為可點擊")

# 7. 將「僅顯示未讀」toggle 關閉時，則不會看見「全部已讀」按鈕並判斷是 React 還是 Android native 介面
btn_allread = poco(text="全部已讀")
if poco("android.widget.Switch").exists():
    poco("android.widget.Switch").click()
else:
    touch(Template(r"tpl1764660901206.png", record_pos=(0.396, -0.497), resolution=(1080, 2424)))
assert_true((not btn_allread.exists()) or (not btn_allread.attr("visible")), "關閉『僅顯示未讀』時，畫面不應顯示「全部已讀」按鈕")
