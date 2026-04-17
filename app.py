from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)

# 从环境变量获取配置
AI_API_URL = os.getenv('AI_API_URL', 'https://power-api.yingdao.com/oapi/power/v1/rest/flow/d3f1235e-9eab-4b17-bd65-6514d4f8b7c7/execute')
AI_API_KEY = os.getenv('AI_API_KEY', 'AP_b3D47FdfG2NEDmRN')

# 健康检查
@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Flask API is running',
        'endpoints': {
            '/api/ai-analysis': 'AI智能分析',
            '/': '健康检查'
        }
    })

# AI 智能分析
@app.route('/api/ai-analysis')
def ai_analysis():
    try:
        import urllib.request
        import json
        
        # 准备请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {AI_API_KEY}'
        }
        
        # 准备请求数据
        data = {'input': {}}
        
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
            return jsonify(response_json)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Vercel 会自动设置 PORT 环境变量
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)