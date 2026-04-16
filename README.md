# RPA数据采集+动态看板+AI分析全栈系统

## 系统架构

### 1. 后端服务 (Node.js)
- **功能**：提供RESTful API，连接MySQL数据库，处理数据的增删改查和AI分析请求
- **技术栈**：Node.js, Express, MySQL2
- **API端点**：
  - `GET /api/data` - 获取所有数据
  - `POST /api/data` - 插入数据（供RPA调用）
  - `POST /api/analyze` - 进行AI分析

### 2. 前端应用 (Vue 3)
- **功能**：实现数据看板，包含图表、表格、筛选器，动态展示数据库实时数据
- **技术栈**：Vue 3, Axios, ECharts, Ant Design Vue
- **主要功能**：
  - 数据趋势图表
  - 分类占比图表
  - 数据表格
  - 类别筛选器
  - AI分析功能

### 3. RPA数据采集 (Python)
- **功能**：模拟影刀爬取数据，通过API写入数据库
- **技术栈**：Python, Requests

### 4. AI集成
- **功能**：调用影刀AI Power API，对看板指定板块进行智能洞察分析
- **技术栈**：Node.js, Axios

## 部署指南

### 1. 环境准备
- Node.js 14.0+
- Python 3.7+
- MySQL 5.7+

### 2. 后端部署
1. 克隆项目到本地
2. 安装依赖：`npm install`
3. 配置MySQL数据库连接信息
4. 启动后端服务：`npm start`

### 3. 前端部署
1. 进入frontend目录
2. 安装依赖：`npm install`
3. 构建项目：`npm run build`
4. 将构建产物部署到Web服务器

### 4. RPA部署
1. 安装Python依赖：`pip install requests`
2. 运行RPA脚本：`python rpa_script.py`

### 5. 环境变量配置

#### 后端环境变量
- `DB_HOST` - 数据库主机
- `DB_USER` - 数据库用户名
- `DB_PASSWORD` - 数据库密码
- `DB_NAME` - 数据库名称
- `PORT` - 后端服务端口

#### 前端环境变量
- `VITE_API_BASE_URL` - 后端API基础URL

## 系统功能

1. **数据采集**：RPA脚本通过API将数据写入数据库
2. **数据展示**：前端看板实时展示数据库中的数据，包括图表和表格
3. **数据筛选**：支持按类别筛选数据
4. **AI分析**：对看板数据进行智能洞察分析，提供关键洞察和建议

## 项目结构

```
├── backend/           # 后端代码
│   ├── index.js       # 主入口文件
│   ├── package.json   # 依赖配置
│   └── .env           # 环境变量
├── frontend/          # 前端代码
│   ├── src/           # 源代码
│   ├── public/        # 静态资源
│   ├── package.json   # 依赖配置
│   └── vite.config.js # Vite配置
├── rpa/               # RPA脚本
│   └── rpa_script.py  # 数据采集脚本
└── README.md          # 项目文档
```

## 示例数据

系统启动时会自动生成一些示例数据，包括不同类别的数据项，用于测试和演示系统功能。

## 注意事项

1. 确保MySQL数据库已创建并可访问
2. 确保后端服务和前端应用在同一网络环境中
3. 如需部署到公网，需要配置相应的网络和安全设置
4. 实际使用中，需要替换影刀AI Power API的模拟实现为真实的API调用

## 系统演示

1. 启动后端服务
2. 运行RPA脚本生成数据
3. 访问前端应用查看数据看板
4. 点击"AI分析"按钮查看智能洞察分析结果

## 技术支持

如遇到问题，请参考以下资源：
- Node.js官方文档：https://nodejs.org/en/docs/
- Vue 3官方文档：https://vuejs.org/guide/
- MySQL官方文档：https://dev.mysql.com/doc/
- ECharts官方文档：https://echarts.apache.org/zh/index.html