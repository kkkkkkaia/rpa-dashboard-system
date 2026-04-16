import os
from supabase import create_client, Client

# Supabase配置
url = "https://kxpvyzokzwruustynjrk.supabase.co"
key = "sb_publishable_WavBS4LVdCn_5okwYujlUA_mZuL-WPZ"

def test_supabase_connection():
    """测试Supabase连接并查看数据库结构"""
    print("=== Supabase数据库测试 ===")
    print(f"连接到: {url}")
    print()
    
    try:
        # 创建Supabase客户端
        supabase: Client = create_client(url, key)
        print("✅ 连接成功!")
        print()
        
        # 1. 测试数据库连接
        print("1. 测试数据库连接:")
        try:
            # 尝试获取项目信息
            response = supabase.rpc("echo", {"value": "test"}).execute()
            print("   ✅ 数据库连接正常")
        except Exception as e:
            print(f"   ❌ 数据库连接测试失败: {e}")
        print()
        
        # 2. 查看所有表
        print("2. 查看数据库表结构:")
        try:
            # 使用PostgreSQL系统表查询所有表
            result = supabase.rpc("get_all_tables").execute()
            if result.data:
                print("   数据库中的表:")
                for table in result.data:
                    print(f"   - {table['table_name']}")
            else:
                # 备选方案：直接尝试查询已知表
                print("   尝试查询已知表...")
                tables_to_test = ["帖子实时分析", "posts", "users", "analytics"]
                for table in tables_to_test:
                    try:
                        result = supabase.table(table).select("*").limit(1).execute()
                        print(f"   ✅ 表 '{table}' 存在")
                    except Exception:
                        pass
        except Exception as e:
            print(f"   ❌ 查询表结构失败: {e}")
        print()
        
        # 3. 查看"帖子实时分析"表结构
        print("3. 查看'帖子实时分析'表结构:")
        try:
            # 尝试获取表结构
            result = supabase.rpc("get_table_columns", {"table_name": "帖子实时分析"}).execute()
            if result.data:
                print("   表字段:")
                for column in result.data:
                    print(f"   - {column['column_name']} ({column['data_type']})")
            else:
                # 备选方案：获取前几条数据来推断结构
                result = supabase.table("帖子实时分析").select("*").limit(5).execute()
                if result.data:
                    print("   从数据推断的字段:")
                    if result.data:
                        sample = result.data[0]
                        for key, value in sample.items():
                            print(f"   - {key} ({type(value).__name__})")
                    print(f"   \n示例数据 (前5条):")
                    for i, item in enumerate(result.data):
                        print(f"   {i+1}. {item}")
                else:
                    print("   表存在但无数据")
        except Exception as e:
            print(f"   ❌ 查询表结构失败: {e}")
        print()
        
        # 4. 测试数据获取
        print("4. 测试数据获取:")
        try:
            result = supabase.table("帖子实时分析").select("*").order("created_at", desc=True).limit(10).execute()
            if result.data:
                print(f"   ✅ 成功获取 {len(result.data)} 条数据")
                print("   最新10条数据:")
                for i, item in enumerate(result.data[:5]):  # 只显示前5条
                    print(f"   {i+1}. {item}")
                if len(result.data) > 5:
                    print(f"   ... 还有 {len(result.data) - 5} 条数据")
            else:
                print("   ⚠️  表中无数据")
        except Exception as e:
            print(f"   ❌ 获取数据失败: {e}")
        print()
        
        # 5. 测试数据统计
        print("5. 数据统计:")
        try:
            # 总记录数
            count_result = supabase.table("帖子实时分析").select("*", count="exact").execute()
            total_count = count_result.count or 0
            print(f"   总记录数: {total_count}")
            
            # 分类统计
            if total_count > 0:
                categories = supabase.table("帖子实时分析").select("category").execute()
                category_set = set(item["category"] for item in categories.data if "category" in item)
                print(f"   分类数量: {len(category_set)}")
                if category_set:
                    print(f"   分类: {', '.join(category_set)}")
        except Exception as e:
            print(f"   ❌ 统计失败: {e}")
        print()
        
        print("=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请检查API密钥和URL是否正确")

def main():
    test_supabase_connection()

if __name__ == "__main__":
    main()