import requests
import json

# Supabase配置
SUPABASE_URL = "https://kxpvyzokzwruustynjrk.supabase.co"
SUPABASE_KEY = "sb_publishable_WavBS4LVdCn_5okwYujlUA_mZuL-WPZ"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def test_supabase_connection():
    """测试Supabase连接并查看数据库结构"""
    print("=== Supabase数据库测试 ===")
    print(f"连接到: {SUPABASE_URL}")
    print()
    
    try:
        # 1. 测试连接
        print("1. 测试连接:")
        health_url = f"{SUPABASE_URL}/rest/v1/"
        response = requests.get(health_url, headers=headers)
        if response.status_code == 200:
            print("   ✅ 连接成功!")
        else:
            print(f"   ❌ 连接失败: {response.status_code}")
        print()
        
        # 2. 查看表结构
        print("2. 查看'帖子实时分析'表结构:")
        table_url = f"{SUPABASE_URL}/rest/v1/帖子实时分析"
        response = requests.get(table_url, headers=headers, params={"limit": 1})
        
        if response.status_code == 200:
            data = response.json()
            if data:
                sample = data[0]
                print("   表字段:")
                for key, value in sample.items():
                    print(f"   - {key} ({type(value).__name__})")
                print()
                print("   示例数据:")
                print(f"   {sample}")
            else:
                print("   ⚠️  表存在但无数据")
        elif response.status_code == 404:
            print("   ❌ 表不存在")
        else:
            print(f"   ❌ 查询失败: {response.status_code}")
        print()
        
        # 3. 测试数据获取
        print("3. 测试数据获取:")
        response = requests.get(table_url, headers=headers, params={"limit": 10, "order": "created_at.desc"})
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 成功获取 {len(data)} 条数据")
            if data:
                print("   最新10条数据:")
                for i, item in enumerate(data[:5]):  # 只显示前5条
                    print(f"   {i+1}. {item}")
                if len(data) > 5:
                    print(f"   ... 还有 {len(data) - 5} 条数据")
        else:
            print(f"   ❌ 获取数据失败: {response.status_code}")
        print()
        
        # 4. 测试数据统计
        print("4. 数据统计:")
        response = requests.get(table_url, headers=headers, params={"select": "count(*)", "head": "true"})
        
        if response.status_code == 200:
            count = response.headers.get("X-Count", 0)
            print(f"   总记录数: {count}")
            
            # 分类统计
            response = requests.get(table_url, headers=headers, params={"select": "category", "distinct": "true"})
            if response.status_code == 200:
                categories = response.json()
                category_list = [cat["category"] for cat in categories if "category" in cat]
                print(f"   分类数量: {len(category_list)}")
                if category_list:
                    print(f"   分类: {', '.join(category_list)}")
        else:
            print(f"   ❌ 统计失败: {response.status_code}")
        print()
        
        print("=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("请检查API密钥和URL是否正确")

def main():
    test_supabase_connection()

if __name__ == "__main__":
    main()