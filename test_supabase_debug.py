import requests
import json
import sys

# Supabase配置
SUPABASE_URL = "https://kxpvyzokzwruustynjrk.supabase.co"
SUPABASE_KEY = "sb_publishable_WavBS4LVdCn_5okwYujlUA_mZuL-WPZ"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def print_debug(message):
    """打印调试信息"""
    print("DEBUG: " + message)

def test_supabase_connection():
    """测试Supabase连接并查看数据库结构"""
    print("=== Supabase数据库测试 ===")
    print("连接到: " + SUPABASE_URL)
    print()
    
    try:
        # 1. 测试连接
        print("1. 测试连接:")
        health_url = SUPABASE_URL + "/rest/v1/"
        print_debug("请求URL: " + health_url)
        print_debug("请求头: " + str(headers))
        
        response = requests.get(health_url, headers=headers, timeout=10)
        print_debug("响应状态码: " + str(response.status_code))
        print_debug("响应内容: " + response.text[:200] + "...")
        
        if response.status_code == 200:
            print("   连接成功!")
        else:
            print("   连接失败: " + str(response.status_code))
        print()
        
        # 2. 测试表是否存在
        print("2. 测试'帖子实时分析'表是否存在:")
        table_url = SUPABASE_URL + "/rest/v1/帖子实时分析"
        print_debug("表URL: " + table_url)
        
        response = requests.get(table_url, headers=headers, params={"limit": 1}, timeout=10)
        print_debug("响应状态码: " + str(response.status_code))
        
        if response.status_code == 200:
            print("   表存在")
            data = response.json()
            print_debug("响应数据: " + str(data))
            
            if data:
                sample = data[0]
                print("   表结构:")
                for key, value in sample.items():
                    print("   - " + key + " (" + type(value).__name__ + ")")
                print()
                print("   示例数据:")
                print("   " + str(sample))
            else:
                print("   表存在但无数据")
        elif response.status_code == 404:
            print("   表不存在")
        else:
            print("   查询失败: " + str(response.status_code))
            print_debug("响应内容: " + response.text)
        print()
        
        # 3. 测试其他可能的表
        print("3. 测试其他可能的表:")
        tables = ["posts", "users", "analytics", "data"]
        for table in tables:
            table_url = SUPABASE_URL + "/rest/v1/" + table
            try:
                response = requests.get(table_url, headers=headers, params={"limit": 1}, timeout=5)
                if response.status_code == 200:
                    print("   表 '" + table + "' 存在")
                    data = response.json()
                    if data:
                        sample = data[0]
                        print("   字段: " + ", ".join(sample.keys()))
                elif response.status_code == 404:
                    print("   表 '" + table + "' 不存在")
                else:
                    print("   表 '" + table + "' 查询失败: " + str(response.status_code))
            except Exception as e:
                print("   表 '" + table + "' 测试失败: " + str(e))
        print()
        
        print("=== 测试完成 ===")
        
    except Exception as e:
        print("测试失败: " + str(e))
        print("请检查API密钥和URL是否正确")
        import traceback
        traceback.print_exc()

def main():
    test_supabase_connection()

if __name__ == "__main__":
    main()