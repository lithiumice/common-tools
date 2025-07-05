#!/bin/bash

# Ubuntu APT 源自动替换脚本 (清华源)
# 支持 Ubuntu 20.04 (focal)、22.04 (jammy)、24.04 (noble) 等常见版本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$(id -u)" -ne 0 ]; then
   echo -e "${RED}错误: 此脚本需要 root 权限运行。请使用 sudo 执行。${NC}"
   exit 1
fi

# 获取 Ubuntu 版本代号
CODENAME=$(lsb_release -cs 2>/dev/null)
if [ -z "$CODENAME" ]; then
    # 备用方法获取版本代号
    CODENAME=$(grep -oP 'VERSION_CODENAME=\K\w+' /etc/os-release 2>/dev/null)
fi

if [ -z "$CODENAME" ]; then
    echo -e "${RED}错误: 无法识别 Ubuntu 版本代号。请手动指定。${NC}"
    exit 1
fi

# 检查是否为支持的版本
SUPPORTED_CODENAMES=("focal" "jammy" "noble")
SUPPORTED=false
for SUPPORTED_CODENAME in "${SUPPORTED_CODENAMES[@]}"; do
    if [ "$CODENAME" = "$SUPPORTED_CODENAME" ]; then
        SUPPORTED=true
        break
    fi
done

if [ "$SUPPORTED" = false ]; then
    echo -e "${YELLOW}警告: 当前 Ubuntu 版本 ($CODENAME) 可能不受完全支持。${NC}"
    echo -e "${YELLOW}继续操作可能会导致软件包无法正常安装。${NC}"
    
    read -p "是否继续? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 源列表文件路径
SOURCE_FILE="/etc/apt/sources.list"
BACKUP_FILE="/etc/apt/sources.list.bak"

# 创建备份
echo -e "${GREEN}正在备份原始源列表...${NC}"
cp "$SOURCE_FILE" "$BACKUP_FILE" || { echo -e "${RED}备份失败！${NC}"; exit 1; }
echo -e "${GREEN}已备份到 $BACKUP_FILE${NC}"

# 生成清华源配置
echo -e "${GREEN}正在生成清华源配置...${NC}"
cat > "$SOURCE_FILE" << EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $CODENAME-proposed main restricted universe multiverse
EOF

echo -e "${GREEN}清华源配置已写入 $SOURCE_FILE${NC}"

# 更新 APT 索引
echo -e "${GREEN}正在更新软件包索引...${NC}"
apt update

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}APT 源已成功替换为清华源！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "${YELLOW}提示: 如需升级已安装的软件包，请运行:${NC}"
echo -e "${YELLOW}sudo apt upgrade${NC}"
echo -e "${GREEN}=========================================${NC}"

exit 0

