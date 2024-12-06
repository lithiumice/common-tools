@echo off
:: proxy-toggle.bat

if "%1"=="on" (
    echo Enabling proxy...
    set http_proxy=http://127.0.0.1:7890
    set https_proxy=http://127.0.0.1:7890
    echo Proxy enabled
) else if "%1"=="off" (
    echo Disabling proxy...
    set http_proxy=
    set https_proxy=
    echo Proxy disabled
) else (
    echo Usage: proxy-toggle [on^|off]
    echo Current proxy settings:
    echo http_proxy: %http_proxy%
    echo https_proxy: %https_proxy%
)