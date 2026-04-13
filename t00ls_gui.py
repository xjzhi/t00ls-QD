import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import re
import urllib3
import threading
from datetime import datetime
import os
import webbrowser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ModernT00lsSignGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("T00ls Auto-Sign")
        self.root.geometry("900x700")

        # 设置窗口最小尺寸
        self.root.minsize(800, 600)

        # 设置图标
        self.setup_icon()

        # 应用自定义颜色主题
        self.setup_colors()

        # 配置变量
        self.cookie_var = tk.StringVar()
        self.status_var = tk.StringVar(value="就绪")
        self.username_var = tk.StringVar(value="未登录")
        self.sign_status_var = tk.StringVar(value="● 未签到")

        # 创建主界面
        self.create_main_layout()

        # 加载配置
        self.load_config()

        # 初始化日志
        self.setup_logging()

    def setup_colors(self):
        """设置自定义颜色主题"""
        # 现代深色主题
        self.colors = {
            'bg_dark': '#1e1e2e',           # 主要背景
            'bg_light': '#2d2d3b',          # 次要背景
            'bg_card': '#3a3a4e',           # 卡片背景
            'text_primary': '#ffffff',      # 主要文字
            'text_secondary': '#b8b8b8',    # 次要文字
            'accent': '#5865f2',            # 强调色（蓝色）
            'accent_hover': '#4752c4',      # 强调色悬停
            'success': '#43a047',           # 成功色（绿色）
            'warning': '#fb8c00',           # 警告色（橙色）
            'error': '#e53935',             # 错误色（红色）
            'border': '#404040',            # 边框颜色
            'input_bg': '#252535',          # 输入框背景
        }

        # 设置窗口背景
        self.root.configure(bg=self.colors['bg_dark'])

    def setup_icon(self):
        """设置应用图标"""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

    def create_main_layout(self):
        """创建主布局"""
        # 创建主要框架
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 左侧控制面板
        left_panel = tk.Frame(main_container, bg=self.colors['bg_light'], relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # 右侧日志面板
        right_panel = tk.Frame(main_container, bg=self.colors['bg_dark'], relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 左侧面板内容
        self.create_left_panel(left_panel)

        # 右侧面板内容
        self.create_right_panel(right_panel)

    def create_left_panel(self, parent):
        """创建左侧控制面板"""
        # 标题区域
        title_frame = tk.Frame(parent, bg=self.colors['bg_light'], height=60)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        # 应用标题
        title_label = tk.Label(
            title_frame,
            text="T00ls Auto-Sign",
            font=("Microsoft YaHei", 20, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=15)

        # 分割线
        separator = tk.Frame(title_frame, height=1, bg=self.colors['border'])
        separator.pack(fill=tk.X, padx=10)

        # 账户信息卡片
        account_card = self.create_card(parent, "账户信息")

        # 用户名显示
        user_frame = tk.Frame(account_card, bg=self.colors['bg_card'])
        user_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            user_frame,
            text="当前账号:",
            font=("Microsoft YaHei", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(10, 5))

        self.username_label = tk.Label(
            user_frame,
            textvariable=self.username_var,
            font=("Microsoft YaHei", 10, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['success'],
            anchor=tk.W
        )
        self.username_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 签到状态显示
        status_frame = tk.Frame(account_card, bg=self.colors['bg_card'])
        status_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            status_frame,
            text="签到状态:",
            font=("Microsoft YaHei", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(10, 5))

        self.status_label = tk.Label(
            status_frame,
            textvariable=self.sign_status_var,
            font=("Microsoft YaHei", 10, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Cookie设置卡片
        cookie_card = self.create_card(parent, "Cookie设置")

        # Cookie输入区域
        tk.Label(
            cookie_card,
            text="Cookie字符串:",
            font=("Microsoft YaHei", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(10, 5))

        # 使用Text小部件代替Entry以便显示多行内容和滚动条
        cookie_frame = tk.Frame(cookie_card, bg=self.colors['bg_card'])
        cookie_frame.pack(fill=tk.X, padx=10, pady=5)

        self.cookie_text = scrolledtext.ScrolledText(
            cookie_frame,
            height=4,
            font=("Consolas", 9),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=2,
            highlightthickness=0
        )
        self.cookie_text.pack(fill=tk.BOTH, expand=True)

        # 从变量中设置初始值
        self.cookie_text.insert(1.0, self.cookie_var.get())

        # 绑定文本变化事件
        def on_cookie_change(event=None):
            content = self.cookie_text.get(1.0, tk.END).strip()
            self.cookie_var.set(content)

        self.cookie_text.bind('<KeyRelease>', on_cookie_change)

        # Cookie操作按钮
        button_frame = tk.Frame(cookie_card, bg=self.colors['bg_card'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # 帮助按钮
        help_btn = self.create_button(
            button_frame,
            "获取帮助",
            self.get_cookie_help,
            self.colors['bg_light'],
            self.colors['text_primary']
        )
        help_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 测试按钮
        test_btn = self.create_button(
            button_frame,
            "测试Cookie",
            self.test_cookie_thread,
            self.colors['accent'],
            self.colors['text_primary']
        )
        test_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 管理卡片
        manage_card = self.create_card(parent, "管理操作")

        # 操作按钮
        action_frame = tk.Frame(manage_card, bg=self.colors['bg_card'])
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        # 保存配置按钮
        save_btn = self.create_button(
            action_frame,
            "💾 保存配置",
            self.save_config,
            self.colors['success'],
            self.colors['text_primary']
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 加载配置按钮
        load_btn = self.create_button(
            action_frame,
            "📂 加载配置",
            self.load_config_dialog,
            self.colors['bg_light'],
            self.colors['text_primary']
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 清理日志按钮
        clear_btn = self.create_button(
            action_frame,
            "🗑️ 清理日志",
            self.clear_log,
            self.colors['warning'],
            self.colors['text_primary']
        )
        clear_btn.pack(side=tk.LEFT)

        # 签到操作卡片
        sign_card = self.create_card(parent, "签到操作")

        # 主要操作按钮
        primary_frame = tk.Frame(sign_card, bg=self.colors['bg_card'])
        primary_frame.pack(fill=tk.X, padx=10, pady=20)

        # 自动签到按钮
        auto_sign_btn = tk.Button(
            primary_frame,
            text="🚀 自动签到",
            command=self.auto_sign_thread,
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=30,
            pady=10
        )
        auto_sign_btn.pack(side=tk.LEFT, padx=5)

        # 调试按钮
        debug_btn = self.create_button(
            primary_frame,
            "🔧 调试Formhash",
            self.debug_formhash_thread,
            self.colors['bg_light'],
            self.colors['text_primary']
        )
        debug_btn.pack(side=tk.LEFT, padx=5)

        # 底部状态栏
        status_bar = tk.Frame(parent, bg=self.colors['bg_light'], height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label_bottom = tk.Label(
            status_bar,
            textvariable=self.status_var,
            font=("Microsoft YaHei", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary'],
            anchor=tk.W
        )
        self.status_label_bottom.pack(side=tk.LEFT, padx=10, pady=5)

        # 时间显示
        self.time_label = tk.Label(
            status_bar,
            font=("Microsoft YaHei", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary'],
            anchor=tk.E
        )
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # 更新时间显示
        self.update_time()

    def create_right_panel(self, parent):
        """创建右侧日志面板"""
        # 日志标题
        log_title_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=40)
        log_title_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            log_title_frame,
            text="操作日志",
            font=("Microsoft YaHei", 14, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=10)

        # 操作按钮
        log_buttons = tk.Frame(log_title_frame, bg=self.colors['bg_dark'])
        log_buttons.pack(side=tk.RIGHT, padx=10)

        # 导出日志按钮
        export_btn = self.create_button(
            log_buttons,
            "📤 导出日志",
            self.export_log,
            self.colors['bg_card'],
            self.colors['text_primary']
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        # 日志区域
        log_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief=tk.FLAT, bd=0)
        log_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=2,
            highlightthickness=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    def create_card(self, parent, title):
        """创建卡片式容器"""
        card = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['border']
        )
        card.pack(fill=tk.X, pady=5, padx=5)

        # 卡片标题
        tk.Label(
            card,
            text=title,
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(10, 5))

        return card

    def create_button(self, parent, text, command, bg_color, fg_color):
        """创建自定义样式按钮"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Microsoft YaHei", 10),
            bg=bg_color,
            fg=fg_color,
            activebackground=self.colors['accent_hover'],
            activeforeground=fg_color,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=6
        )
        return btn

    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"🕒 {current_time}")
        self.root.after(1000, self.update_time)

    def log(self, message, color=None):
        """添加日志到文本区域"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        if color is None:
            # 根据消息类型自动设置颜色
            if "✅" in message or "🎉" in message or "成功" in message:
                color = self.colors['success']
            elif "❌" in message or "失败" in message or "错误" in message:
                color = self.colors['error']
            elif "⚠️" in message or "警告" in message:
                color = self.colors['warning']
            elif "🚀" in message or "开始" in message:
                color = self.colors['accent']
            else:
                color = self.colors['text_primary']

        # 插入带格式的文本
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", f"message_{color}")

        # 应用标签格式
        self.log_text.tag_config("timestamp", foreground=self.colors['text_secondary'])
        self.log_text.tag_config(f"message_{color}", foreground=color)

        # 自动滚动到底部
        self.log_text.see(tk.END)

        # 更新状态栏
        short_message = message[:40] + "..." if len(message) > 40 else message
        self.status_var.set(short_message)

    def setup_logging(self):
        """设置日志输出"""
        self.log("=" * 50, self.colors['accent'])
        self.log("T00ls Auto-Sign - 现代化签到工具", self.colors['accent'])
        self.log("=" * 50, self.colors['accent'])
        self.log("")
        self.log("使用说明：", self.colors['text_primary'])
        self.log("1. 在Cookie框中输入从浏览器获取的Cookie", self.colors['text_secondary'])
        self.log("2. 点击【测试Cookie】验证Cookie是否有效", self.colors['text_secondary'])
        self.log("3. 点击【自动签到】完成签到", self.colors['text_secondary'])
        self.log("")
        self.log("欢迎使用！", self.colors['success'])

    def clear_log(self):
        """清理日志"""
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清理", self.colors['success'])

    def export_log(self):
        """导出日志到文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"t00ls_sign_log_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.log_text.get(1.0, tk.END))

            self.log(f"日志已导出到: {filename}", self.colors['success'])
            messagebox.showinfo("导出成功", f"日志已导出到:\n{filename}")
        except Exception as e:
            self.log(f"导出日志失败: {e}", self.colors['error'])
            messagebox.showerror("导出失败", f"导出日志失败: {e}")

    def save_config(self):
        """保存配置到文件"""
        try:
            config = {
                "cookie": self.cookie_var.get(),
            }

            with open("t00ls_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            self.log("配置已保存到 t00ls_config.json", self.colors['success'])
            messagebox.showinfo("保存成功", "配置已保存成功")
        except Exception as e:
            self.log(f"保存配置失败: {e}", self.colors['error'])
            messagebox.showerror("保存失败", f"保存配置失败: {e}")

    def load_config(self):
        """从配置文件加载数据"""
        try:
            if os.path.exists("t00ls_config.json"):
                with open("t00ls_config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)

                cookie = config.get("cookie", "")
                self.cookie_var.set(cookie)
                self.cookie_text.delete(1.0, tk.END)
                self.cookie_text.insert(1.0, cookie)

                self.log("配置已从文件加载", self.colors['success'])
        except Exception as e:
            self.log(f"加载配置失败: {e}", self.colors['error'])

    def load_config_dialog(self):
        """从对话框加载配置文件"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="选择配置文件",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )

            if filename:
                with open(filename, "r", encoding="utf-8") as f:
                    config = json.load(f)

                cookie = config.get("cookie", "")
                self.cookie_var.set(cookie)
                self.cookie_text.delete(1.0, tk.END)
                self.cookie_text.insert(1.0, cookie)

                self.log(f"配置已从 {filename} 加载", self.colors['success'])
                messagebox.showinfo("加载成功", "配置加载成功")
        except Exception as e:
            self.log(f"加载配置失败: {e}", self.colors['error'])
            messagebox.showerror("加载失败", f"加载配置失败: {e}")

    def get_cookie_help(self):
        """显示获取Cookie的帮助信息"""
        help_window = tk.Toplevel(self.root)
        help_window.title("如何获取Cookie")
        help_window.geometry("600x400")
        help_window.configure(bg=self.colors['bg_dark'])

        help_text = """
如何获取 T00ls Cookie:

[方法一：使用浏览器开发者工具]
1. 登录 T00ls 论坛 (https://www.t00ls.com)
2. 按 F12 打开开发者工具
3. 选择 Network (网络) 标签
4. 刷新页面或点击任意链接
5. 在请求中找到 checklogin.html 或任意请求
6. 查看 Request Headers (请求头) 中的 Cookie

[方法二：使用浏览器扩展]
1. 安装 EditThisCookie 或类似 Cookie 编辑扩展
2. 登录 T00ls 论坛
3. 点击扩展图标，找到 www.t00ls.com 的 Cookie
4. 复制 Cookie 字符串

📝 注意事项：
• Cookie 有有效期，过期后需要重新获取
• 不要分享你的 Cookie，它相当于你的登录凭证
• Cookie 格式类似于：xxxxxx_xxxx=xxxxxxxxx; xxxxxx_xxxx=xxxxxxxxx
        """

        text_widget = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0
        )
        text_widget.insert(1.0, help_text)
        text_widget.config(state="disabled")
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(
            help_window,
            text="关闭",
            command=help_window.destroy,
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            padx=20,
            pady=5
        ).pack(pady=10)

    # ============ 工具函数 ============
    def extract_username(self, content):
        """从响应中提取用户名"""
        # 尝试从 <span> 标签提取
        pattern = r'<span>([^<]+)</span>'
        match = re.search(pattern, content)
        if match:
            return match.group(1)

        # 尝试从个人资料链接提取
        pattern = r'members-profile-\d+\.html[^>]*>([^<]+)</a>'
        match = re.search(pattern, content)
        if match:
            return match.group(1)

        return None

    # ============ 核心功能（线程安全版本） ============
    def test_cookie_thread(self):
        """测试Cookie线程"""
        cookie_content = self.cookie_text.get(1.0, tk.END).strip()
        if not cookie_content:
            messagebox.showwarning("警告", "请输入Cookie")
            return

        thread = threading.Thread(target=self.test_cookie)
        thread.daemon = True
        thread.start()

    def test_cookie(self):
        """测试Cookie是否有效"""
        self.log("🚀 开始测试Cookie有效性...", self.colors['accent'])
        cookie = self.cookie_var.get().strip()

        headers = {
            'Host': 'www.t00ls.com',
            'Cookie': cookie,
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
                username = self.extract_username(content)

                if username:
                    self.username_var.set(username)
                    self.log(f"✅ Cookie有效，{username} 账号已登录", self.colors['success'])
                    messagebox.showinfo("测试成功", f"Cookie有效！\n用户名: {username}")
                elif '登录' in content and '退出' not in content:
                    self.log("❌ Cookie无效，显示登录链接", self.colors['error'])
                    messagebox.showerror("测试失败", "Cookie无效，请检查Cookie是否正确")
                else:
                    self.log("⚠️ 未知响应格式", self.colors['warning'])
                    messagebox.showwarning("警告", "无法解析响应，请尝试重新获取Cookie")
            else:
                self.log(f"❌ 请求失败，状态码: {response.status_code}", self.colors['error'])
                messagebox.showerror("请求失败", f"HTTP状态码: {response.status_code}")

        except Exception as e:
            self.log(f"❌ 测试Cookie失败: {e}", self.colors['error'])
            messagebox.showerror("测试失败", f"测试过程出错:\n{e}")

    def auto_sign_thread(self):
        """自动签到线程"""
        cookie_content = self.cookie_text.get(1.0, tk.END).strip()
        if not cookie_content:
            messagebox.showwarning("警告", "请输入Cookie")
            return

        thread = threading.Thread(target=self.auto_sign)
        thread.daemon = True
        thread.start()

    def auto_sign(self):
        """自动签到主流程"""
        self.log("🚀 开始自动签到流程...", self.colors['accent'])
        cookie = self.cookie_var.get().strip()

        # 1. 测试Cookie
        cookie_valid = False
        username = ""

        try:
            self.log("➡️ 验证Cookie...", self.colors['text_primary'])
            headers = {
                'Host': 'www.t00ls.com',
                'Cookie': cookie,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.t00ls.com/'
            }

            response = requests.get(
                'https://www.t00ls.com/checklogin.html',
                headers=headers,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                content = response.text
                username = self.extract_username(content)

                if username:
                    cookie_valid = True
                    self.username_var.set(username)
                    self.log(f"✅ Cookie有效，用户: {username}", self.colors['success'])
                else:
                    self.log("❌ Cookie无效", self.colors['error'])
                    messagebox.showerror("签到失败", "Cookie无效，请检查")
                    return
            else:
                self.log(f"❌ Cookie验证失败，状态码: {response.status_code}", self.colors['error'])
                messagebox.showerror("签到失败", f"Cookie验证失败\n状态码: {response.status_code}")
                return

        except Exception as e:
            self.log(f"❌ Cookie验证异常: {e}", self.colors['error'])
            messagebox.showerror("签到失败", f"Cookie验证异常:\n{e}")
            return

        # 2. 获取formhash
        self.log("➡️ 获取formhash...", self.colors['text_primary'])
        formhash = None

        try:
            response = requests.get(
                'https://www.t00ls.com/checklogin.html',
                headers=headers,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                content = response.text
                pattern = r'formhash=([a-f0-9]{8})'
                match = re.search(pattern, content)

                if match:
                    formhash = match.group(1)
                    self.log(f"✅ 找到formhash: {formhash}", self.colors['success'])
                else:
                    self.log("❌ 未找到formhash", self.colors['error'])
                    messagebox.showerror("签到失败", "无法获取formhash")
                    return
            else:
                self.log(f"❌ 获取formhash失败，状态码: {response.status_code}", self.colors['error'])
                messagebox.showerror("签到失败", f"获取formhash失败\n状态码: {response.status_code}")
                return

        except Exception as e:
            self.log(f"❌ 获取formhash异常: {e}", self.colors['error'])
            messagebox.showerror("签到失败", f"获取formhash异常:\n{e}")
            return

        # 3. 执行签到
        self.log("➡️ 执行签到...", self.colors['text_primary'])
        try:
            headers = {
                'Host': 'www.t00ls.com',
                'Cookie': cookie,
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

            response = requests.post(
                'https://www.t00ls.com/ajax-sign.json',
                headers=headers,
                data=data,
                verify=False,
                timeout=30
            )

            self.log(f"📤 请求状态码: {response.status_code}", self.colors['text_primary'])

            # 解析响应
            try:
                result = response.json()
                self.log(f"📄 响应: {str(result)[:100]}...", self.colors['text_primary'])

                if 'status' in result:
                    if result['status'] == 'success':
                        message = result.get('message', '签到成功')
                        self.sign_status_var.set("✅ 签到成功")
                        self.log(f"🎉 {message}", self.colors['success'])
                        messagebox.showinfo("签到成功", f"用户: {username}\n{message}")

                    elif result.get('message') == 'alreadysign':
                        self.sign_status_var.set("📝 今日已签到")
                        self.log("📝 今日已签到", self.colors['success'])
                        messagebox.showinfo("签到提醒", f"用户: {username}\n今日已签到")

                    else:
                        self.sign_status_var.set("❌ 签到失败")
                        self.log(f"❌ 签到失败: {result.get('message', '未知错误')}", self.colors['error'])
                        messagebox.showerror("签到失败", f"用户: {username}\n{result.get('message', '未知错误')}")

                else:
                    self.sign_status_var.set("⚠️ 未知响应")
                    self.log(f"⚠️ 未知响应格式: {str(result)[:100]}...", self.colors['warning'])
                    messagebox.showwarning("警告", f"未知响应格式:\n{str(result)[:200]}")

            except json.JSONDecodeError:
                self.log(f"❌ 非JSON响应: {response.text[:100]}", self.colors['error'])
                messagebox.showerror("响应错误", "服务器返回非JSON响应")

        except Exception as e:
            self.log(f"❌ 签到请求异常: {e}", self.colors['error'])
            messagebox.showerror("签到失败", f"签到请求异常:\n{e}")

    def debug_formhash_thread(self):
        """调试formhash线程"""
        cookie_content = self.cookie_text.get(1.0, tk.END).strip()
        if not cookie_content:
            messagebox.showwarning("警告", "请输入Cookie")
            return

        thread = threading.Thread(target=self.debug_formhash)
        thread.daemon = True
        thread.start()

    def debug_formhash(self):
        """调试获取formhash"""
        self.log("🔧 开始调试获取formhash...", self.colors['accent'])
        cookie = self.cookie_var.get().strip()

        headers = {
            'Host': 'www.t00ls.com',
            'Cookie': cookie,
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

            self.log(f"状态码: {response.status_code}", self.colors['text_primary'])

            content = response.text
            pattern = r'formhash=([a-f0-9]{8})'
            match = re.search(pattern, content)

            if match:
                self.log(f"✅ 找到formhash: {match.group(1)}", self.colors['success'])

                # 显示更多调试信息
                self.log("=== 调试信息 ===", self.colors['accent'])
                self.log(f"响应长度: {len(content)} 字符", self.colors['text_primary'])
                self.log(f"包含'formhash': {'formhash' in content}", self.colors['text_primary'])

                # 尝试找到formhash周围的上下文
                if match:
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 100)
                    context = content[start:end].replace('\n', ' ')
                    self.log(f"formhash上下文: ...{context}...", self.colors['text_secondary'])

            else:
                self.log("❌ 未找到formhash", self.colors['error'])
                self.log("=== 开始显示响应内容 ===", self.colors['accent'])
                # 限制显示长度
                if len(content) > 1000:
                    self.log(content[:500], self.colors['text_secondary'])
                    self.log("......(内容过长，已截断)......", self.colors['text_secondary'])
                    self.log(content[-500:], self.colors['text_secondary'])
                else:
                    self.log(content, self.colors['text_secondary'])

        except Exception as e:
            self.log(f"❌ 调试失败: {e}", self.colors['error'])

def main():
    """主函数"""
    root = tk.Tk()

    # 尝试设置tkinter主题
    try:
        root.tk.call('source', 'sun-valley.tcl')
        root.tk.call('set_theme', 'dark')
    except:
        pass

    # 创建应用实例
    app = ModernT00lsSignGUI(root)

    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 绑定快捷键
    root.bind('<Control-s>', lambda e: app.save_config())
    root.bind('<Control-l>', lambda e: app.clear_log())

    # 开始主循环
    root.mainloop()

if __name__ == "__main__":
    main()
