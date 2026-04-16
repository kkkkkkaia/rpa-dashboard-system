import requests
import random
import time

# API端点
API_URL = 'http://localhost:3000/api/data'

# 模拟数据类别
CATEGORIES = ['类别A', '类别B', '类别C', '类别D']
# 模拟数据名称
NAMES = ['数据项1', '数据项2', '数据项3', '数据项4', '数据项5']

def generate_data():
    """生成模拟数据"""
    return {
        'name': random.choice(NAMES),
        'value': random.randint(10, 100),
        'category': random.choice(CATEGORIES)
    }

def send_data(data):
    """发送数据到API"""
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print(f"数据发送成功: {data}")
        else:
            print(f"数据发送失败: {response.status_code}")
    except Exception as e:
        print(f"发送数据时出错: {e}")

def main():
    """主函数"""
    print("开始RPA数据采集...")
    for i in range(10):  # 生成10条数据
        data = generate_data()
        send_data(data)
        time.sleep(1)  # 每1秒发送一条数据
    print("RPA数据采集完成")

if __name__ == "__main__":
    main()