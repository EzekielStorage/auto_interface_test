@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ==============================
:: 固定配置区（可按需修改）
:: ==============================
set TEST_PATH=C:\Users\Administrator\Desktop\250526\code\interface_test_example
set LOG_PATH=C:\Users\Administrator\Desktop\250526\code\interface_test_example\logs_bat
set CONFIG_FILE=%TEST_PATH%\batch_runtest.yaml

:: ==============================
:: 参数处理
:: %1 = pytest 额外参数
:: ==============================

:: 拼接 pytest 额外参数
set PYTEST_ARGS=
shift

:loop_args
if "%~1"=="" goto start
set PYTEST_ARGS=!PYTEST_ARGS! %~1
shift
goto loop_args

:start

echo ==============================
echo 固定测试路径：%TEST_PATH%
echo 配置文件：%CONFIG_FILE%
echo 额外参数：%PYTEST_ARGS%
echo ==============================

:: ==============================
:: 执行前切换目录（关键优化）
:: ==============================
cd /d %TEST_PATH%

if errorlevel 1 (
    echo [ERROR] 路径不存在：%TEST_PATH%
    pause
    exit /b 1
)

:: 创建日志目录
if not exist "%LOG_PATH%" (
    mkdir "%LOG_PATH%"
)

:: ==============================
:: 从 YAML 文件读取配置并执行
:: ==============================
set FAIL_COUNT=0
set TOTAL_COUNT=0

:: 使用 PowerShell 解析 YAML 文件并生成临时脚本
powershell -Command ^
    "$yamlPath = '%CONFIG_FILE%'; "^
    "$content = Get-Content $yamlPath -Raw; "^
    "$lines = $content -split \"`n\"; "^
    "$inExample = $false; "^
    "foreach ($line in $lines) { "^
    "    if ($line -match '^example:') { $inExample = $true; continue } "^
    "    if ($inExample -and $line -match '^\s+(\S+):\s+(\d+)') { "^
    "        Write-Output \"$($matches[1])=$($matches[2])\" "^
    "    } "^
    "    if ($inExample -and $line -match '^\S' -and $line -notmatch ':') { break } "^
    "}" > "%TEMP%\test_config.txt"

:: 读取解析结果并执行
for /f "tokens=*" %%a in (%TEMP%\test_config.txt) do (
    for /f "tokens=1,2 delims==" %%i in ("%%a") do (
        set TEST_NAME=%%i
        set RUN_COUNT=%%j

        echo.
        echo ===== 执行测试用例：!TEST_NAME! (!RUN_COUNT! 次) =====

        for /l %%k in (1,1,!RUN_COUNT!) do (
            :: 生成时间戳
            for /f %%t in ('powershell -command "[int64](Get-Date -UFormat %%s) * 1000"') do set TIMESTAMP=%%t

            set /a TOTAL_COUNT+=1

            :: 输出日志（每次一个文件）
            echo 执行：pytest . --test_example_name=!TEST_NAME! !PYTEST_ARGS!

            set "LOG_FILE=%LOG_PATH%\result_!TEST_NAME!_!TIMESTAMP!_%%k.log"
            pytest . --test_example_name=!TEST_NAME! !PYTEST_ARGS! > "!LOG_FILE!"

            if errorlevel 1 (
                echo [FAIL] !TEST_NAME! 第 %%k 次执行失败
                set /a FAIL_COUNT+=1
            ) else (
                echo [PASS] !TEST_NAME! 第 %%k 次执行成功
            )
        )
    )
)

:: 清理临时文件
del "%TEMP%\test_config.txt" >nul 2>&1

:: ==============================
:: 汇总结果
:: ==============================
echo.
echo ==============================
echo 总执行次数：%TOTAL_COUNT%
echo 失败次数：%FAIL_COUNT%
echo 成功次数：%TOTAL_COUNT% - %FAIL_COUNT%
echo ==============================

pause
