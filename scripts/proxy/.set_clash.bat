@REM # 如果 Clash 默认端口是 7890
set http_proxy=http://127.0.0.1:7895
set https_proxy=http://127.0.0.1:7895

set http_proxy=http://127.0.0.1:7895
set https_proxy=https://127.0.0.1:7895


@REM # 临时取消代理设置
set http_proxy=
set https_proxy=


set PX=127.0.0.1:7895
set all_proxy=socks://%PX%/
set ALL_PROXY=socks://%PX%/
set http_proxy=http://%PX%
set HTTP_PROXY=http://%PX%
set ftp_proxy=http://%PX%
set FTP_PROXY=http://%PX%
set https_proxy=http://%PX%
set HTTPS_PROXY=http://%PX%
