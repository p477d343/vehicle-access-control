#!/bin/bash

# 函數：將12位數字轉換為標準MAC地址格式
format_mac() {
    echo "$1" | sed 's/.\{2\}/&:/g' | sed 's/:$//'
}

# 檢查是否提供了MAC地址參數
if [ $# -eq 0 ]; then
    echo "錯誤：請提供新的MAC地址作為參數（12位數字，不帶冒號）"
    echo "用法：$0 <新MAC地址>"
    echo "例如：$0 001122334455"
    exit 1
fi

# 獲取作為參數傳入的新MAC地址
new_mac=$1

# 檢查輸入是否為12位數字
if ! [[ $new_mac =~ ^[0-9A-Fa-f]{12}$ ]]; then
    echo "錯誤：MAC地址必須是12位十六進制數字"
    exit 1
fi

# 格式化MAC地址
formatted_mac=$(format_mac $new_mac)

# 執行命令
sudo ip link set dev eth0 down
sudo ip link set dev eth0 address $formatted_mac
sudo ip link set dev eth0 up

echo "MAC地址已更改為: $formatted_mac"
