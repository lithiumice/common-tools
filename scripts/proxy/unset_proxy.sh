proxy_off() {
    unset http_proxy
    unset https_proxy
    unset ftp_proxy
    unset all_proxy
    unset no_proxy
    echo "代理已关闭"
}