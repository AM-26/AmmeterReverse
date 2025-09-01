import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import time
import os
import datetime
from PIL import Image, ImageTk
import tempfile
import sys
from paddleocr import PaddleOCR
import re
import cv2
import pyperclip

class LDPlayerController:
    flag = 1
    runcount = 1
    def __init__(self, root):
        self.root = root
        self.root.title("雷电模拟器控制器")
        self.root.geometry("1920x1080")
        self.root.resizable(True, True)
        
        self.coord_font = ("Arial", 12, "bold")
        # 初始化变量
        self.image = None
        self.photo = None
        self.coords = []
        self.scale_factor = 1.0
        self.original_width = 1920
        self.original_height = 1080

        # 设置雷电模拟器ADB路径
        self.adb_path = r'D:\androidSim\leidian\LDPlayer9\adb.exe'
        
        # 截图保存目录
        self.screenshot_dir = r'D:\paddleOCR\pythonScreenShot'
        
        # 创建目录（如果不存在）
        if not os.path.exists(self.screenshot_dir):
            try:
                os.makedirs(self.screenshot_dir)
            except PermissionError:
                # 尝试在用户目录创建
                self.screenshot_dir = os.path.join(os.path.expanduser("~"), "pythonScreenShot")
                os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # 创建主框架
        self.create_widgets()
        
        # 检查ADB路径
        if not os.path.exists(self.adb_path):
            messagebox.showerror("错误", f"未找到ADB路径: {self.adb_path}")
        
        # 启动时自动连接设备
        self.connect_device()

    def create_widgets(self):
        # 创建标签页
        tab_control = ttk.Notebook(self.root)
        
        # 设备控制标签页
        device_tab = ttk.Frame(tab_control)
        tab_control.add(device_tab, text='设备控制')
        
        # 点击操作标签页
        click_tab = ttk.Frame(tab_control)
        tab_control.add(click_tab, text='点击操作')
        
        # 获取坐标标签页
        getpicref_tab = ttk.Frame(tab_control)
        tab_control.add(getpicref_tab, text='获取坐标')
        
        # 日志标签页
        log_tab = ttk.Frame(tab_control)
        tab_control.add(log_tab, text='操作日志')
        
        tab_control.pack(expand=1, fill="both")
        
        # 设备控制标签页内容
        device_frame = ttk.LabelFrame(device_tab, text="设备连接")
        device_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Button(device_frame, text="连接设备", command=self.connect_device).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(device_frame, text="断开设备", command=self.disconnect_device).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(device_frame, text="重启ADB服务", command=self.restart_adb).grid(row=0, column=2, padx=5, pady=5)
        
        self.device_status = tk.StringVar()
        self.device_status.set("设备状态: 未连接")
        ttk.Label(device_frame, textvariable=self.device_status).grid(row=1, column=0, columnspan=3, pady=5)
        
        # 设备信息显示
        info_frame = ttk.LabelFrame(device_tab, text="设备信息")
        info_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.device_info = scrolledtext.ScrolledText(info_frame, height=8)
        self.device_info.pack(padx=5, pady=5, fill="both", expand=True)
        self.device_info.config(state=tk.DISABLED)

        # 点击操作标签页内容
        click_frame = ttk.LabelFrame(click_tab, text="点击设置")
        click_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(click_frame, text="X坐标:").grid(row=0, column=0, padx=5, pady=5)
        self.x_entry = ttk.Entry(click_frame, width=8)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5)
        self.x_entry.insert(0, "500")
        
        ttk.Label(click_frame, text="Y坐标:").grid(row=0, column=2, padx=5, pady=5)
        self.y_entry = ttk.Entry(click_frame, width=8)
        self.y_entry.grid(row=0, column=3, padx=5, pady=5)
        self.y_entry.insert(0, "500")
        
        ttk.Label(click_frame, text="点击次数:").grid(row=0, column=4, padx=5, pady=5)
        self.click_count_entry = ttk.Entry(click_frame, width=8)
        self.click_count_entry.grid(row=0, column=5, padx=5, pady=5)
        self.click_count_entry.insert(0, "1")
        
        ttk.Label(click_frame, text="间隔(秒):").grid(row=0, column=6, padx=5, pady=5)
        self.interval_entry = ttk.Entry(click_frame, width=8)
        self.interval_entry.grid(row=0, column=7, padx=5, pady=5)
        self.interval_entry.insert(0, "1")
        
        ttk.Button(click_frame, text="单次点击", command=self.single_click).grid(row=0, column=8, padx=5, pady=5)
        ttk.Button(click_frame, text="连续点击", command=self.multi_click).grid(row=0, column=9, padx=5, pady=5)

        # 截图功能标签页内容
        #screenshot_frame = ttk.Frame(screenshot_tab)
        #screenshot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 第二排按钮区域
        click2_frame = ttk.LabelFrame(click_tab, text="截图测试")
        click2_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 控制按钮区域
        btn_frame = ttk.Frame(click2_frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="截取屏幕", command=self.capture_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存截图", command=self.save_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="刷新", command=self.refresh_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="OCR", command=self.targetOCR).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="电表倒转", command=self.ammeterReverse).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="源石锭", command=self.multiMoney).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="烛火", command=self.fire).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="收藏品", command=self.multiCollection).pack(side=tk.LEFT, padx=5)

        ttk.Label(btn_frame, text="令节点X坐标:").pack(side=tk.LEFT, padx=5)
        self.ling_x_entry = ttk.Entry(btn_frame, width=8)
        self.ling_x_entry.pack(side=tk.LEFT, padx=5)
        self.ling_x_entry.insert(0, "540")
        
        ttk.Label(btn_frame, text="令节点Y坐标:").pack(side=tk.LEFT, padx=5)
        self.ling_y_entry = ttk.Entry(btn_frame, width=8)
        self.ling_y_entry.pack(side=tk.LEFT, padx=5)
        self.ling_y_entry.insert(0, "370")

        ttk.Label(btn_frame, text="运行次数:(电表倒转模式下为每次获取烛火对应的源石锭获取次数)").pack(side=tk.LEFT, padx=5)
        self.runcount_entry = ttk.Entry(btn_frame, width=8)
        self.runcount_entry.pack(side=tk.LEFT, padx=5)
        self.runcount_entry.insert(0, "1")
        
        # 截图显示区域
        self.screenshot_frame = ttk.LabelFrame(click2_frame, text="当前截图")
        self.screenshot_frame.pack(fill="both", expand=True)
        
        self.screenshot_label = tk.Label(self.screenshot_frame, text="点击[截取屏幕]按钮获取截图", bg="#f0f0f0")
        self.screenshot_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 截图信息
        self.screenshot_info = tk.StringVar()
        self.screenshot_info.set("截图信息: 未截取")
        ttk.Label(click2_frame, textvariable=self.screenshot_info).pack(pady=5)

         # 图片显示区域
        #self.canvas_frame = ttk.LabelFrame(click2_frame, text="当前截图")
        #self.canvas_frame = ttk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        #self.canvas_frame.pack(fill=ttk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 创建画布
        #self.canvas = ttk.Canvas(self.canvas_frame, bg="#34495e", bd=0, highlightthickness=0)
        #self.canvas.pack(fill=ttk.BOTH, expand=True)
        
        # 状态栏
        #self.status_var = ttk.StringVar(value="就绪 - 请加载一张1920×1080的图片")
        #status_bar = ttk.Label(self.root, textvariable=self.status_var, bd=1, relief=ttk.SUNKEN, 
        #                    anchor=ttk.W, bg="#e0e0e0", fg="#333", padx=10)
        #status_bar.pack(side=ttk.BOTTOM, fill=ttk.X)
        
        # 绑定事件
        #self.canvas.bind("<Button-1>", self.on_canvas_click)
        #self.canvas.bind("<Motion>", self.on_canvas_motion)

        #获取坐标标签页内容
        getpicref_frame = ttk.LabelFrame(getpicref_tab, text="1920×1080 图片坐标获取工具")
        getpicref_frame.pack(padx=10, pady=10, fill="x")
        # 加载图片按钮
        ttk.Button(getpicref_frame, text="加载图片", command=self.load_image).pack(side=tk.LEFT, padx=5)
        # 坐标显示
        coord_frame = tk.Frame(getpicref_frame, bg="#e3f2fd", bd=1, relief=tk.SUNKEN)
        coord_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(coord_frame, text="当前坐标:", bg="#e3f2fd", padx=5).pack(side=tk.LEFT)
        self.coord_label = tk.Label(coord_frame, text="(X, Y)", font=self.coord_font, 
                                  bg="#e3f2fd", fg="#d32f2f", width=15)
        self.coord_label.pack(side=tk.LEFT, padx=5)
        # 图片显示区域
        canvas_frame = tk.Frame(getpicref_tab, bg="#2c3e50", padx=10, pady=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        # 创建画布
        self.canvas = tk.Canvas(canvas_frame, bg="#34495e", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)     
        # 状态栏
        self.status_var = tk.StringVar(value="就绪 - 请加载一张1920×1080的图片")
        status_bar = tk.Label(getpicref_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                            anchor=tk.W, bg="#e0e0e0", fg="#333", padx=10)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)        
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        
        # 日志标签页内容
        log_frame = ttk.LabelFrame(log_tab, text="操作日志")
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.log_text.config(state=tk.DISABLED)

    def load_image(self):
        file_path = self.current_screenshot
        
        if not file_path:
            return
            
        try:
            # 打开图片
            self.image = Image.open(file_path)
            img_width, img_height = self.image.size
            
            # 检查图片尺寸
            if img_width != self.original_width or img_height != self.original_height:
                self.status_var.set(f"警告: 图片尺寸为 {img_width}x{img_height} (应为1920x1080)")
            else:
                self.status_var.set("已加载1920x1080图片")
            
            # 计算缩放比例以适应画布
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width < 10 or canvas_height < 10:  # 初始大小可能为1
                canvas_width = 900
                canvas_height = 500
            
            width_ratio = canvas_width / img_width
            height_ratio = canvas_height / img_height
            self.scale_factor = min(width_ratio, height_ratio)
            
            # 缩放图片
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
            
            # 显示图片
            self.photo = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # 重置坐标
            self.coord_label.config(text="(X, Y)")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")
            self.status_var.set("图片加载失败")

    def on_canvas_click(self, event):
        #if not self.image:
        #    messagebox.showwarning("警告", "请先加载图片")
        #    return
            
        # 计算原始坐标 (1920x1080)
        x = int(event.x / self.scale_factor)
        y = int(event.y / self.scale_factor)
        
        # 确保坐标在范围内
        x = max(0, min(x, self.original_width - 1))
        y = max(0, min(y, self.original_height - 1))
        
        # 显示坐标
        self.coord_label.config(text=f"({x}, {y})")
        
        # 保存坐标历史
        self.coords.append((x, y))
        if len(self.coords) > 10:  # 只保留最近10个
            self.coords.pop(0)
            
        # 在图片上标记点击位置
        self.canvas.delete("marker")
        radius = 5
        self.canvas.create_oval(
            event.x - radius, event.y - radius,
            event.x + radius, event.y + radius,
            outline="red", width=2, tags="marker"
        )
        self.canvas.create_line(
            event.x - radius*2, event.y,
            event.x + radius*2, event.y,
            fill="red", width=1, tags="marker"
        )
        self.canvas.create_line(
            event.x, event.y - radius*2,
            event.x, event.y + radius*2,
            fill="red", width=1, tags="marker"
        )
        
        self.status_var.set(f"已捕获坐标: ({x}, {y}) - 点击复制按钮复制坐标")
        self.ling_x_entry.delete(0,tk.END)
        self.ling_x_entry.insert(0,str(x))
        self.ling_y_entry.delete(0,tk.END)
        self.ling_y_entry.insert(0,str(y))
    
    def on_canvas_motion(self, event):
        if not self.image:
            return
            
        # 计算原始坐标 (1920x1080)
        x = int(event.x / self.scale_factor)
        y = int(event.y / self.scale_factor)
        
        # 确保坐标在范围内
        x = max(0, min(x, self.original_width - 1))
        y = max(0, min(y, self.original_height - 1))
        
        # 更新状态栏显示坐标
        self.status_var.set(f"当前位置: ({x}, {y}) - 点击获取坐标")

    def log_message(self, message):
        """添加日志消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def run_adb_command(self, *args):
        """执行ADB命令并返回结果"""
        try:
            cmd = [self.adb_path] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return result.stdout.strip()
        except Exception as e:
            self.log_message(f"执行命令出错: {str(e)}")
            return ""
    
    def connect_device(self):
        """连接设备"""
        def connect_thread():
            self.log_message("正在连接设备...")
            
            # 启动ADB服务
            self.run_adb_command("start-server")
            
            # 获取设备列表
            devices_output = self.run_adb_command("devices")
            
            if "List of devices attached" in devices_output:
                lines = devices_output.splitlines()[1:]
                devices = [line.split('\t')[0] for line in lines if '\tdevice' in line]
                
                if devices:
                    self.device_status.set(f"设备状态: 已连接 ({len(devices)}个设备)")
                    self.log_message(f"已连接设备: {', '.join(devices)}")
                    
                    # 获取设备信息
                    self.get_device_info()
                else:
                    self.device_status.set("设备状态: 未检测到设备")
                    self.log_message("未检测到任何设备，请确保模拟器已启动")
            else:
                self.device_status.set("设备状态: 连接失败")
                self.log_message("无法获取设备列表")
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect_device(self):
        """断开设备连接"""
        self.run_adb_command("kill-server")
        self.device_status.set("设备状态: 已断开")
        self.log_message("已断开设备连接")
        
        # 清空设备信息
        self.device_info.config(state=tk.NORMAL)
        self.device_info.delete(1.0, tk.END)
        self.device_info.config(state=tk.DISABLED)
        
        # 清空截图
        self.screenshot_label.config(image='', text="设备已断开")
        self.screenshot_info.set("截图信息: 设备已断开")
    
    def restart_adb(self):
        """重启ADB服务"""
        self.disconnect_device()
        time.sleep(1)
        self.connect_device()
    
    def get_device_info(self):
        """获取设备信息"""
        def info_thread():
            self.log_message("正在获取设备信息...")
            
            # 获取设备型号
            model = self.run_adb_command("shell", "getprop", "ro.product.model")
            
            # 获取Android版本
            android_version = self.run_adb_command("shell", "getprop", "ro.build.version.release")
            
            # 获取屏幕分辨率
            screen_size = self.run_adb_command("shell", "wm", "size")
            
            # 获取CPU信息
            cpu_info = self.run_adb_command("shell", "cat", "/proc/cpuinfo")
            cpu_model = next((line.split(':')[1].strip() for line in cpu_info.splitlines() if "model name" in line), "未知")
            
            # 获取内存信息
            mem_info = self.run_adb_command("shell", "cat", "/proc/meminfo")
            total_mem = next((line.split(':')[1].strip() for line in mem_info.splitlines() if "MemTotal" in line), "未知")
            
            # 显示设备信息
            info_text = f"设备型号: {model}\n"
            info_text += f"Android版本: {android_version}\n"
            info_text += f"屏幕分辨率: {screen_size}\n"
            info_text += f"CPU型号: {cpu_model}\n"
            info_text += f"内存大小: {total_mem}\n"
            
            self.device_info.config(state=tk.NORMAL)
            self.device_info.delete(1.0, tk.END)
            self.device_info.insert(tk.END, info_text)
            self.device_info.config(state=tk.DISABLED)
            
            self.log_message("设备信息获取完成")
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def tap(self, x, y):
        """执行点击操作"""
        try:
            result = self.run_adb_command("shell", "input", "tap", str(x), str(y))
            if not result:
                return True
            return False
        except:
            return False
    
    def single_click(self):
        """执行单次点击"""
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            
            if self.tap(x, y):
                self.log_message(f"点击成功: ({x}, {y})")
            else:
                self.log_message(f"点击失败: ({x}, {y})")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的坐标值")
    
    def multi_click(self):
        """执行连续点击"""
        def click_thread():
            try:
                x = int(self.x_entry.get())
                y = int(self.y_entry.get())
                count = int(self.click_count_entry.get())
                interval = float(self.interval_entry.get())
                
                if count <= 0:
                    messagebox.showerror("输入错误", "点击次数必须大于0")
                    return
                
                if interval < 0.1:
                    messagebox.showerror("输入错误", "间隔时间不能小于0.1秒")
                    return
                
                for i in range(count):
                    if self.tap(x, y):
                        self.log_message(f"点击 {i+1}/{count}: ({x}, {y})")
                    else:
                        self.log_message(f"点击 {i+1}/{count} 失败")
                    
                    time.sleep(interval)
                
                self.log_message(f"完成 {count} 次点击")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数值")
        
        threading.Thread(target=click_thread, daemon=True).start()
    
    def capture_screenshot(self):
        """截取设备屏幕 - 修复版本"""
        def capture_thread():
            try:
                self.log_message("正在截取屏幕...")
                
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_path = temp_file.name
                
                # 修复的截图命令 - 使用screencap和重定向
                cmd = f'"{self.adb_path}" exec-out screencap -p > "{temp_path}"'
                
                # 在Windows上使用shell执行
                process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
                
                if process.returncode != 0:
                    error_msg = stderr.decode("utf-8", errors="ignore")
                    self.log_message(f"截图失败: {error_msg}")
                    self.screenshot_label.config(text=f"截图失败: {error_msg}")
                    return
                
                # 检查文件是否存在
                if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                    self.log_message("截图失败：未生成截图文件")
                    self.screenshot_label.config(text="截图失败：文件为空")
                    return
                
                # 加载图片
                try:
                    img = Image.open(temp_path)
                except Exception as e:
                    self.log_message(f"无法加载截图: {str(e)}")
                    self.screenshot_label.config(text=f"无法加载截图: {str(e)}")
                    return
                
                # 调整图片大小以适应显示区域
                max_width = self.screenshot_frame.winfo_width() - 20
                max_height = self.screenshot_frame.winfo_height() - 50
                
                # 如果窗口大小尚未确定，使用默认值
                if max_width <= 10 or max_height <= 10:
                    max_width = 600
                    max_height = 400
                
                if img.width > max_width or img.height > max_height:
                    ratio = min(max_width / img.width, max_height / img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.LANCZOS)
                
                # 转换为Tkinter PhotoImage
                self.screenshot_img = ImageTk.PhotoImage(img)
                
                # 更新UI
                self.screenshot_label.config(image=self.screenshot_img, text="")
                self.screenshot_label.image = self.screenshot_img  # 保持引用
                
                # 更新截图信息
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                self.screenshot_info.set(f"截图信息: {img.width}×{img.height} | 时间: {timestamp}")
                
                self.log_message(f"截图成功: {img.width}×{img.height}")
                
                # 保存截图路径
                self.current_screenshot = temp_path
                
            except Exception as e:
                self.log_message(f"截图失败: {str(e)}")
                self.screenshot_label.config(image='', text=f"截图失败: {str(e)}")
        
        threading.Thread(target=capture_thread, daemon=True).start()
    
    def save_screenshot(self):
        """保存截图到文件"""
        if not hasattr(self, 'current_screenshot') or not os.path.exists(self.current_screenshot):
            messagebox.showwarning("保存截图", "没有可用的截图")
            return
        
        try:
            # 生成文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"screenshot_{timestamp}.png"
            default_path = os.path.join(self.screenshot_dir, default_filename)
            
            # 弹出保存对话框
            file_path = filedialog.asksaveasfilename(
                initialdir=self.screenshot_dir,
                initialfile=default_filename,
                defaultextension=".png",
                filetypes=[("PNG图片", "*.png"), ("所有文件", "*.*")]
            )
            
            if file_path:
                # 保存文件
                import shutil
                shutil.copy(self.current_screenshot, file_path)
                self.log_message(f"截图已保存: {file_path}")
                messagebox.showinfo("保存成功", f"截图已保存到:\n{file_path}")
        except Exception as e:
            self.log_message(f"保存截图失败: {str(e)}")
            messagebox.showerror("保存失败", f"保存截图时出错:\n{str(e)}")

    def OCR(self):
        self.getPic()
        # 初始化 PaddleOCR 实例
        ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False)
        # 对示例图像执行 OCR 推理 
        res = ocr.predict(
            input=self.current_screenshot)
        
        # 手动删除临时文件
        try:
            os.remove(self.current_screenshot)
            print(f"已删除临时文件: {self.current_screenshot}")
        except OSError as e:
            print(f"删除临时文件失败: {e}")

        # 遍历所有 OCR 结果项
        for item in res:
            # 检查是否包含 'rec_texts' 键
            if 'rec_texts' in item:
                texts = item['rec_texts']
                print(f"找到文本列表: {texts}")
        return res        

    def targetOCR(self):
        # 初始化 PaddleOCR 实例
        ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False)
        # 1. 读取图像
        image = cv2.imread(self.current_screenshot)  # 替换为你的图片路径

        # 手动删除临时文件
        try:
            os.remove(self.current_screenshot)
            print(f"已删除临时文件: {self.current_screenshot}")
        except OSError as e:
            print(f"删除临时文件失败: {e}")

        # 2. 定义四个顶点坐标 (按顺序：左上、右上、右下、左下)
        points = [
            (1700, 100),   # 左上
            (1870, 100),   # 右上
            (1870, 270),   # 右下
            (1700, 270)    # 左下
        ]
        # 3. 计算裁剪区域的边界
        x_min = min(p[0] for p in points)  # 最左边的x坐标
        y_min = min(p[1] for p in points)  # 最上边的y坐标
        x_max = max(p[0] for p in points)  # 最右边的x坐标
        y_max = max(p[1] for p in points)  # 最下边的y坐标
        # 4. 裁剪图像 (注意：OpenCV使用[y:y+h, x:x+w]格式)
        cropped = image[y_min:y_max, x_min:x_max]

        # 5. 保存结果 (保存在当前目录)
        cv2.imwrite('cropped_region.jpg', cropped)
        # 对示例图像执行 OCR 推理 
        res = ocr.predict(
            input='cropped_region.jpg')

        # 处理 PaddleX OCRResult 对象
        print(f"结果类型: {type(res)}")
        if len(res) > 0:
            print(f"第一项类型: {type(res[0])}")
            
            # 打印第一项的所有键
            print("第一项的键:", list(res[0].keys()))
            
            # 尝试访问可能的文本键
            for possible_key in ['text', 'rec_texts', 'label', 'result', 'content']:
                if possible_key in res[0]:
                    print(f"找到键 '{possible_key}': {res[0][possible_key]}")

        # 提取数字的正整数
        result = None

        # 遍历所有 OCR 结果项
        for item in res:
            # 检查是否包含 'rec_texts' 键
            if 'rec_texts' in item:
                texts = item['rec_texts']
                print(f"找到文本列表: {texts}")
                
                # 遍历所有识别文本
                for text in texts:
                    # 尝试直接转换为整数
                    try:
                        num = int(text)
                        if num > 0:  # 确保是正整数
                            result = num
                            print(f"找到数字: {result} (直接转换)")
                            break  # 找到后跳出内部循环
                    except ValueError:
                        # 如果不是纯数字，尝试提取数字部分
                        if any(char.isdigit() for char in text):
                            # 提取数字字符并组合
                            digits = ''.join(filter(str.isdigit, text))
                            if digits:
                                result = int(digits)
                                print(f"找到数字: {result} (从文本提取)")
                                break  # 找到后跳出内部循环
                
                # 如果已找到数字，提前结束
                if result is not None:
                    break  # 找到后跳出外部循环

        # 最终结果
        if result is not None:
            print(f"最终提取的数字: {result} (类型: {type(result)})")
            self.x_entry.delete(0, "end")
            self.x_entry.insert(0, str(result))
        else:
            print("警告: 未在OCR结果中找到任何数字")
    
    def getPic(self):
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_path = temp_file.name
        #临时文件目录 需手动删除
        print(f"创建的临时文件: {temp_path}")
        # 修复的截图命令 - 使用screencap和重定向
        cmd = f'"{self.adb_path}" exec-out screencap -p > "{temp_path}"'
        
        # 在Windows上使用shell执行
        process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode("utf-8", errors="ignore")
            self.log_message(f"截图失败: {error_msg}")
            self.screenshot_label.config(text=f"截图失败: {error_msg}")
            return
        
        # 检查文件是否存在
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            self.log_message("截图失败：未生成截图文件")
            self.screenshot_label.config(text="截图失败：文件为空")
            return
        
        # 加载图片
        try:
            img = Image.open(temp_path)
        except Exception as e:
            self.log_message(f"无法加载截图: {str(e)}")
            self.screenshot_label.config(text=f"无法加载截图: {str(e)}")
            return
        
        # 转换为Tkinter PhotoImage
        self.screenshot_img = ImageTk.PhotoImage(img)

        # 保存截图路径
        self.current_screenshot = temp_path

    def ammeterReverse(self):  
        counter = 0      
        self.runcount = int(self.runcount_entry.get())       
        while(self.flag):
            counter += 1
            tempcount = self.runcount
            while(tempcount):
                tempcount -= 1
                self.money()
                print("第%d"%(counter)+"轮第%d"%(self.runcount-tempcount)+"次money结束")
                time.sleep(3)
            self.fire()
            print("第%d"%(counter)+"轮fire结束")
            time.sleep(5)
        print("第%d"%(counter)+"轮fail\n")
        return 

    def enterChangle(self):
        ling_x = int(self.ling_x_entry.get())
        ling_y = int(self.ling_y_entry.get())
        time.sleep(3)
        self.tap(ling_x,ling_y)
        print("选择常乐,坐标为（%d,%d）\n"%(ling_x,ling_y))
        time.sleep(1)
        self.tap(1730,830)
        print("进入常乐\n")
        time.sleep(4)
        #self.tap(500,400)
        #print("吸收\n")
        time.sleep(6)

    def secondChance(self):
        res = self.OCR()
        # 提取文字
        result = None

        # 遍历所有 OCR 结果项
        for item in res:
            # 检查是否包含 'rec_texts' 键
            if 'rec_texts' in item:
                texts = item['rec_texts']
                print(f"找到文本列表: {texts}")
                
                # 遍历所有识别文本
                for text in texts:
                    # 尝试直接转换为整数
                    try:
                        #num = int(text)
                        if text == '来就来':  # 确保是正整数
                            result = 1
                            print(f"找到来就来")
                            break  # 找到后跳出内部循环
                    except ValueError:
                        print(f"valueError:Line 638\n")
                
                # 如果已找到数字，提前结束
                if result is not None:
                    break  # 找到后跳出外部循环

        # 最终结果
        if result is not None:
            print(f"second chance\n")
            return 1
        else:
            print(f"no second chance\n")
            return 0    
    
    def dealwithFailure(self):
        self.tap(960,970)
        print("确认失败\n")
        time.sleep(5)
        #self.tap(510,510)
        #print("吸收\n")
        time.sleep(5)
        self.tap(1800,560)
        print("选择倒霉啊\n")
        time.sleep(2)
        self.tap(1780,580)
        print("确认倒霉啊\n")
        time.sleep(10)
        if(self.secondChance()):
            self.tap(1790,440)
            print("选择来就来\n")
            time.sleep(2)
            self.tap(1790,440)
            print("确认来就来\n")
            time.sleep(10)
            self.tap(1800,570)
            print("选中厉如锋\n")
            time.sleep(1)  
            self.tap(1800,570)
            print("点击厉如锋\n")
            time.sleep(6)
            if(self.fireSuccess()):
                self.tap(960,960)
                print("确认")
                time.sleep(5)
                #self.tap(500,400)
                #print("吸收\n")
                time.sleep(4)
                self.tap(1790,820)
                print("选中烛火")
                time.sleep(1)
                self.tap(1790,820)
                print("点击烛火")
                time.sleep(6)
                self.tap(960,990)
                print("结束fire")
            else:
                print("uncanny continuous failure\n")
                time.sleep(2)
                self.tap(960,960)
                print("确认连续两次失败")
                time.sleep(10)
                self.tap(1800,560)
                print("选择倒霉啊\n")
                time.sleep(2)
                self.tap(1780,580)
                print("确认倒霉啊\n")
                time.sleep(10)
                self.tap(960,980)
                print("确认返回主页\n")
                time.sleep(5)
                #self.flag = 0
        else:
            self.tap(960,980)
            print("确认返回主页")
            time.sleep(5)

    def multiMoney(self):
        count = int(self.runcount_entry.get())
        tempcount = count
        print("重复次数：%d\n"%count)
        while(count):
            self.money()
            time.sleep(2)
            count -= 1
            print("第%d"%(tempcount-count)+"次money结束\n")

    def multiCollection(self):
        count = int(self.runcount_entry.get())
        tempcount = count
        print("重复次数：%d\n"%count)
        while(count):
            self.collection()
            time.sleep(2)
            count -= 1
            print("第%d"%(tempcount-count)+"次collection结束\n")

    def money(self):
        self.enterChangle()
        self.tap(1790,430)
        print("选中消耗50源石锭\n")
        time.sleep(1)
        self.tap(1790,430)
        print("点击消耗50源石锭\n")
        time.sleep(5)
        #self.tap(500,400)
        #print("吸收\n")
        time.sleep(4)
        self.tap(1800,300)
        print("选中衡如常\n")
        time.sleep(2)  
        self.tap(1800,300)
        print("点击衡如常\n")
        time.sleep(6)
        if(self.moneySuccess()):
            self.tap(960,960)
            print("确认\n")
            time.sleep(5)
            #self.tap(500,400)
            #print("吸收\n")
            time.sleep(8)
            self.tap(1790,570)
            print("选中获得65源石锭\n")
            time.sleep(1)
            self.tap(1790,570)
            print("点击获得65源石锭\n")
            time.sleep(6)
            self.tap(960,990)
            print("结束money\n")
        else:
            print("money failure\n")
            self.dealwithFailure()
            

    def fire(self):
        self.enterChangle()
        self.tap(1790,430)
        print("选中消耗50源石锭\n")
        time.sleep(1)
        self.tap(1790,430)
        print("点击消耗50源石锭\n")
        time.sleep(5)
        #self.tap(500,400)
        #print("吸收\n")
        time.sleep(4)
        self.tap(1800,570)
        print("选中厉如锋\n")
        time.sleep(1)  
        self.tap(1800,570)
        print("点击厉如锋\n")
        time.sleep(6)
        if(self.fireSuccess()):
            self.tap(960,960)
            print("确认")
            time.sleep(5)
            #self.tap(500,400)
            #print("吸收\n")
            time.sleep(8)
            self.tap(1790,820)
            print("选中烛火")
            time.sleep(1)
            self.tap(1790,820)
            print("点击烛火")
            time.sleep(6)
            self.tap(960,990)
            print("结束fire")
        else:
            print("fire failure\n")
            self.dealwithFailure()
    
    def collection(self):
        self.enterChangle()
        self.tap(1790,430)
        print("选中消耗50源石锭\n")
        time.sleep(1)
        self.tap(1790,430)
        print("点击消耗50源石锭\n")
        time.sleep(5)
        #self.tap(500,400)
        #print("吸收\n")
        time.sleep(4)
        self.tap(1800,570)
        print("选中厉如锋\n")
        time.sleep(1)  
        self.tap(1800,570)
        print("点击厉如锋\n")
        time.sleep(6)
        if(self.fireSuccess()):
            self.tap(960,960)
            print("确认")
            time.sleep(5)
            #self.tap(500,400)
            #print("吸收\n")
            time.sleep(4)
            self.tap(1790,330)
            print("选中收藏品")
            time.sleep(1)
            self.tap(1790,330)
            print("点击收藏品")
            time.sleep(3)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(1)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(1)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(1)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(1)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(1)
            self.tap(980,824)
            print("确认收藏品\n")
            time.sleep(2)
            self.tap(960,990)
            print("结束collection")
        else:
            print("collection failure\n")
            self.dealwithFailure()
    
    def moneySuccess(self):
        #self.getPic()
        res = self.OCR()
        # 提取文字
        result = None

        # 遍历所有 OCR 结果项
        for item in res:
            # 检查是否包含 'rec_texts' 键
            if 'rec_texts' in item:
                texts = item['rec_texts']
                print(f"找到文本列表: {texts}")
                
                # 遍历所有识别文本
                for text in texts:
                    # 尝试直接转换为整数
                    try:
                        #num = int(text)
                        if text == '获得了65源石锭':  # 确保是正整数
                            result = 1
                            print(f"获得了65源石锭")
                            break  # 找到后跳出内部循环
                    except ValueError:
                        print(f"valueError:Line 638\n")
                
                # 如果已找到数字，提前结束
                if result is not None:
                    break  # 找到后跳出外部循环

        # 最终结果
        if result is not None:
            print(f"moneySuccess")
            return 1
        else:
            print(f"moneyFailure")
            return 0

    def fireSuccess(self):
        #self.getPic()
        res = self.OCR()
        # 提取文字
        result = None

        # 遍历所有 OCR 结果项
        for item in res:
            # 检查是否包含 'rec_texts' 键
            if 'rec_texts' in item:
                texts = item['rec_texts']
                print(f"找到文本列表: {texts}")
                
                # 遍历所有识别文本
                for text in texts:
                    # 尝试直接转换为整数
                    try:
                        #num = int(text)
                        if text == '获得了自选奖励':  # 确保是正整数
                            result = 1
                            print(f"获得了烛火")
                            break  # 找到后跳出内部循环
                    except ValueError:
                        print(f"valueError:Line 673\n")
                
                # 如果已找到数字，提前结束
                if result is not None:
                    break  # 找到后跳出外部循环

        # 最终结果
        if result is not None:
            print(f"fireSuccess")
            return 1
        else:
            print("fireFailure")
            return 0

    def refresh_screenshot(self):
        """刷新截图显示"""
        if hasattr(self, 'current_screenshot') and os.path.exists(self.current_screenshot):
            try:
                # 加载图片
                img = Image.open(self.current_screenshot)
                
                # 调整图片大小以适应显示区域
                max_width = self.screenshot_frame.winfo_width() - 20
                max_height = self.screenshot_frame.winfo_height() - 50
                
                # 如果窗口大小尚未确定，使用默认值
                if max_width <= 10 or max_height <= 10:
                    max_width = 600
                    max_height = 400
                
                if img.width > max_width or img.height > max_height:
                    ratio = min(max_width / img.width, max_height / img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.LANCZOS)
                
                # 转换为Tkinter PhotoImage
                self.screenshot_img = ImageTk.PhotoImage(img)
                
                # 更新UI
                self.screenshot_label.config(image=self.screenshot_img)
                self.screenshot_label.image = self.screenshot_img  # 保持引用
                
                self.log_message("截图已刷新")
            except Exception as e:
                self.log_message(f"刷新截图失败: {str(e)}")
        else:
            messagebox.showinfo("刷新截图", "没有可用的截图")
if __name__ == "__main__":
    root = tk.Tk()
    app = LDPlayerController(root)
    #root.after(200, app.update_grid)  # 定期更新网格
    root.mainloop()    