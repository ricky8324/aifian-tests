import os
import sys
import zipfile
import json
import requests
import sys
import glob
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
REPORT_BASE = "airtest-report"
ZIP_OUTPUT = os.path.join(os.getcwd(), "airtest-report.zip")

def zip_reports():
    if not os.path.exists(REPORT_BASE):
        print("❗ Report directory not found.")
        return

    print(f"[DEBUG] Current working dir: {os.getcwd()}")
    print("[DEBUG] Starting zip...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(REPORT_BASE):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, REPORT_BASE)
                print(f"[DEBUG] Adding to zip: {file_path}")
                zipf.write(file_path, arcname)
                
    if os.path.exists(ZIP_OUTPUT):
        print(f"✅ 測試報告已壓縮為 {ZIP_OUTPUT}")
    else:
        print("❌ 壓縮報告失敗，找不到 zip 檔案")


def load_results():
    all_results = []
    result_files = glob.glob("airtest_results_*.json")
    
    if not result_files:
        print("❗ 找不到任何 airtest_results_*.json 檔案")
        return []

    for path in result_files:
        print(f"[DEBUG] Loading results from: {path}")
        try:
            with open(path, "r") as f:
                results = json.load(f)
                all_results.extend(results)
        except Exception as e:
            print(f"⚠️ 讀取 {path} 發生錯誤: {e}")
    
    return all_results

def notify_slack(results):
    if not SLACK_WEBHOOK:
        print("⚠️ SLACK_WEBHOOK 未設定，跳過 Slack 通知")
        return

    failed = [r for r in results if r["status"] == "FAIL"]
    if not failed:
        print("✅ 所有測試通過，不發送 Slack 通知")
        return

    # 構建失敗測試訊息
    lines = [f"❌ *{r['name']}*" for r in failed]
    summary = "\n".join(lines)

    # GitHub 相關資訊
    run_id = os.getenv("GITHUB_RUN_ID")
    repository = os.getenv("GITHUB_REPOSITORY")  # e.g. org/repo
    artifact_url = f"https://github.com/{repository}/actions/runs/{run_id}"

    payload = {
        "text": f"*❌ Airtest 測試失敗通知*\n{summary}\n📎 [下載測試報告 Artifact]({artifact_url})"
    }

    response = requests.post(SLACK_WEBHOOK, json=payload)
    print("📨 Slack 發送結果:", response.status_code, response.text)

def main():
    zip_reports()
    results = load_results()
    notify_slack(results)

    # 根據結果判斷是否讓 Job 失敗
    has_fail = any(r["status"] == "FAIL" for r in results)
    if has_fail:
        print("❌ 有測試失敗，GitHub Actions 將標記為失敗")
        sys.exit(1)
    else:
        print("✅ 所有測試通過，GitHub Actions 為成功")

if __name__ == "__main__":
    main()
