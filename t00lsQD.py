import requests
import json
import re
import urllib3
import random
import time
from datetime import datetime, timedelta
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置信息
COOKIE = 'UTH_visitedfid=39; smile=6D1; UTH_cookietime=2592000; UTH_auth=7946%2Fw7l%2FlFg0r1H4PIcAp6EY2w%2Bob1dwfgJf4bPdk2OgTWYFXGfsYilT4WNPvTvnYrJ15yFAkAEP9MqzIw2mAJW%2FJZaUNpaEFn%2Ffw; UTH_sid=6uEAqd'
PUSHPLUS_TOKEN = ''  # 如果需要推送，填写你的 token

def calculate_next_execution_time():
    """计算下一次执行时间（11:30-12:00之间的随机时间）"""
    now = datetime.now()
    
    # 如果当前时间在11:30之前，则今天执行
    if now.hour < 11 or (now.hour == 11 and now.minute < 30):
        target_date = now.date()
    # 如果当前时间在11:30-12:00之间，则立即执行
    elif now.hour == 11 and now.minute >= 30:
        return now  # 立即执行
    # 如果当前时间在12:00之后，则明天执行
    else:
        target_date = now.date() + timedelta(days=1)
    
    # 设置目标时间范围：11:30:00 到 12:00:00
    base_time = datetime.combine(target_date, datetime.strptime("11:30:00", "%H:%M:%S").time())
    
    # 生成随机秒数（0到1800秒之间，即30分钟）
    random_seconds = random.randint(0, 1800)
    
    # 计算目标执行时间
    target_time = base_time + timedelta(seconds=random_seconds)
    
    return target_time

def wait_until(target_time):
    """等待到指定时间"""
    now = datetime.now()
    
    # 如果已经过了目标时间，立即执行
    if now >= target_time:
        return target_time
    
    # 计算需要等待的秒数
    wait_seconds = (target_time - now).total_seconds()
    
    print(f"⏰ 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ 计划执行时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ 等待 {wait_seconds:.2f} 秒后执行...")
    
    # 等待到目标时间
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    
    return target_time

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

def get_formhash_and_username():
    """获取 formhash 和用户名"""
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
            return None, None
        
        content = response.text
        
        # 提取用户名
        username = extract_username(content)
        
        # 提取 formhash
        pattern = r'formhash=([a-f0-9]{8})'
        match = re.search(pattern, content)
        
        if match:
            formhash = match.group(1)
            return formhash, username
        else:
            return None, username
            
    except Exception as e:
        print(f"❌ 获取信息失败: {e}")
        return None, None

def sign_in(formhash, username):
    """执行签到"""
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
        response = requests.post(
            'https://www.t00ls.com/ajax-sign.json',
            headers=headers,
            data=data,
            verify=False,
            timeout=30
        )
        
        # 记录当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取完整的响应数据
        response_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'text': response.text,
            'time': current_time
        }
        
        # 尝试解析JSON
        try:
            json_result = response.json()
            response_data['json'] = json_result
            return response_data, json_result
        except json.JSONDecodeError:
            response_data['json'] = None
            return response_data, {'status': 'error', 'message': response.text[:100]}
            
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_data = {
            'status_code': 0,
            'headers': {},
            'text': str(e),
            'json': None,
            'time': current_time
        }
        return response_data, {'status': 'error', 'message': str(e)}

def format_response_data(response_data):
    """格式化响应数据用于显示"""
    formatted = []
    formatted.append(f"⚠️ 请求时间: {response_data['time']}")
    formatted.append(f"⚠️ 状态码: {response_data['status_code']}")
    
    
    # 显示响应体
    if response_data['json']:
        formatted.append("\n⚠️ JSON 响应:")
        formatted.append(f"  {json.dumps(response_data['json'], ensure_ascii=False, indent=2)}")
    elif response_data['text']:
        formatted.append("\n⚠️ 响应体:")
        # 限制显示长度，避免过长
        text_preview = response_data['text'][:500]
        if len(response_data['text']) > 500:
            text_preview += "..."
        formatted.append(f"  {text_preview}")
    
    return "\n".join(formatted)

def execute_sign_in():
    """执行签到任务"""
    print("=" * 50)
    print("⚠️ T00ls 自动签到脚本")
    print("=" * 50)
    
    # 1. 获取 formhash 和用户名
    print("\n⚠️ 获取签到信息...")
    formhash, username = get_formhash_and_username()
    
    if not formhash:
        print("❌ 无法获取 formhash，签到失败")
        pushplus('T00ls签到失败', '无法获取formhash')
        return False
    
    if not username:
        print("⚠️  无法获取用户名，继续签到...")
        username = "未知用户"
    else:
        print(f"✅ 当前用户: {username}")
        print(f"✅ 获取到 formhash: {formhash}")
    
    # 2. 执行签到
    print("\n⚠️ 正在签到...")
    response_data, result = sign_in(formhash, username)
    
    # 3. 处理结果
    print("\n" + "=" * 50)
    print("⚠️ 签到结果")
    print("=" * 50)
    
    # 显示完整的响应数据
    print("\n" + format_response_data(response_data))
    
    print("=" * 50)
    print("⚠️ 签到状态:")
    
    success = False
    if 'status' in result:
        if result['status'] == 'success':
            message = result.get('message', '签到成功')
            print(f"✅ {message}")
            pushplus('✅T00ls签到成功', 
                    f"**用户**: {username}\n"
                    f"**时间**: {response_data['time']}\n"
                    f"**状态**: {message}\n"
                    f"**响应**: ```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```")
            success = True
        elif result.get('message') == 'alreadysign':
            print("❌ 今日已签到")
            pushplus('T00ls签到提醒', 
                    f"**用户**: {username}\n"
                    f"**时间**: {response_data['time']}\n"
                    f"**状态**: 今日已签到\n"
                    f"**响应**: ```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```")
            success = True  # 已签到也算完成任务
        else:
            print(f"❌ 签到失败: {result.get('message', '未知错误')}")
            pushplus('T00ls签到失败', 
                    f"**用户**: {username}\n"
                    f"**时间**: {response_data['time']}\n"
                    f"**状态**: 签到失败\n"
                    f"**错误**: {result.get('message', '未知错误')}\n"
                    f"**响应**: ```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```")
    else:
        print(f"❌ 未知响应格式: {result}")
        pushplus('T00ls签到异常', 
                f"**用户**: {username}\n"
                f"**时间**: {response_data['time']}\n"
                f"**状态**: 未知响应格式\n"
                f"**响应**: ```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```")
    
    print("=" * 50)
    return success

def main():
    """主函数：循环执行签到"""
    execution_count = 0
    max_executions = 365  # 最多执行365天（一年）
    
    while execution_count < max_executions:
        execution_count += 1
        print(f"\n{'='*60}")
        print(f"📅 第 {execution_count} 次执行")
        print(f"{'='*60}")
        
        # 计算下一次执行时间
        next_time = calculate_next_execution_time()
        
        # 等待到执行时间
        scheduled_time = wait_until(next_time)
        print(f"✅ 到达计划执行时间: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 执行签到
        success = execute_sign_in()
        
        if success:
            print(f"\n✅ 第 {execution_count} 次签到任务完成")
        else:
            print(f"\n❌ 第 {execution_count} 次签到任务失败")
        
        # 计算下一次执行时间（明天）
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.date()
        
        # 设置明天11:30-12:00之间的随机时间
        base_time = datetime.combine(tomorrow_date, datetime.strptime("11:30:00", "%H:%M:%S").time())
        random_seconds = random.randint(0, 1800)
        next_execution_time = base_time + timedelta(seconds=random_seconds)
        
        # 计算需要等待的时间
        wait_until_tomorrow = (next_execution_time - datetime.now()).total_seconds()
        
        print(f"\n⏰ 下一次执行时间: {next_execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ 距离下一次执行还有: {wait_until_tomorrow/3600:.2f} 小时")
        
        # 如果距离下一次执行时间很短，直接等待
        if wait_until_tomorrow < 3600:  # 小于1小时
            print(f"⏰ 等待 {wait_until_tomorrow/60:.2f} 分钟后执行下一次...")
            time.sleep(wait_until_tomorrow)
        else:
            # 否则，等待到接近执行时间（提前5分钟）
            wait_until_near = wait_until_tomorrow - 300  # 提前5分钟
            if wait_until_near > 0:
                print(f"⏰ 等待 {wait_until_near/3600:.2f} 小时后进入下一次循环...")
                time.sleep(wait_until_near)
        
        print(f"\n{'='*60}")
        print(f"🔄 准备下一次执行...")
        print(f"{'='*60}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，脚本停止")
    except Exception as e:
        print(f"\n\n❌ 脚本异常: {e}")
        print("脚本停止")
