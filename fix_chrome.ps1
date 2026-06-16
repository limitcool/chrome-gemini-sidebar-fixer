# PowerShell version of Chrome Gemini configuration fixer
$ErrorActionPreference = "Stop"

Write-Host "Initializing PowerShell fixer... / 正在初始化 PowerShell 修复程序..."

$localAppData = $env:LOCALAPPDATA
if (-not $localAppData) {
    Write-Error "Unable to get LOCALAPPDATA environment variable! / 无法获取系统 LOCALAPPDATA 环境变量！"
    Exit
}

$filePath = Join-Path $localAppData "Google\Chrome\User Data\Local State"
$backupPath = "$filePath.bak"

if (-not (Test-Path $filePath)) {
    Write-Host "[ERROR / 错误] Chrome configuration file not found at: $filePath"
    Write-Host "未找到 Chrome 配置文件，请确认您是否安装了 Google Chrome 浏览器。"
    Exit
}

# Backup
try {
    Copy-Item $filePath $backupPath -Force
    Write-Host "[SUCCESS / 成功] Original configuration backed up to: $backupPath"
    Write-Host "已将原始配置文件备份至: $backupPath"
} catch {
    Write-Host "[WARNING / 警告] Backup failed: $_. Proceeding anyway. / 创建备份失败: $_，将继续尝试修复。"
}

# Read and parse JSON
try {
    $rawContent = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    $data = $rawContent | ConvertFrom-Json
} catch {
    Write-Host "[ERROR / 错误] Failed to read/parse configuration: $_ / 读取或解析配置文件失败: $_"
    Exit
}

$modified = $false

# 1. Modify variations_permanent_consistency_country
if ($data.variations_permanent_consistency_country) {
    $val = $data.variations_permanent_consistency_country
    if ($val -is [array]) {
        for ($i = 0; $i -lt $val.Count; $i++) {
            if ($val[$i] -eq "cn") {
                $val[$i] = "us"
                $modified = $true
                Write-Host "-> Modified variations_permanent_consistency_country list value 'cn' -> 'us'"
                Write-Host "-> 已将 variations_permanent_consistency_country 中的 'cn' 修改为 'us'"
            } elseif ($val[$i] -eq "CN") {
                $val[$i] = "US"
                $modified = $true
                Write-Host "-> Modified variations_permanent_consistency_country list value 'CN' -> 'US'"
                Write-Host "-> 已将 variations_permanent_consistency_country 中的 'CN' 修改为 'US'"
            }
        }
    } else {
        if ($val -eq "cn") {
            $data.variations_permanent_consistency_country = "us"
            $modified = $true
            Write-Host "-> Modified variations_permanent_consistency_country from 'cn' -> 'us'"
            Write-Host "-> 已将 variations_permanent_consistency_country 从 'cn' 修改为 'us'"
        }
    }
}

# 2. Modify is_glic_eligible
$modifiedGlicCount = 0
if ($data.profile -and $data.profile.info_cache) {
    $infoCache = $data.profile.info_cache
    foreach ($profileName in $infoCache.psobject.Properties.Name) {
        $profile = $infoCache.$profileName
        if ($profile.is_glic_eligible -ne $null -and $profile.is_glic_eligible -ne $true) {
            $profile.is_glic_eligible = $true
            $modifiedGlicCount++
            $modified = $true
        }
    }
}

if ($modifiedGlicCount -gt 0) {
    Write-Host "-> Set 'is_glic_eligible' to True in $modifiedGlicCount profiles."
    Write-Host "-> 已在 $modifiedGlicCount 个 Chrome 配置文件中将 'is_glic_eligible' 设置为 True"
}

# Write back
if ($modified) {
    try {
        $newJson = $data | ConvertTo-Json -Depth 100 -Compress
        [System.IO.File]::WriteAllText($filePath, $newJson, [System.Text.Encoding]::UTF8)
        Write-Host "[SUCCESS / 成功] Fixes successfully written to Chrome configuration! / 修复更改已成功写入 Chrome 配置文件！"
    } catch {
        Write-Host "[ERROR / 错误] Failed to write configuration: $_ / 写入配置文件失败: $_"
    }
} else {
    Write-Host "[INFO / 提示] Configuration values are already fixed, no modification needed."
    Write-Host "配置文件中的对应值已经处于修复后状态，无需重复修改。"
}

Write-Host "`nPress Enter to exit... / 按回车键退出程序..."
Read-Host
