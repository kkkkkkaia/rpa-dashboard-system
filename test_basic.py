import requests

# Supabase配置
url = "https://kxpvyzokzwruustynjrk.supabase.co"
key = "sb_publishable_WavBS4LVdCn_5okwYujlUA_mZuL-WPZ"

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}"
}

print("测试Supabase数据库连接...")
print("URL:", url)
print("Key:", key[:20] + "...")
print()

# 测试连接
try:
    response = requests.get(url + "/rest/v1/", headers=headers, timeout=5)
    print("连接测试:")
    print("状态码:", response.status_code)
    print("响应:", response.text[:100] + "...")
    print()
except Exception as e:
    print("连接测试失败:", e)
    print()

# 测试表是否存在
try:
    response = requests.get(url + "/rest/v1/帖子实时分析", headers=headers, params={"limit": 1}, timeout=5)
    print("表测试:")
    print("状态码:", response.status_code)
    if response.status_code == 200:
        data = response.json()
        print("数据条数:", len(data))
        if data:
            print("字段:", list(data[0].keys()))
            print("示例:", data[0])
    else:
        print("响应:", response.text)
except Exception as e:
    print("表测试失败:", e)

print("\n测试完成")