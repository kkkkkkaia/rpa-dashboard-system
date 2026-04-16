const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

// 模拟数据库
let db = [];
let id = 1;

// 处理请求
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  
  // 设置CORS头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // 处理OPTIONS请求
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }
  
  // 处理GET请求
  if (req.method === 'GET' && pathname === '/api/data') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(db));
    return;
  }
  
  // 处理POST请求
  if (req.method === 'POST' && pathname === '/api/data') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      const data = JSON.parse(body);
      const newData = {
        id: id++,
        name: data.name,
        value: data.value,
        category: data.category,
        timestamp: new Date().toISOString()
      };
      db.push(newData);
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(newData));
    });
    return;
  }
  
  // 处理AI分析请求
  if (req.method === 'POST' && pathname === '/api/analyze') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
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
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(analysisResult));
    });
    return;
  }
  
  // 处理根路径
  if (req.method === 'GET' && pathname === '/') {
    const filePath = path.join(__dirname, 'frontend', 'index.html');
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.statusCode = 404;
        res.end('File not found');
        return;
      }
      res.setHeader('Content-Type', 'text/html');
      res.statusCode = 200;
      res.end(content);
    });
    return;
  }
  
  // 处理前端静态文件
  if (req.method === 'GET' && (pathname.startsWith('/frontend/') || pathname.endsWith('.js') || pathname.endsWith('.css') || pathname.endsWith('.html'))) {
    let filePath;
    if (pathname.startsWith('/frontend/')) {
      filePath = path.join(__dirname, pathname);
    } else {
      filePath = path.join(__dirname, 'frontend', pathname);
    }
    
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.statusCode = 404;
        res.end('File not found');
        return;
      }
      
      // 设置内容类型
      if (filePath.endsWith('.html')) {
        res.setHeader('Content-Type', 'text/html');
      } else if (filePath.endsWith('.js')) {
        res.setHeader('Content-Type', 'application/javascript');
      } else if (filePath.endsWith('.css')) {
        res.setHeader('Content-Type', 'text/css');
      }
      
      res.statusCode = 200;
      res.end(content);
    });
    return;
  }
  

  
  // 处理其他请求
  res.statusCode = 404;
  res.end('Not found');
});

// 启动服务器
const port = 8080;
server.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
  console.log('模拟数据库已初始化');
  
  // 生成一些初始数据
  const categories = ['类别A', '类别B', '类别C', '类别D'];
  const names = ['数据项1', '数据项2', '数据项3', '数据项4', '数据项5'];
  
  for (let i = 0; i < 10; i++) {
    db.push({
      id: id++,
      name: names[Math.floor(Math.random() * names.length)],
      value: Math.floor(Math.random() * 90) + 10,
      category: categories[Math.floor(Math.random() * categories.length)],
      timestamp: new Date().toISOString()
    });
  }
  
  console.log('已生成初始数据');
  console.log('服务器启动成功，等待请求...');
});