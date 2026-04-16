# GitHub上传指南

## 前提条件
1. 已安装Git
2. 已有GitHub账号：kkkkkkaia
3. 已有仓库：RPA-dashboard-system

## 上传步骤

### 1. 打开Git Bash（不是PowerShell）

### 2. 进入项目目录
```bash
cd "d:/kaia/OneDrive/桌面/test"
```

### 3. 初始化Git仓库（如果还没有初始化）
```bash
git init
```

### 4. 配置Git用户信息（如果还没有配置）
```bash
git config user.name "kkkkkkaia"
git config user.email "your-email@example.com"
```

### 5. 添加所有文件到暂存区
```bash
git add .
```

### 6. 提交文件
```bash
git commit -m "Initial commit: RPA数据采集+动态看板+AI分析全栈系统"
```

### 7. 添加远程仓库
```bash
git remote add origin https://github.com/kkkkkkaia/RPA-dashboard-system.git
```

### 8. 推送到GitHub
```bash
git push -u origin master
```

## 如果仓库已经有内容

### 1. 先克隆仓库
```bash
git clone https://github.com/kkkkkkaia/RPA-dashboard-system.git
cd RPA-dashboard-system
```

### 2. 复制项目文件到仓库目录
将test目录下的所有文件复制到RPA-dashboard-system目录

### 3. 提交并推送
```bash
git add .
git commit -m "Add RPA dashboard system"
git push -u origin master
```

## 注意事项
- 确保有网络连接
- 可能需要输入GitHub用户名和密码（或Personal Access Token）
- 如果使用2FA，需要使用Personal Access Token作为密码