#!/bin/bash

# 定义默认代理服务器地址
DEFAULT_PX="127.0.0.1:7897"

# 获取用户输入的代理服务器地址
read -p "请输入Clash的代理服务器地址 [默认: $DEFAULT_PX]: " USER_PX

# 如果用户输入为空，则使用默认地址
PX=${USER_PX:-$DEFAULT_PX}

# 定义配置内容
CLASHRC_CONTENT=$(cat <<EOF
export no_proxy=localhost,127.0.0.0/8,*.local 
# 访问指定地址时不使用代理，可以用逗号分隔多个地址
export NO_PROXY=localhost,127.0.0.0/8,*.local
# export PX=192.168.0.101:7893 # NAS
export PX=$PX # 用户配置
export all_proxy=socks://\$PX/
export ALL_PROXY=socks://\$PX/
export http_proxy=http://\$PX
export HTTP_PROXY=http://\$PX
export ftp_proxy=http://\$PX
export FTP_PROXY=http://\$PX
export https_proxy=http://\$PX
export HTTPS_PROXY=http://\$PX
EOF
)

# 写入 .clashrc 文件
echo "正在创建/更新 ~/.clashrc 文件..."
echo "$CLASHRC_CONTENT" > ~/.clashrc
echo "~/.clashrc 文件已更新"

# 检查 .bashrc 中是否已存在 source 行
if ! grep -q "source ~/.clashrc" ~/.bashrc; then
    echo "正在更新 ~/.bashrc 文件..."
    echo "source ~/.clashrc" >> ~/.bashrc
    echo "已将 'source ~/.clashrc' 添加到 ~/.bashrc"
else
    echo "~/.bashrc 中已存在 source 行，跳过此步骤"
fi

# 检查 .zshrc 中是否已存在 source 行（如果文件存在）
if [ -f ~/.zshrc ]; then
    if ! grep -q "source ~/.clashrc" ~/.zshrc; then
        echo "正在更新 ~/.zshrc 文件..."
        echo "source ~/.clashrc" >> ~/.zshrc
        echo "已将 'source ~/.clashrc' 添加到 ~/.zshrc"
    else
        echo "~/.zshrc 中已存在 source 行，跳过此步骤"
    fi
fi

echo "代理环境变量设置完成！使用的代理服务器地址: $PX"
echo "请重启终端或执行 'source ~/.bashrc' 使设置生效"    