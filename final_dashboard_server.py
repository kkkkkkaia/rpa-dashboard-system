import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timedelta
import re
import urllib.request

# 数据库配置
DATABASE_URL = 'postgresql://postgres.kxpvyzokzwruustynjrk:Yixiaoyu_2003@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres'

# AI API配置
AI_API_URL = 'https://power-api.yingdao.com/oapi/power/v1/rest/flow/d3f1235e-9eab-4b17-bd65-6514d4f8b7c7/execute'
AI_API_KEY = os.getenv('AI_API_KEY', 'AP_b3D47FdfG2NEDmRN')

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=False)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 定义数据模型
class DataModel(Base):
    __tablename__ = 'data_table'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text)
    post_id = Column(String(50))
    author = Column(String(100))
    content = Column(Text)
    published_at = Column(DateTime)
    views = Column(Integer)
    analysis = Column(Text)

# 情感分析函数
def analyze_sentiment(text):
    if not text:
        return '中性'
    
    negative_words = ['报错', '失败', '无法', '不工作', '错误', '问题', '崩溃', '卡', '慢', '困难', '不行']
    positive_words = ['成功', '好', '完美', '解决', '有效', '快速', '方便', '好用', '赞', '优秀']
    
    text_lower = text.lower()
    negative_count = sum(1 for word in negative_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    if negative_count > positive_count:
        return '消极'
    elif positive_count > negative_count:
        return '积极'
    else:
        return '中性'

# 问题类型分类函数
def categorize_question(title, content):
    text = f"{title or ''} {content or ''}".lower()
    
    categories = {
        '浏览器兼容': ['浏览器', 'chrome', 'firefox', 'edge', 'ie'],
        '元素定位': ['元素', '定位', '捕获', 'xpath', 'selector'],
        '数据采集': ['抓取', '采集', '数据', '爬取', 'scrap'],
        '循环逻辑': ['循环', 'loop', 'for', 'while'],
        'Excel操作': ['excel', '表格', 'wps'],
        'AI应用': ['ai', '智能', '机器学习'],
        '产品咨询': ['咨询', '如何', '怎么', '教程', '使用'],
        '第三方集成': ['集成', '接口', 'api', '第三方']
    }
    
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return '其他'

# 核心指标查询
def get_core_metrics():
    db = SessionLocal()
    try:
        # 总发帖量
        total_posts = db.query(func.count(DataModel.id)).scalar() or 0
        
        # 总浏览量
        total_views = db.query(func.sum(DataModel.views)).scalar() or 0
        
        # 篇均浏览量
        avg_views = total_views / total_posts if total_posts > 0 else 0
        
        # 消极情绪占比
        negative_count = 0
        total_with_content = 0
        
        posts = db.query(DataModel.title, DataModel.content).all()
        for title, content in posts:
            text = f"{title or ''} {content or ''}"
            if text.strip():
                total_with_content += 1
                if analyze_sentiment(text) == '消极':
                    negative_count += 1
        
        negative_ratio = (negative_count / total_with_content * 100) if total_with_content > 0 else 0
        
        return {
            'total_posts': total_posts,
            'total_views': int(total_views),
            'avg_views': round(avg_views, 2),
            'negative_ratio': round(negative_ratio, 2)
        }
    finally:
        db.close()

# 发帖趋势查询
def get_post_trends():
    db = SessionLocal()
    try:
        # 最近30天
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # 按日期分组统计
        daily_data = db.query(
            func.date(DataModel.published_at).label('date'),
            func.count(DataModel.id).label('post_count'),
            func.sum(DataModel.views).label('view_count')
        ).filter(
            DataModel.published_at >= thirty_days_ago
        ).group_by(
            func.date(DataModel.published_at)
        ).order_by(
            func.date(DataModel.published_at)
        ).all()
        
        # 构建结果
        trends = []
        for date, post_count, view_count in daily_data:
            trends.append({
                'date': date.strftime('%Y-%m-%d'),
                'post_count': post_count,
                'view_count': view_count or 0
            })
        
        return trends
    finally:
        db.close()

# 问题类型分布查询
def get_category_distribution():
    db = SessionLocal()
    try:
        posts = db.query(DataModel.title, DataModel.content).all()
        
        # 统计各类别数量
        category_counts = {}
        for title, content in posts:
            category = categorize_question(title, content)
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # 计算占比
        total = len(posts)
        distribution = []
        for category, count in category_counts.items():
            distribution.append({
                'category': category,
                'count': count,
                'percentage': round((count / total * 100), 2) if total > 0 else 0
            })
        
        return distribution
    finally:
        db.close()

# 情感分布查询
def get_sentiment_distribution():
    db = SessionLocal()
    try:
        posts = db.query(DataModel.title, DataModel.content).all()
        
        # 统计情感分布
        sentiment_counts = {'积极': 0, '中性': 0, '消极': 0}
        for title, content in posts:
            text = f"{title or ''} {content or ''}"
            sentiment = analyze_sentiment(text)
            sentiment_counts[sentiment] += 1
        
        # 计算占比
        total = len(posts)
        distribution = []
        for sentiment, count in sentiment_counts.items():
            distribution.append({
                'sentiment': sentiment,
                'count': count,
                'percentage': round((count / total * 100), 2) if total > 0 else 0
            })
        
        return distribution
    finally:
        db.close()

# 交叉分析查询
def get_cross_analysis():
    db = SessionLocal()
    try:
        posts = db.query(DataModel.title, DataModel.content).all()
        
        # 统计各类型下的情感分布
        cross_data = {}
        for title, content in posts:
            category = categorize_question(title, content)
            sentiment = analyze_sentiment(f"{title or ''} {content or ''}")
            
            if category not in cross_data:
                cross_data[category] = {'积极': 0, '中性': 0, '消极': 0}
            cross_data[category][sentiment] += 1
        
        # 构建结果
        analysis = []
        for category, sentiments in cross_data.items():
            analysis.append({
                'category': category,
                'positive': sentiments['积极'],
                'neutral': sentiments['中性'],
                'negative': sentiments['消极']
            })
        
        return analysis
    finally:
        db.close()

# 核心贡献者查询
def get_core_contributors():
    db = SessionLocal()
    try:
        # 统计作者发帖量和累计浏览量
        contributors = db.query(
            DataModel.author,
            func.count(DataModel.id).label('post_count'),
            func.sum(DataModel.views).label('total_views')
        ).group_by(
            DataModel.author
        ).order_by(
            func.count(DataModel.id).desc()
        ).limit(10).all()
        
        # 构建结果
        result = []
        for author, post_count, total_views in contributors:
            if author:
                result.append({
                    'author': author,
                    'post_count': post_count,
                    'total_views': total_views or 0
                })
        
        return result
    finally:
        db.close()

# 热度追踪查询
def get_hot_posts():
    db = SessionLocal()
    try:
        # 查询浏览量前10的帖子
        hot_posts = db.query(
            DataModel.title,
            DataModel.author,
            DataModel.published_at,
            DataModel.views,
            DataModel.link,
            DataModel.content
        ).order_by(
            DataModel.views.desc()
        ).limit(10).all()
        
        # 构建结果
        result = []
        for title, author, published_at, views, link, content in hot_posts:
            result.append({
                'title': title,
                'author': author,
                'published_at': published_at.isoformat() if published_at else None,
                'views': views or 0,
                'link': link,
                'category': categorize_question(title, content),
                'sentiment': analyze_sentiment(f"{title or ''} {content or ''}")
            })
        
        return result
    finally:
        db.close()

# AI智能分析
def get_ai_analysis():
    try:
        # 准备请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {AI_API_KEY}'
        }
        
        # 准备请求数据
        data = {
            'input': {}
        }
        
        # 构建请求
        req = urllib.request.Request(AI_API_URL, method='POST')
        
        # 添加请求头
        for key, value in headers.items():
            req.add_header(key, value)
        
        # 发送请求
        json_data = json.dumps(data).encode('utf-8')
        with urllib.request.urlopen(req, json_data, timeout=30) as response:
            response_text = response.read().decode('utf-8')
            response_json = json.loads(response_text)
            return response_json
    except Exception as e:
        return {'error': str(e)}

# HTTP请求处理器
class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置CORS头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 处理不同的API端点
        if self.path == '/api/metrics':
            data = get_core_metrics()
        elif self.path == '/api/trends':
            data = get_post_trends()
        elif self.path == '/api/categories':
            data = get_category_distribution()
        elif self.path == '/api/sentiment':
            data = get_sentiment_distribution()
        elif self.path == '/api/cross-analysis':
            data = get_cross_analysis()
        elif self.path == '/api/contributors':
            data = get_core_contributors()
        elif self.path == '/api/hot-posts':
            data = get_hot_posts()
        elif self.path == '/api/ai-analysis':
            data = get_ai_analysis()
        elif self.path == '/':
            data = {
                'status': 'healthy',
                'endpoints': {
                    '/api/metrics': '核心指标',
                    '/api/trends': '发帖趋势',
                    '/api/categories': '问题类型分布',
                    '/api/sentiment': '情感分布',
                    '/api/cross-analysis': '交叉分析',
                    '/api/contributors': '核心贡献者',
                    '/api/hot-posts': '热度追踪',
                    '/api/ai-analysis': 'AI智能分析'
                }
            }
        else:
            data = {'error': 'Endpoint not found'}
        
        # 发送响应
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

# 启动服务器
def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'Server running on http://localhost:{port}')
    print('Available endpoints:')
    print('  GET /api/metrics         - 核心指标')
    print('  GET /api/trends          - 发帖趋势')
    print('  GET /api/categories      - 问题类型分布')
    print('  GET /api/sentiment       - 情感分布')
    print('  GET /api/cross-analysis  - 交叉分析')
    print('  GET /api/contributors    - 核心贡献者')
    print('  GET /api/hot-posts       - 热度追踪')
    print('  GET /api/ai-analysis     - AI智能分析')
    print('  GET /                    - 健康检查')
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')

if __name__ == '__main__':
    print('Starting dashboard server...')
    try:
        run_server(8000)
    except Exception as e:
        print(f'Error starting server: {e}')
        import traceback
        traceback.print_exc()