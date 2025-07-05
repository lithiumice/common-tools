#!/bin/bash

# Ubuntu软件自动安装脚本
# 基于文档内容，支持选择性安装不同类别的软件，安装后可继续选择其他软件

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # 无颜色

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

# 检查命令执行状态
check_status() {
    if [ $? -ne 0 ]; then
        log_error "$1 失败"
        return 1
    else
        log_info "$1 成功"
        return 0
    fi
}

# 更新系统
update_system() {
    log_info "开始更新系统..."
    sudo apt update && sudo apt upgrade -y
    if ! check_status "系统更新"; then return 1; fi
    sudo apt autoremove -y
    if ! check_status "自动移除无用包"; then return 1; fi
    return 0
}

# 安装基本工具
install_base_tools() {
    log_info "开始安装基本工具..."
    sudo apt install -y build-essential curl wget git vim nano htop unzip zip tar screen tmux software-properties-common apt-transport-https ca-certificates lsb-release
    if ! check_status "基本工具安装"; then return 1; fi
    return 0
}

# 安装开发工具
install_dev_tools() {
    log_info "开始安装开发工具..."
    sudo apt install -y gcc g++ make cmake gdb clang \
        python3 python3-pip python3-venv openjdk-11-jdk
    if ! check_status "开发工具安装"; then return 1; fi
    return 0
}

# 安装版本控制工具
install_version_control() {
    log_info "开始安装版本控制工具..."
    sudo apt install -y git git-lfs
    if ! check_status "版本控制工具安装"; then return 1; fi
    return 0
}

# 安装网络工具
install_network_tools() {
    log_info "开始安装网络工具..."
    sudo apt install -y net-tools nmap traceroute telnet dnsutils curl wget
    if ! check_status "网络工具安装"; then return 1; fi
    return 0
}

# 安装数据库
install_databases() {
    log_info "开始安装数据库..."
    echo "请选择要安装的数据库（可多选，用空格分隔）："
    echo "1) MySQL"
    echo "2) PostgreSQL"
    echo "3) SQLite"
    echo "q) 取消"
    read -p "输入选项: " db_choice
    
    case $db_choice in
        *1* ) 
            log_info "安装MySQL..."
            sudo apt install -y mysql-server mysql-client
            if ! check_status "MySQL安装"; then return 1; fi
            ;;
        *2* ) 
            log_info "安装PostgreSQL..."
            sudo apt install -y postgresql postgresql-contrib
            if ! check_status "PostgreSQL安装"; then return 1; fi
            ;;
        *3* ) 
            log_info "安装SQLite..."
            sudo apt install -y sqlite3
            if ! check_status "SQLite安装"; then return 1; fi
            ;;
        q ) 
            log_info "取消数据库安装"
            return 0
            ;;
        * ) 
            log_error "无效选项"
            return 1
            ;;
    esac
    return 0
}

# 安装常用软件
install_common_software() {
    log_info "开始安装常用软件..."
    sudo apt install -y firefox gnome-tweaks vlc gimp libreoffice
    if ! check_status "常用软件安装"; then return 1; fi
    return 0
}

# 安装Docker
install_docker() {
    log_info "开始安装Docker和容器工具..."
    sudo apt install -y docker.io docker-compose
    if ! check_status "Docker安装"; then return 1; fi
    sudo usermod -aG docker $USER
    log_info "已将当前用户添加到docker组，请重新登录使设置生效"
    return 0
}

# 安装Node.js
install_nodejs() {
    log_info "开始安装Node.js和npm..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
    if ! check_status "Node.js安装"; then return 1; fi
    sudo npm install -g yarn
    if ! check_status "Yarn安装"; then return 1; fi
    return 0
}

# 安装IDE和编辑器
install_ides() {
    log_info "开始安装IDE和编辑器..."
    echo "请选择要安装的IDE/编辑器（可多选，用空格分隔）："
    echo "1) Visual Studio Code"
    echo "2) IntelliJ IDEA Community Edition"
    echo "q) 取消"
    read -p "输入选项: " ide_choice
    
    case $ide_choice in
        *1* ) 
            log_info "安装Visual Studio Code..."
            wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
            sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
            sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
            sudo apt update
            sudo apt install -y code
            if ! check_status "Visual Studio Code安装"; then return 1; fi
            ;;
        *2* ) 
            log_info "安装IntelliJ IDEA Community Edition..."
            sudo snap install intellij-idea-community --classic
            if ! check_status "IntelliJ IDEA安装"; then return 1; fi
            ;;
        q ) 
            log_info "取消IDE/编辑器安装"
            return 0
            ;;
        * ) 
            log_error "无效选项"
            return 1
            ;;
    esac
    return 0
}

# 安装科学计算和机器学习工具
install_ml_tools() {
    log_info "开始安装科学计算和机器学习工具..."
    sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pandas python3-sklearn
    if ! check_status "科学计算工具安装"; then return 1; fi
    pip install tensorflow keras jupyterlab
    if ! check_status "机器学习工具安装"; then return 1; fi
    return 0
}

# 安装多媒体工具
install_multimedia() {
    log_info "开始安装多媒体工具..."
    sudo apt install -y ubuntu-restricted-extras ffmpeg
    if ! check_status "多媒体工具安装"; then return 1; fi
    return 0
}

# 安装Qt和图形开发工具
install_qt() {
    log_info "开始安装Qt和图形开发工具..."
    sudo apt install -y qtcreator qt5-default
    if ! check_status "Qt和图形开发工具安装"; then return 1; fi
    return 0
}

# 安装Papirus图标主题
install_icon_theme() {
    sudo add-apt-repository ppa:varlesh-l/papirus-pack
    sudo apt-get update
    sudo apt-get install papirus-gtk-icon-theme

    sudo add-apt-repository ppa:varlesh-l/papirus-pack
    sudo apt-get update
    sudo apt-get install papirus-pack-kde5
}



# 安装其他软件
install_other_software() {
    log_info "开始安装其他软件..."
    echo "请选择要安装的其他软件（可多选，用空格分隔）："
    echo "1) Go语言环境"
    echo "2) Rust语言环境"
    echo "q) 取消"
    read -p "输入选项: " other_choice
    
    case $other_choice in
        *1* ) 
            log_info "安装Go语言环境..."
            sudo apt install -y golang
            if ! check_status "Go语言环境安装"; then return 1; fi
            ;;
        *2* ) 
            log_info "安装Rust语言环境..."
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
            log_info "Rust语言环境安装脚本已运行，请按照提示完成安装"
            ;;
        q ) 
            log_info "取消其他软件安装"
            return 0
            ;;
        * ) 
            log_error "无效选项"
            return 1
            ;;
    esac
    return 0
}

# 清理系统
cleanup_system() {
    log_info "开始清理系统..."
    sudo apt autoremove -y && sudo apt autoclean
    if ! check_status "系统清理"; then return 1; fi
    return 0
}

# 显示软件类别菜单
show_menu() {
    echo "请选择要安装的软件类别（输入编号，q退出）："
    echo "1) 更新系统"
    echo "2) 基本工具"
    echo "3) 开发工具"
    echo "4) 版本控制工具"
    echo "5) 网络工具"
    echo "6) 数据库"
    echo "7) 常用软件"
    echo "8) Docker和容器工具"
    echo "9) Node.js和npm"
    echo "10) IDE和编辑器"
    echo "11) 科学计算和机器学习工具"
    echo "12) 多媒体工具"
    echo "13) Qt和图形开发工具"
    echo "14) 其他软件"
    echo "c) 清理系统"
    echo "q) 退出"
}

# 获取用户选择并执行安装
get_and_execute_choice() {
    show_menu
    read -p "输入选项: " choice
    
    case $choice in
        1) update_system ;;
        2) install_base_tools ;;
        3) install_dev_tools ;;
        4) install_version_control ;;
        5) install_network_tools ;;
        6) install_databases ;;
        7) install_common_software ;;
        8) install_docker ;;
        9) install_nodejs ;;
        10) install_ides ;;
        11) install_ml_tools ;;
        12) install_multimedia ;;
        13) install_qt ;;
        14) install_other_software ;;
        c|C) cleanup_system ;;
        q|Q) return 1 ;;
        *) log_error "无效选项，请重新输入" ;;
    esac
    
    return 0
}

# 主函数
main() {
    echo "====================================="
    echo "      Ubuntu软件自动安装脚本       "
    echo "====================================="
    
    # 确认用户权限
    if [ "$(id -u)" -ne 0 ]; then
        log_warn "此脚本需要root权限执行，将使用sudo命令"
    fi
    
    # 循环让用户选择安装
    while true; do
        get_and_execute_choice
        if [ $? -eq 1 ]; then
            break
        fi
        
        echo
        read -p "是否继续安装其他软件？(y/n): " continue_choice
        case $continue_choice in
            n|N) break ;;
            y|Y) ;;
            *) log_error "无效选项，默认继续" ;;
        esac
        echo
    done
    
    log_info "脚本执行完成！"
}

# 执行主函数
main    
