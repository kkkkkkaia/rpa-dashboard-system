const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// 数据库连接配置
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'rpa_data'
});

// 连接数据库
db.connect((err) => {
  if (err) {
    console.error('数据库连接失败:', err);
    return;
  }
  console.log('数据库连接成功');
  
  // 创建数据表
  const createTableQuery = `
    CREATE TABLE IF NOT EXISTS rpa_data (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      value INT NOT NULL,
      category VARCHAR(100) NOT NULL,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  
  db.query(createTableQuery, (err) => {
    if (err) {
      console.error('创建数据表失败:', err);
    } else {
      console.log('数据表创建成功');
    }
  });
});

// 中间件
app.use(cors());
app.use(bodyParser.json());

// API路由

// 获取所有数据
app.get('/api/data', (req, res) => {
  const query = 'SELECT * FROM rpa_data ORDER BY timestamp DESC';
  db.query(query, (err, results) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(results);
  });
});

// 按类别获取数据
app.get('/api/data/:category', (req, res) => {
  const { category } = req.params;
  const query = 'SELECT * FROM rpa_data WHERE category = ? ORDER BY timestamp DESC';
  db.query(query, [category], (err, results) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(results);
  });
});

// 插入数据（供RPA调用）
app.post('/api/data', (req, res) => {
  const { name, value, category } = req.body;
  const query = 'INSERT INTO rpa_data (name, value, category) VALUES (?, ?, ?)';
  db.query(query, [name, value, category], (err, results) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ id: results.insertId, name, value, category, timestamp: new Date() });
  });
});

// AI分析API
app.post('/api/analyze', (req, res) => {
  const { data } = req.body;
  
  // 模拟调用影刀AI Power API
  // 实际项目中需要替换为真实的API调用
  const analysisResult = {
    summary: '数据整体呈现上升趋势',
    insights: [
      '类别A占比最高，建议重点关注',
      '最近7天数据增长明显',
      '周末数据活跃度较低'
    ],
    recommendations: [
      '增加类别A的监控频率',
      '优化周末数据采集策略',
      '关注数据异常波动'
    ]
  };
  
  res.json(analysisResult);
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});