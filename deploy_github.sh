#!/bin/bash
# GitHub上传脚本

# 配置GitHub仓库信息
REPO_URL="https://github.com/USERNAME/REPO_NAME.git"
BRANCH="main"

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交文件
git commit -m "Initial commit: RPA数据采集+动态看板+AI分析全栈系统"

# 添加远程仓库
git remote add origin $REPO_URL

# 推送到GitHub
git push -u origin $BRANCH