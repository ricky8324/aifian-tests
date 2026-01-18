import os
import io
import subprocess
import json
from datetime import datetime
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# === CONFIG ===
PYTHON = "/opt/homebrew/bin/python3.9"
DEVICE = "Android://127.0.0.1:5037/R5CW20A8NQJ"
TEST_ROOT = "repository/mobile/tests"
# MODULES = ["account", "auth", "login", "message-hub", "portfolio", "rewards"]  # 模組依需求增減
MODULES = ["portfolio"]

# === MAIN ===
def run_airtest_module(module_name):
    AIRTEST_ROOT = os.path.join(TEST_ROOT, module_name)
    LOG_DIR = os.path.join("logdir", module_name)
    REPORT_DIR = os.path.join("airtest-report", module_name)

    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    test_results = []

    for root, dirs, files in os.walk(AIRTEST_ROOT):
        for item in dirs:
            if item.endswith(".air"):
                airtest_path = os.path.join(root, item)

                # 確保是資料夾
                if not os.path.isdir(airtest_path):
                    continue

                # 相對於 AIRTEST_ROOT 的路徑
                rel_path = os.path.relpath(airtest_path, TEST_ROOT)
                parts = rel_path.split(os.sep)

                # 路徑三層結構
                group = parts[0] if len(parts) >= 1 else "unknown"
                subfolder = parts[1] if len(parts) >= 2 else ""
                filename = parts[2] if len(parts) >= 3 else parts[-1]

                base_name = filename.replace(".air", "")
                rel_name = f"[{group}]/[{subfolder}]: {filename}" if subfolder else f"[{group}]: {filename}"
                safe_name = f"{base_name}"

                print(f"\n🚀 Running Airtest project: {rel_name}")
                print(f"[DEBUG] airtest_path: {airtest_path}")

                # log 資料夾名稱需安全處理（移除非法字元）
                log_path = os.path.join(LOG_DIR, subfolder, filename)
                report_dir = os.path.join(REPORT_DIR, subfolder)
                os.makedirs(log_path, exist_ok=True)
                os.makedirs(report_dir, exist_ok=True)

                print(f"[DEBUG] log_path: {log_path}")
                print(f"[DEBUG] report_dir: {report_dir}")

                # 執行測試
                is_failed = False

                try:
                    subprocess.run([
                        PYTHON, "-m", "airtest", "run", airtest_path,
                        "--device", DEVICE,
                        "--log", log_path
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    is_failed = True
                    print(f"[ERROR] Airtest execution failed for {rel_name}")
                    print(f"        Exit code: {e.returncode}")
                    print(f"        Command: {e.cmd}")

                # 產生報告
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                report_filename = f"{safe_name}-{timestamp}.html"
                report_path = os.path.join(report_dir, report_filename)

                try:
                    subprocess.run([
                        PYTHON, "-m", "airtest", "report", airtest_path,
                        "--log_root", log_path,
                        "--outfile", report_path,
                        "--lang", "zh"
                    ], check=True)
                    print(f"[INFO] Report generated at {report_path}")
                except Exception as e:
                    print(f"⚠️ Failed to generate report for {rel_name}: {e}")

                # 判斷失敗
                log_txt = os.path.join(log_path, "log.txt")
                if not is_failed and os.path.exists(log_txt):
                    with open(log_txt, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                        if "assertionerror" in content:
                            is_failed = True
                            print(f"[Error] {rel_name} failed due to AssertionError in log.txt")

                if not is_failed and os.path.exists(report_path):
                    with open(report_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                        fail_logs = soup.select(".log.fail")
                        if len(fail_logs) > 0:
                            is_failed = True
                            print(f"[Error] {rel_name} failed due to fail log block in HTML")

                test_results.append({
                    "name": rel_name,
                    "status": "FAIL" if is_failed else "PASS"
                })

    # 儲存 JSON 結果
    result_filename = f"airtest_results_{module_name}.json"
    with open(result_filename, "w") as f:
        json.dump(test_results, f, indent=2)

    print(f"\n📦 測試完成，結果儲存於 {result_filename}")

    # 顯示總結
    num_fail = sum(1 for r in test_results if r["status"] == "FAIL")
    if num_fail > 0:
        print(f"❌ {num_fail} test(s) failed.")
    else:
        print("✅ All tests passed.")

# === 執行所有模組 ===
if __name__ == "__main__":
    for module in MODULES:
        run_airtest_module(module)
