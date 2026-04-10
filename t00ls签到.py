import requests
import json
import re
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置信息
COOKIE = 'UTH_visitedfid=39; smile=6D1; UTH_cookietime=2592000; UTH_auth=7946%2Fw7l%2FlFg0r1H4PIcAp6EY2w%2Bob1dwfgJf4bPdk2OgTWYFXGfsYilT4WNPvTvnYrJ15yFAkAEP9MqzIw2mAJW%2FJZaUNpaEFn%2Ffw; UTH_sid=6uEAqd'
PUSHPLUS_TOKEN = ''  # 如果需要推送，填写你的 token

def pushplus(title, content):
    """推送消息到 PushPlus"""
    if not PUSHPLUS_TOKEN:
        return
    
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    try:
        requests.post(url, json=data, timeout=10)
    except:
        pass

def extract_username(content):
    """从响应内容中提取用户名"""
    # 尝试从 <span> 标签中提取用户名
    pattern = r'<span>([^<]+)</span>'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    
    # 尝试从个人资料链接中提取用户名
    pattern = r'members-profile-\d+\.html[^>]*>([^<]+)</a>'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    
    return None

def test_cookie():
    """测试 Cookie 是否有效"""
    print("=== 测试 Cookie 有效性 ===")
    
    headers = {
        'Host': 'www.t00ls.com',
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.t00ls.com/'
    }
    
    try:
        response = requests.get(
            'https://www.t00ls.com/checklogin.html',
            headers=headers,
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.text
            
            # 提取用户名
            username = extract_username(content)
            
            if username:
                print(f"✅ Cookie 有效，{username} 账号已登录")
                return True, username
            elif '登录' in content and '退出' not in content:
                print("❌ Cookie 无效，显示登录链接")
                return False, None
            else:
                print("⚠️  未知响应格式")
                return False, None
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ 测试 Cookie 失败: {e}")
        return False, None

def get_formhash():
    """获取 formhash"""
    print("=== 获取 formhash ===")
    
    headers = {
        'Host': 'www.t00ls.com',
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.t00ls.com/'
    }
    
    try:
        response = requests.get(
            'https://www.t00ls.com/checklogin.html',
            headers=headers,
            verify=False,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
        
        content = response.text
        
        # 提取 formhash
        pattern = r'formhash=([a-f0-9]{8})'
        match = re.search(pattern, content)
        
        if match:
            formhash = match.group(1)
            print(f"✅ 找到 formhash: {formhash}")
            return formhash
        else:
            print("❌ 未找到 formhash")
            print("\n完整响应内容:")
            print("-" * 50)
            print(content)
            print("-" * 50)
            return None
            
    except Exception as e:
        print(f"❌ 获取 formhash 失败: {e}")
        return None

def sign_in(formhash):
    """执行签到"""
    print("=== 执行签到 ===")
    
    headers = {
        'Host': 'www.t00ls.com',
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.t00ls.com',
        'Referer': 'https://www.t00ls.com/',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }
    
    data = f'formhash={formhash}&signsubmit=apply'
    
    try:
        print(f"📤 签到请求数据: formhash={formhash}")
        response = requests.post(
            'https://www.t00ls.com/ajax-sign.json',
            headers=headers,
            data=data,
            verify=False,
            timeout=30
        )
        
        print(f"📥 响应状态码: {response.status_code}")
        
        # 格式化显示响应头
        print("\n📋 响应头:")
        print("-" * 40)
        headers_to_show = ['Date', 'Content-Type', 'Content-Length', 'Server', 'CF-RAY']
        for header in headers_to_show:
            if header in response.headers:
                print(f"  {header}: {response.headers[header]}")
        print("-" * 40)
        
        # 解析响应体
        try:
            result = response.json()
            print(f"\n📄 JSON 响应:")
            print(f"  status: {result.get('status', 'unknown')}")
            print(f"  message: {result.get('message', '无消息')}")
            return result
        except json.JSONDecodeError:
            print(f"\n❌ 非 JSON 响应: {response.text[:100]}")
            return {'status': 'error', 'message': response.text[:100]}
            
    except Exception as e:
        print(f"❌ 签到请求失败: {e}")
        return {'status': 'error', 'message': str(e)}

def debug_formhash():
    """调试获取 formhash"""
    print("=== 调试获取 formhash ===")
    
    headers = {
        'Host': 'www.t00ls.com',
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.t00ls.com/'
    }
    
    try:
        response = requests.get(
            'https://www.t00ls.com/checklogin.html',
            headers=headers,
            verify=False,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        content = response.text
        pattern = r'formhash=([a-f0-9]{8})'
        match = re.search(pattern, content)
        
        if match:
            print(f"✅ 找到 formhash: {match.group(1)}")
        else:
            print("❌ 未找到 formhash")
            print("\n完整响应内容:")
            print("-" * 50)
            print(content)
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ 调试失败: {e}")

def main():
    print("🚀 开始 T00ls 签到...\n")
    
    # 1. 测试 Cookie
    cookie_valid, username = test_cookie()
    print()
    
    if not cookie_valid:
        print("❌ 请从浏览器获取最新的 Cookie 并更新脚本中的 COOKIE 变量")
        pushplus('T00ls签到失败', 'Cookie已失效，请重新登录')
        return
    
    # 2. 获取 formhash
    formhash = get_formhash()
    print()
    
    if not formhash:
        print("❌ 无法获取 formhash，签到失败")
        pushplus('T00ls签到失败', '无法获取formhash')
        return
    
    # 3. 执行签到
    result = sign_in(formhash)
    print()
    
    # 4. 处理结果
    print("📊 签到结果:")
    print("-" * 40)
    
    if 'status' in result:
        if result['status'] == 'success':
            message = result.get('message', '签到成功')
            print(f"🎉 {message}")
            pushplus('T00ls签到成功', f"用户: {username}\n{message}")
        elif result.get('message') == 'alreadysign':
            print("📝 今日已签到")
            pushplus('T00ls签到提醒', f"用户: {username}\n今日已签到")
        else:
            print(f"❌ 签到失败: {result.get('message', '未知错误')}")
            pushplus('T00ls签到失败', f"用户: {username}\n{result}")
    else:
        print(f"❌ 未知响应格式: {result}")
        pushplus('T00ls签到异常', f"用户: {username}\n{result}")
    
    print("-" * 40)

if __name__ == '__main__':
    print("=" * 50)
    print("📱 T00ls 签到脚本")
    print("=" * 50)
    print("1. 测试 Cookie 有效性")
    print("2. 调试获取 formhash")
    print("3. 执行签到")
    print("4. 退出")
    print("-" * 50)
    
    choice = input("请选择 (1-4): ").strip()
    
    if choice == '1':
        test_cookie()
    elif choice == '2':
        debug_formhash()
    elif choice == '3':
        main()
    else:
        print("👋 退出脚本")
