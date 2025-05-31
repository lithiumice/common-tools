# 访问指定地址时不使用代理，可以用逗号分隔多个地址
export no_proxy=localhost,127.0.0.0/8,*.local 
export NO_PROXY=localhost,127.0.0.0/8,*.local

export PX=127.0.0.1:7895
export all_proxy=socks://$PX/
export ALL_PROXY=socks://$PX/
export http_proxy=http://$PX
export HTTP_PROXY=http://$PX
export ftp_proxy=http://$PX
export FTP_PROXY=http://$PX
export https_proxy=http://$PX
export HTTPS_PROXY=http://$PX
