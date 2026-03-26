@echo off
chcp 65001 >nul
echo ========================================
echo ABM 仿真实验分析报告 - LaTeX 编译脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 清理中间文件...
del /q *.aux *.log *.out *.toc *.lof *.lot 2>nul

echo [2/3] 第一次编译...
xelatex -interaction=nonstopmode main.tex >nul 2>&1

echo [3/3] 第二次编译（解决引用）...
xelatex -interaction=nonstopmode main.tex >nul 2>&1

echo.
if exist main.pdf (
    echo ========================================
    echo [OK] 编译成功！
    echo ========================================
    echo 生成的 PDF 文件：main.pdf
    echo.
    echo 正在打开 PDF 文件...
    start main.pdf
) else (
    echo ========================================
    echo [ERROR] 编译失败！
    echo ========================================
    echo 请检查：
    echo 1. 是否安装了 XeTeX 或 TeX Live
    echo 2. main.tex 文件是否存在语法错误
    echo ========================================
)

echo.
pause
