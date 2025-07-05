#!/bin/bash

# CUDA自动安装脚本
# 支持多种CUDA版本选择，自动处理依赖和环境配置

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "请使用root权限运行此脚本"
        exit 1
    fi
}

# 检查网络连接
check_network() {
    log_info "检查网络连接..."
    ping -c 3 developer.download.nvidia.com > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        log_error "无法连接到NVIDIA服务器，请检查网络连接"
        exit 1
    fi
    log_info "网络连接正常"
}

# 选择CUDA版本
select_cuda_version() {
    echo "请选择要安装的CUDA版本:"
    echo "1) CUDA 11.7.0 (推荐)"
    echo "2) CUDA 11.4.0"
    echo "3) CUDA 11.2.0"
    echo "4) CUDA 10.2.89"
    
    read -p "输入选项 [1-4]: " choice
    
    case $choice in
        1) 
            CUDA_VERSION="11.7.0"
            DRIVER_VERSION="515.43.04"
            ;;
        2) 
            CUDA_VERSION="11.4.0"
            DRIVER_VERSION="470.42.01"
            ;;
        3) 
            CUDA_VERSION="11.2.0"
            DRIVER_VERSION="460.27.04"
            ;;
        4) 
            CUDA_VERSION="10.2.89"
            DRIVER_VERSION="440.33.01"
            ;;
        *) 
            log_error "无效的选项"
            exit 1
            ;;
    esac
    
    log_info "已选择CUDA $CUDA_VERSION，需要NVIDIA驱动版本 $DRIVER_VERSION"
}

# 安装前准备
pre_install() {
    log_info "正在进行安装前准备..."
    
    # 安装必要的依赖
    apt-get update > /dev/null 2>&1
    apt-get install -y wget build-essential > /dev/null 2>&1
    
    # 禁用nouveau驱动
    if [ ! -f /etc/modprobe.d/blacklist-nouveau.conf ]; then
        log_info "禁用nouveau驱动..."
        echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
        echo "options nouveau modeset=0" >> /etc/modprobe.d/blacklist-nouveau.conf
        update-initramfs -u > /dev/null 2>&1
        log_warn "禁用nouveau驱动后需要重启系统，安装完成后请重启"
    fi
    
    # 创建临时目录
    TEMP_DIR=$(mktemp -d)
    cd $TEMP_DIR
}

# 下载CUDA安装文件
download_cuda() {
    log_info "开始下载CUDA $CUDA_VERSION安装文件..."
    
    # 构建下载URL
    if [[ $CUDA_VERSION == 10.2.89 ]]; then
        BASE_URL="https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers"
    else
        VERSION_MAJOR_MINOR=$(echo $CUDA_VERSION | cut -d. -f1-2)
        BASE_URL="https://developer.download.nvidia.com/compute/cuda/$VERSION_MAJOR_MINOR.0/local_installers"
    fi
    
    FILENAME="cuda_${CUDA_VERSION}_${DRIVER_VERSION}_linux.run"
    URL="$BASE_URL/$FILENAME"
    
    # 下载文件
    wget -q $URL
    if [ $? -ne 0 ]; then
        log_error "下载失败: $URL"
        exit 1
    fi
    
    log_info "下载完成: $FILENAME"
}

# 安装CUDA和驱动
install_cuda() {
    log_info "开始安装CUDA $CUDA_VERSION和NVIDIA驱动..."
    
    FILENAME="cuda_${CUDA_VERSION}_${DRIVER_VERSION}_linux.run"
    
    # 执行安装
    sh $FILENAME --silent --driver --toolkit --samples > /dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        log_error "安装过程中发生错误，请查看/var/log/cuda-installer.log获取详细信息"
        exit 1
    fi
    
    log_info "CUDA $CUDA_VERSION和NVIDIA驱动安装成功"
}

# 配置环境变量
configure_environment() {
    log_info "配置CUDA环境变量..."
    
    # 获取CUDA安装路径
    CUDA_PATH="/usr/local/cuda-$CUDA_VERSION"
    
    # 添加到PATH
    if ! grep -q "$CUDA_PATH/bin" /etc/profile; then
        echo "export PATH=$CUDA_PATH/bin:$PATH" >> /etc/profile
    fi
    
    # 添加到LD_LIBRARY_PATH
    if ! grep -q "$CUDA_PATH/lib64" /etc/ld.so.conf; then
        echo "$CUDA_PATH/lib64" >> /etc/ld.so.conf
        ldconfig
    fi
    
    log_info "CUDA环境变量配置完成"
}

# 验证安装
verify_installation() {
    log_info "验证CUDA安装..."
    
    # 检查nvcc版本
    nvcc --version > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        log_warn "nvcc命令不可用，可能需要重启系统或重新加载环境变量"
    else
        log_info "CUDA安装验证通过"
    fi
    
    # 检查nvidia-smi
    nvidia-smi > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        log_warn "nvidia-smi命令不可用，驱动可能未正确安装"
    else
        log_info "NVIDIA驱动验证通过"
    fi
}

# 清理
cleanup() {
    log_info "清理临时文件..."
    cd /tmp
    rm -rf $TEMP_DIR
    log_info "清理完成"
}

# 主函数
main() {
    check_root
    check_network
    select_cuda_version
    pre_install
    download_cuda
    install_cuda
    configure_environment
    verify_installation
    cleanup
    
    log_info "======================================"
    log_info "CUDA $CUDA_VERSION和NVIDIA驱动安装完成"
    log_info "请重启系统使配置生效"
    log_info "======================================"
}

# 执行主函数
main    