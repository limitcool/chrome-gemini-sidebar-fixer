# Chrome Gemini Sidebar Fixer (Chrome Gemini 侧边栏修复工具)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [中文](#中文)

---

## English

A script tool to fix the missing "Ask Gemini" (or Glic/Gemini sidebar) icon in the top right corner of Google Chrome.

### 📖 Introduction
Due to changes in Google Chrome's sidebar management logic, or regional policy restrictions in some locations, the Gemini sidebar icon may be hidden or unpinned.

This tool resolves the issue by:
1. Modifying `variations_permanent_consistency_country` from `cn` to `us` in the configuration to bypass regional restrictions.
2. Setting `is_glic_eligible` to `true` across all Chrome profiles to force-enable the Glic/Gemini sidebar feature.

### 🛠️ Usage
Please ensure you **completely close Google Chrome** before running the script (check the system tray or background tasks).

#### Option 1: One-Liner (Run directly in PowerShell without downloading)
Open PowerShell and copy-paste the following command to execute:
```powershell
irm https://raw.githubusercontent.com/limitcool/chrome-gemini-sidebar-fixer/main/fix_chrome.ps1 | iex
```

#### Option 2: Local Script (Python)
If Python is installed on your system:
```bash
python fix_chrome.py
```

#### Option 3: Local Script (PowerShell)
Right-click `fix_chrome.ps1` and choose **"Run with PowerShell"**, or execute the following in PowerShell:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\fix_chrome.ps1
```

### 📁 File Structure
* `fix_chrome.py`: Python version of the fix logic.
* `fix_chrome.ps1`: PowerShell version of the fix logic (fallback).
* `LICENSE`: MIT License.

---

## 中文

用于一键修复 Google Chrome 浏览器右上角 “问问 Gemini” (或 Glic/Gemini 侧边栏) 图标丢失问题的脚本工具。

### 📖 介绍
由于 Chrome 浏览器更新了侧边栏管理逻辑，或者在某些网络环境/地理位置限制下，Gemini 图标可能会被自动隐藏或取消固定。

本工具通过以下两种方式修复该问题：
1. 将 Chrome 配置文件中的 `variations_permanent_consistency_country` 从 `cn` 修改为 `us`，绕过区域策略限制。
2. 将所有 Chrome 用户配置文件（Profiles）中的 `is_glic_eligible` 设置为 `true`，以强制启用 Gemini 侧边栏功能。

### 🛠️ 使用方法
在运行脚本前，**请务必完全关闭 Google Chrome 浏览器**（检查系统托盘或后台进程，以防修改被覆盖）。

#### 方式 1：一键命令运行（无需下载，直接在 PowerShell 中执行）
打开 PowerShell 窗口，复制并运行以下命令：
```powershell
irm https://raw.githubusercontent.com/limitcool/chrome-gemini-sidebar-fixer/main/fix_chrome.ps1 | iex
```

#### 方式 2：本地运行 (Python)
如果您的系统上安装了 Python，可以直接运行：
```bash
python fix_chrome.py
```

#### 方式 3：本地运行 (PowerShell)
右键点击 `fix_chrome.ps1` 并选择 **“使用 PowerShell 运行”**，或者在 PowerShell 窗口中运行：
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\fix_chrome.ps1
```

### 📁 文件说明
* `fix_chrome.py`：Python 版本的修复核心逻辑。
* `fix_chrome.ps1`：PowerShell 版本的修复核心逻辑（备用）。
* `LICENSE`：MIT 开源许可证。

---

## License / 许可证
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目使用 MIT 许可证进行开源 - 详情请参阅 [LICENSE](LICENSE) 文件。
