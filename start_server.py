import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

# AI API配置
AI_API_URL = 'https://power-api.yingdao.com/oapi/power/v1/rest/flow/d3f1235e-9eab-4b17-bd65-6514d4f8b7c7/execute'
AI_API_KEY = os.getenv('AI_API_KEY', 'AP_b3D47FdfG2NEDmRN')

# HTTP请求处理器
class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置CORS头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 处理不同的API端点
        if self.path == '/api/ai-analysis':
            # AI智能分析
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {AI_API_KEY}'
                }
                data = {'input': {}}
                req = urllib.request.Request(AI_API_URL, method='POST')
                for key, value in headers.items():
                    req.add_header(key, value)
                json_data = json.dumps(data).encode('utf-8')
                with urllib.request.urlopen(req, json_data, timeout=30) as response:
                    response_text = response.read().decode('utf-8')
                    response_json = json.loads(response_text)
                    data = response_json
            except Exception as e:
                data = {'error': str(e)}
        elif self.path == '/':
            data = {
                'status': 'healthy',
                'message': 'Simple API Server is running'
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
    print('Press Ctrl+C to stop')
    httpd.serve_forever()

if __name__ == '__main__':
    print('Starting server...')
    run_server(8000)