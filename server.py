from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import random
from datetime import datetime
import os

# 模拟数据库
db = []
id_counter = 1

categories = ['类别A', '类别B', '类别C', '类别D']
names = ['数据项1', '数据项2', '数据项3', '数据项4', '数据项5']

# 生成初始数据
for _ in range(10):
    db.append({
        'id': id_counter,
        'name': random.choice(names),
        'value': random.randint(10, 100),
        'category': random.choice(categories),
        'timestamp': datetime.now().isoformat()
    })
    id_counter += 1

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(db).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            new_record = {
                'id': id_counter,
                'name': data.get('name'),
                'value': data.get('value'),
                'category': data.get('category'),
                'timestamp': datetime.now().isoformat()
            }
            db.append(new_record)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(new_record).encode())
        elif self.path == '/api/analyze':
            analysis = {
                'summary': '数据整体呈现上升趋势',
                'insights': [
                    '类别A占比最高，建议重点关注',
                    '最近7天数据增长明显',
                    '周末数据活跃度较低'
                ],
                'recommendations': [
                    '增加类别A的监控频率',
                    '优化周末数据采集策略',
                    '关注数据异常波动'
                ]
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(analysis).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run(port=8888):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    print(f'服务器运行在 http://localhost:{port}')
    print(f'已生成{len(db)}条初始数据')
    server.serve_forever()

if __name__ == '__main__':
    run()