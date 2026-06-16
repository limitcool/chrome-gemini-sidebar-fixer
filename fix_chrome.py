import os
import json
import shutil
import sys
import subprocess

def check_chrome_running():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq chrome.exe"', shell=True).decode('gbk', errors='ignore')
        return "chrome.exe" in output.lower()
    except:
        return False

def main():
    print("Initializing fixer... / 正在初始化修复程序...")
    
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        print("[ERROR / 错误] Unable to get LOCALAPPDATA environment variable! / 无法获取系统 LOCALAPPDATA 环境变量！")
        return
        
    file_path = os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Local State')
    backup_path = file_path + '.bak'
    
    if not os.path.exists(file_path):
        print(f"[ERROR / 错误] Chrome configuration file not found at: {file_path}")
        print("未找到 Chrome 配置文件，请确认您是否安装了 Google Chrome 浏览器。")
        return

    if check_chrome_running():
        print("\n[WARNING / 警告] Chrome browser seems to be running. / Chrome 浏览器似乎仍在运行。")
        print("Please close Chrome completely (including background processes), otherwise changes may be overwritten!")
        print("请完全关闭 Chrome（包括系统托盘图标和后台运行的 Chrome 进程），否则修改可能会被 Chrome 覆写！")
        choice = input("Have you completely closed Chrome? / 您是否已完全关闭 Chrome？(Y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("Fix cancelled. Please close Chrome and run again. / 修复已取消，请关闭 Chrome 后重新运行。")
            return

    # Backup
    try:
        shutil.copy2(file_path, backup_path)
        print(f"[SUCCESS / 成功] Original configuration backed up to: {backup_path}")
        print(f"已将原始配置文件备份至: {backup_path}")
    except Exception as e:
        print(f"[WARNING / 警告] Backup failed: {e}. Proceeding anyway. / 创建备份失败: {e}，将继续尝试修复。")

    # Read and modify JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR / 错误] Failed to read/parse configuration: {e} / 读取或解析配置文件失败: {e}")
        return

    modified = False

    # 1. Modify variations_permanent_consistency_country
    if 'variations_permanent_consistency_country' in data:
        val = data['variations_permanent_consistency_country']
        if isinstance(val, list):
            if 'cn' in val:
                idx = val.index('cn')
                val[idx] = 'us'
                modified = True
                print("-> Modified variations_permanent_consistency_country list value 'cn' -> 'us'")
                print("-> 已将 variations_permanent_consistency_country 中的 'cn' 修改为 'us'")
            elif 'CN' in val:
                idx = val.index('CN')
                val[idx] = 'US'
                modified = True
                print("-> Modified variations_permanent_consistency_country list value 'CN' -> 'US'")
                print("-> 已将 variations_permanent_consistency_country 中的 'CN' 修改为 'US'")
        elif isinstance(val, str):
            if val.lower() == 'cn':
                data['variations_permanent_consistency_country'] = 'us'
                modified = True
                print("-> Modified variations_permanent_consistency_country string value 'cn' -> 'us'")
                print("-> 已将 variations_permanent_consistency_country 从 'cn' 修改为 'us'")

    # 2. Modify is_glic_eligible
    modified_glic_count = 0
    def modify_glic(d):
        nonlocal modified_glic_count, modified
        if isinstance(d, dict):
            for k, v in d.items():
                if k == 'is_glic_eligible':
                    if d[k] is not True:
                        d[k] = True
                        modified_glic_count += 1
                        modified = True
                else:
                    modify_glic(v)
        elif isinstance(d, list):
            for item in d:
                modify_glic(item)

    modify_glic(data)
    if modified_glic_count > 0:
        print(f"-> Set 'is_glic_eligible' to True in {modified_glic_count} profiles.")
        print(f"-> 已在 {modified_glic_count} 个 Chrome 配置文件中将 'is_glic_eligible' 设置为 True")

    # Write back
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("[SUCCESS / 成功] Fixes successfully written to Chrome configuration! / 修复更改已成功写入 Chrome 配置文件！")
        except Exception as e:
            print(f"[ERROR / 错误] Failed to write configuration: {e} / 写入配置文件失败: {e}")
    else:
        print("[INFO / 提示] Configuration values are already fixed, no modification needed.")
        print("配置文件中的对应值已经处于修复后状态，无需重复修改。")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[EXCEPTION / 异常] Error during execution: {e} / 运行中发生错误: {e}")
    input("\nPress Enter to exit... / 按回车键退出程序...")
