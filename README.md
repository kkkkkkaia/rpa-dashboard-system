# 数据分析看板

基于 Flask 和 PostgreSQL 的数据分析看板，支持数据库查询、AI 智能分析等功能。

## 📁 项目文件

- `dashboard.html` - 前端看板页面
- `start_server.py` - AI API 服务
- `final_dashboard_server.py` - 数据库查询服务（完整版）
- `config.py` - 数据库配置文件

## 🚀 启动方式

### 1. 启动 AI API 服务（端口 8000）

```bash
python start_server.py
```

服务地址：`http://localhost:8000`

### 2. 启动前端服务（端口 3000）

```bash
python -m http.server 3000
```

服务地址：`http://localhost:3000`

## 🌐 访问方式

### 方式一：直接打开文件
在浏览器中直接打开 `dashboard.html` 文件

### 方式二：通过 HTTP 服务访问
启动前端服务后，在浏览器访问：
```
http://localhost:3000/dashboard.html
```

## 📊 功能模块

### 1. 核心指标
- 总发帖量
- 总浏览量
- 篇均浏览量
- 消极情绪占比

### 2. 发帖趋势
- 最近 30 天每天的帖子数量
- 最近 30 天每天的浏览量
- 趋势折线图展示

### 3. 问题类型分布
- 浏览器兼容
- 元素定位
- 数据采集
- 循环逻辑
- Excel 操作
- AI 应用
- 产品咨询
- 第三方集成

### 4. 情感分布
- 积极帖子数量和占比
- 中性帖子数量和占比
- 消极帖子数量和占比

### 5. 交叉分析
- 按问题类型分组
- 统计每种类型下的积极、中性、消极数量

### 6. 核心贡献者
- 发帖量前 10 的作者
- 累计浏览量

### 7. 热度追踪
- 浏览量前 10 的帖子
- 显示标题、作者、发布时间、问题类型、情感、浏览量、链接

### 8. AI 智能分析
点击"发帖趋势"卡片中的"智能分析"按钮，系统会：
- 调用 AI API 获取分析数据
- 解析 CSV 格式的分析结果
- 生成详细的文字分析报告

## 🔧 数据库配置

数据库配置文件：`config.py`

```python
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://用户名:密码@主机:端口/数据库名'
)
```

## 🔑 API 配置

AI API 配置文件：`start_server.py`

```python
AI_API_URL = 'https://power-api.yingdao.com/oapi/power/v1/rest/flow/d3f1235e-9eab-4b17-bd65-6514d4f8b7c7/execute'
AI_API_KEY = os.getenv('AI_API_KEY', 'AP_b3D47FdfG2NEDmRN')
```

## 📝 使用说明

1. 修改 `config.py` 中的数据库连接配置
2. 启动 AI API 服务：`python start_server.py`
3. 启动前端服务：`python -m http.server 3000`
4. 在浏览器中打开 `dashboard.html`
5. 点击"刷新数据"按钮加载数据库数据
6. 点击"智能分析"按钮获取 AI 分析结果

## 🎨 技术栈

- **前端**：HTML5 + CSS3 + JavaScript
- **图表库**：Chart.js
- **UI 框架**：Bootstrap 5.3
- **后端**：Python HTTP Server
- **数据库**：PostgreSQL (Supabase)
- **ORM**：SQLAlchemy 1.4.46

## ⚠️ 注意事项

- 确保数据库连接配置正确
- 确保 AI API Key 有效
- 建议使用 Chrome、Firefox、Edge 等现代浏览器访问