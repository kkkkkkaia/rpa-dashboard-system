# GitHub上传指南

## 方法一：使用命令行（推荐）

### 1. 在GitHub创建新仓库
1. 访问 https://github.com/new
2. 填写仓库名称：`rpa-dashboard-system`
3. 选择Private或Public
4. 点击"Create repository"

### 2. 初始化本地Git仓库
打开终端，进入项目目录，执行以下命令：

```bash
# 进入项目目录
cd "d:\kaia\OneDrive\桌面\test"

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交文件
git commit -m "Initial commit: RPA数据采集+动态看板+AI分析全栈系统"

# 添加远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/rpa-dashboard-system.git

# 推送到GitHub
git push -u origin main
```

### 3. 首次推送需要认证
如果是首次推送GitHub，可能需要输入GitHub用户名和Personal Access Token。

## 方法二：使用GitHub Desktop

### 1. 下载GitHub Desktop
访问 https://desktop.github.com/ 下载安装

### 2. 添加仓库
1. 打开GitHub Desktop
2. 点击 "File" -> "Add Local Repository"
3. 选择项目目录 `d:\kaia\OneDrive\桌面\test`
4. 点击 "Publish repository" 推送到GitHub

## 方法三：使用VS Code

### 1. 安装Git插件
在VS Code中安装"Git"插件

### 2. 初始化仓库
1. 打开项目目录
2. 点击左侧源代码管理图标
3. 点击"初始化仓库"
4. 添加提交消息并提交
5. 点击"发布分支"推送到GitHub

## 自动脚本

如果你想自动化执行，可以运行项目中的 `deploy_github.sh` 脚本：

```bash
bash deploy_github.sh
```

## 文件结构

上传到GitHub的文件结构：

```
rpa-dashboard-system/
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── api.js
├── index.js
├── package.json
├── rpa_script.py
├── server.js
└── README.md
```

## 注意事项

1. **不要上传node_modules目录**：确保有 `.gitignore` 文件
2. **敏感信息**：不要将数据库密码、API密钥等敏感信息提交到GitHub
3. **Large Files**：如果文件过大，考虑使用Git LFS

## 创建.gitignore文件

```gitignore
# Node modules
node_modules/

# Environment variables
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Build output
dist/
build/
```

## 常见问题

### Q: git命令找不到？
A: 确保已安装Git并添加到系统PATH环境变量

### Q: 推送被拒绝？
A: 可能仓库已存在，先git pull或使用-f强制推送

### Q: 需要认证？
A: 使用Personal Access Token代替密码
