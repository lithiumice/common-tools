#!/bin/bash

# libboost安装脚本
set -euo pipefail

# 日志函数
log() {
    echo -e "\033[1;32m[$(date '+%Y-%m-%d %H:%M:%S')] $1\033[0m"
}

error() {
    echo -e "\033[1;31m[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1\033[0m" >&2
    exit 1
}

# 检查是否为root用户
if [ "$(id -u)" -ne 0 ]; then
    log "请使用root权限运行此脚本，或在命令前添加sudo"
    exit 1
fi

# 定义变量
BOOST_VERSION="1.73.0"
BOOST_DIR="boost_${BOOST_VERSION//./_}"
BOOST_URL="https://boostorg.jfrog.io/artifactory/main/release/${BOOST_VERSION}/source/${BOOST_DIR}.tar.bz2"
INSTALL_PREFIX="/usr/local"
WORK_DIR="/tmp"

# 选项解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            BOOST_VERSION="$2"
            BOOST_DIR="boost_${BOOST_VERSION//./_}"
            BOOST_URL="https://boostorg.jfrog.io/artifactory/main/release/${BOOST_VERSION}/source/${BOOST_DIR}.tar.bz2"
            shift 2
            ;;
        --prefix)
            INSTALL_PREFIX="$2"
            shift 2
            ;;
        --help)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --version VERSION   指定Boost版本 (默认: 1.73.0)"
            echo "  --prefix PATH       指定安装路径 (默认: /usr/local)"
            echo "  --help              显示此帮助信息"
            exit 0
            ;;
        *)
            error "未知选项: $1"
            ;;
    esac
done

# 依赖检查与安装
log "检查并安装必要的依赖..."
if command -v apt-get &>/dev/null; then
    apt-get update -y
    apt-get install -y wget tar bzip2 build-essential
elif command -v yum &>/dev/null; then
    yum update -y
    yum install -y wget tar bzip2 gcc-c++ make
else
    error "不支持的包管理器，请手动安装: wget, tar, bzip2, build-essential"
fi

# 下载Boost
log "下载Boost ${BOOST_VERSION}..."
cd "$WORK_DIR"
if [ ! -f "${BOOST_DIR}.tar.bz2" ]; then
    wget --no-check-certificate "$BOOST_URL" || error "下载失败"
else
    log "使用已存在的下载文件"
fi

# 解压
log "解压Boost源码..."
if [ ! -d "$BOOST_DIR" ]; then
    tar -xjf "${BOOST_DIR}.tar.bz2" || error "解压失败"
fi
cd "$BOOST_DIR"

# 配置
log "配置Boost构建环境..."
./bootstrap.sh --prefix="$INSTALL_PREFIX" || error "配置失败"

# 构建
log "开始构建Boost (这可能需要一段时间)..."
./b2 -j"$(nproc)" --build-type=complete --with=all || error "构建失败"

# 安装
log "安装Boost到 $INSTALL_PREFIX..."
./b2 install || error "安装失败"

# 更新库缓存
log "更新系统库缓存..."
ldconfig || error "更新库缓存失败"

# 验证安装
log "验证Boost安装..."
if [ -f "${INSTALL_PREFIX}/include/boost/version.hpp" ]; then
    log "Boost安装成功!"
    BOOST_LIB_VERSION=$(grep "#define BOOST_VERSION" "${INSTALL_PREFIX}/include/boost/version.hpp" | awk '{print $3}')
    BOOST_MAJOR=$(($BOOST_LIB_VERSION / 100000))
    BOOST_MINOR=$(($BOOST_LIB_VERSION / 100 % 1000))
    BOOST_PATCH=$(($BOOST_LIB_VERSION % 100))
    log "已安装Boost版本: ${BOOST_MAJOR}.${BOOST_MINOR}.${BOOST_PATCH}"
else
    error "Boost安装失败!"
fi

# 输出环境变量配置
log "====================================="
log "Boost安装完成!"
log "为了让您的系统找到Boost库，请确保您的环境变量包含:"
log "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${INSTALL_PREFIX}/lib"
log "您可以将此行添加到您的~/.bashrc或~/.zshrc文件中"
log "====================================="    