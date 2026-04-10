#!/usr/bin/env python3
"""
T00ls WHOIS查询专用域名生成器 - 增强版
生成所有可能的冷门域名组合并进行存活检测
"""

import subprocess
import socket
import concurrent.futures
import time
from datetime import datetime
import itertools

class T00lsDomainGenerator:
    def __init__(self):
        # 冷门行业专业术语（英文）
        self.obscure_terms = [
            # 工业冷门部件
            'gudgeon', 'trunnion', 'grommet', 'ferrule', 'spigot', 'collet',
            'arbor', 'mandrel', 'bushing', 'flange', 'gusset', 'spar',
            
            # 生物学冷门术语
            'xylem', 'phloem', 'cambium', 'mycelium', 'hyphae', 'sporangia',
            'plasmodium', 'flagellum', 'cilia', 'chromatophore',
            
            # 化学专业术语
            'azimuth', 'zeolite', 'fulvate', 'clathrate', 'adduct', 'enolate',
            'zwitterion', 'mesylate', 'tosylate',
            
            # 地质学冷门词
            'horst', 'graben', 'esker', 'kame', 'drumlin', 'moraine',
            'xenolith', 'ophiolite',
            
            # 古英语/罕见词
            'widdershins', 'defenestration', 'callipygian', 'susurrus',
            'petrichor', 'limerence'
        ]
        
        # 随机后缀（非主流）
        self.rare_suffixes = [
            'ite', 'oid', 'ula', 'ule', 'isk', 'aceous', 'iferous', 
            'escent', 'trix', 'tron'
        ]
        
        # 冷门前缀
        self.rare_prefixes = [
            'meta', 'para', 'ortho', 'iso', 'neo', 'paleo',
            'crypto', 'xeno', 'myco', 'phyto', 'zoo'
        ]
        
        # 数字组合
        self.number_combos = [
            '23', '45', '67', '89', '234', '567', '789', '235', '478',
            '1998', '2002', '2005', '2011', '2014', '2017'
        ]
        
        # 随机字母组合
        self.random_combos = [
            'zq', 'xj', 'qp', 'zx', 'kj', 'vw', 'mn', 'bd',
            'gh', 'kl', 'ty', 'ui', 'op', 'as', 'df'
        ]
        
        print(f"[*] T00ls域名生成器初始化完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] 词库统计:")
        print(f"    - 专业术语: {len(self.obscure_terms)}个")
        print(f"    - 前缀: {len(self.rare_prefixes)}个")
        print(f"    - 后缀: {len(self.rare_suffixes)}个")
        print(f"    - 数字组合: {len(self.number_combos)}个")
        print(f"    - 字母组合: {len(self.random_combos)}个")
    
    def generate_all_combinations(self):
        """生成所有可能的域名组合"""
        all_domains = set()  # 使用集合避免重复
        
        print("\n[*] 开始生成所有可能的域名组合...")
        
        # 方法1: 纯术语
        print(f"[*] 生成纯术语域名...")
        for term in self.obscure_terms:
            all_domains.add(f"{term}.com")
        
        # 方法2: 术语 + 数字（前后）
        print(f"[*] 生成术语+数字组合域名...")
        for term in self.obscure_terms:
            for num in self.number_combos:
                all_domains.add(f"{term}{num}.com")
                all_domains.add(f"{num}{term}.com")
        
        # 方法3: 前缀 + 术语
        print(f"[*] 生成前缀+术语组合域名...")
        for prefix in self.rare_prefixes:
            for term in self.obscure_terms:
                all_domains.add(f"{prefix}{term}.com")
        
        # 方法4: 前缀 + 术语 + 后缀
        print(f"[*] 生成前缀+术语+后缀组合域名...")
        for prefix in self.rare_prefixes:
            for term in self.obscure_terms:
                for suffix in self.rare_suffixes:
                    all_domains.add(f"{prefix}{term}{suffix}.com")
        
        # 方法5: 术语 + 后缀
        print(f"[*] 生成术语+后缀组合域名...")
        for term in self.obscure_terms:
            for suffix in self.rare_suffixes:
                all_domains.add(f"{term}{suffix}.com")
        
        # 方法6: 字母组合 + 术语
        print(f"[*] 生成字母组合+术语域名...")
        for combo in self.random_combos:
            for term in self.obscure_terms:
                all_domains.add(f"{combo}{term}.com")
                all_domains.add(f"{term}{combo}.com")
        
        # 方法7: 修改字符的术语（模拟打字错误）
        print(f"[*] 生成修改字符的域名...")
        for term in self.obscure_terms:
            if len(term) > 4:
                chars = list(term)
                # 替换每个位置的字符
                for i in range(len(chars)):
                    for replacement in ['x', 'z', 'q', 'k', 'v']:
                        if chars[i] != replacement:
                            modified_chars = chars.copy()
                            modified_chars[i] = replacement
                            modified_word = ''.join(modified_chars)
                            all_domains.add(f"{modified_word}.com")
        
        # 转换为列表并排序
        domains_list = sorted(list(all_domains))
        
        print(f"[+] 总共生成 {len(domains_list)} 个唯一域名")
        return domains_list
    
    def check_domain_alive(self, domain):
        """
        检查域名是否存活（通过DNS解析）
        返回: (domain, is_alive)
        """
        try:
            # 移除.com后缀获取主机名
            hostname = domain.replace('.com', '')
            
            # 方法1: 尝试DNS解析
            socket.gethostbyname(domain)
            return (domain, True)
            
        except socket.gaierror:
            # DNS解析失败，域名可能不存在
            return (domain, False)
        except Exception as e:
            # 其他异常，视为不存在
            return (domain, False)
    
    def check_domains_concurrently(self, domains, max_workers=50):
        """
        并发检查域名存活状态
        """
        alive_domains = []
        total = len(domains)
        
        print(f"\n[*] 开始检查 {total} 个域名的存活状态...")
        print(f"[*] 使用 {max_workers} 个并发线程")
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有检查任务
            future_to_domain = {executor.submit(self.check_domain_alive, domain): domain for domain in domains}
            
            # 处理完成的任务
            completed = 0
            for future in concurrent.futures.as_completed(future_to_domain):
                completed += 1
                domain, is_alive = future.result()
                
                if is_alive:
                    alive_domains.append(domain)
                
                # 显示进度
                if completed % 100 == 0 or completed == total:
                    elapsed = time.time() - start_time
                    speed = completed / elapsed if elapsed > 0 else 0
                    print(f"   进度: {completed}/{total} ({completed/total*100:.1f}%) | "
                          f"存活: {len(alive_domains)} | "
                          f"速度: {speed:.1f}个/秒")
        
        elapsed = time.time() - start_time
        print(f"\n[+] 检查完成!")
        print(f"    总耗时: {elapsed:.2f}秒")
        print(f"    检查速度: {total/elapsed:.1f}个/秒")
        print(f"    存活域名: {len(alive_domains)}个")
        print(f"    无效域名: {total - len(alive_domains)}个")
        
        return alive_domains
    
    def save_to_file(self, domains, filename="t00ls_domains.txt", alive_only=False):
        """保存域名到文件"""
        if alive_only:
            filename = "t00ls_alive_domains.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# T00ls WHOIS查询专用域名列表\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 总数: {len(domains)}个\n")
            
            if alive_only:
                f.write(f"# 类型: 存活域名（已通过DNS验证）\n")
            else:
                f.write(f"# 类型: 所有生成域名\n")
            
            f.write("#" * 60 + "\n\n")
            
            for i, domain in enumerate(domains, 1):
                f.write(f"{domain}\n")
        
        print(f"[+] 已保存 {len(domains)} 个域名到 {filename}")
        
        # 显示前20个域名
        print(f"\n[+] 前20个域名:")
        for i, domain in enumerate(domains[:20], 1):
            print(f"  {i:3d}. {domain}")
        
        if len(domains) > 20:
            print(f"  ... 还有 {len(domains)-20} 个域名")

def main():
    generator = T00lsDomainGenerator()
    
    # 1. 生成所有可能的组合
    all_domains = generator.generate_all_combinations()
    
    # 显示统计信息
    print(f"\n[+] 域名生成统计:")
    print(f"    总生成数: {len(all_domains)}")
    
    # 按长度分组统计
    length_groups = {}
    for domain in all_domains:
        length = len(domain.replace('.com', ''))
        length_groups[length] = length_groups.get(length, 0) + 1
    
    print(f"\n[+] 域名长度分布:")
    for length in sorted(length_groups.keys()):
        count = length_groups[length]
        percentage = count / len(all_domains) * 100
        print(f"    {length:2d}字符: {count:4d}个 ({percentage:.1f}%)")
    
    # 保存所有生成的域名
    generator.save_to_file(all_domains, "t00ls_all_domains.txt")
    
    # 2. 检查域名存活状态
    print("\n" + "="*60)
    print("[*] 开始域名存活检测阶段")
    print("="*60)
    
    # 询问是否进行存活检测
    response = input("\n[?] 是否进行域名存活检测？(y/n, 默认y): ").strip().lower()
    
    if response in ['y', 'yes', '']:
        # 进行存活检测
        alive_domains = generator.check_domains_concurrently(all_domains, max_workers=50)
        
        # 保存存活域名
        if alive_domains:
            generator.save_to_file(alive_domains, alive_only=True)
            
            print(f"\n[!] 重要提醒:")
            print(f"    1. 存活域名已保存到 t00ls_alive_domains.txt")
            print(f"    2. 这些域名已通过DNS验证，更可能在T00ls中未被查询")
            print(f"    3. 建议每天从列表中随机选择一个查询")
            print(f"    4. 查询时间建议: 凌晨0:00-6:00")
        else:
            print(f"\n[!] 警告: 未发现存活域名")
            print(f"    这可能是因为所有生成的域名都未被注册")
            print(f"    或者DNS检查过于严格")
    
    else:
        print(f"\n[!] 跳过存活检测")
        print(f"    所有生成的域名已保存到 t00ls_all_domains.txt")
    
    print(f"\n[+] 任务完成!")
    print(f"    当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
