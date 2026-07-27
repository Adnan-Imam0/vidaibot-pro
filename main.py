#!/usr/bin/env python3
"""
VidaiBot Pro - Professional YouTube View Booster with GUI
Advanced anti-detection system with multiple evasion techniques
"""

import sys
import os
import time
import random
import threading
import urllib.parse
from datetime import datetime
from typing import List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import winreg

# Third-party imports
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

# ==================== CONFIGURATION ====================
APP_NAME = "VidaiBot Pro"
APP_VERSION = "2.0.0"
MAX_THREADS = 10

# Anti-detection settings
ROTATE_USER_AGENT = True
RANDOM_MOUSE_MOVEMENTS = True
RANDOM_SCROLLING = True
RANDOM_PAUSES = True
LIKE_PROBABILITY = 0.3
SUBSCRIBE_PROBABILITY = 0.05

# ==================== END CONFIGURATION ====================

class ChromeVersionManager:
    """Manage Chrome version detection and ChromeDriver compatibility"""
    
    @staticmethod
    def get_chrome_version():
        """Get installed Chrome version"""
        try:
            # Try to get from registry
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version = winreg.QueryValueEx(key, "version")[0]
                winreg.CloseKey(key)
                return version
            except:
                pass
            
            # Try alternative registry location
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Google\Update\Clients\{8A69D345-D564-463C-AFF1-A69D9E530F96}")
                version = winreg.QueryValueEx(key, "pv")[0]
                winreg.CloseKey(key)
                return version
            except:
                pass
            
            # Try to get from Chrome executable
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    result = subprocess.run([path, '--version'], capture_output=True, text=True)
                    if result.returncode == 0:
                        version = result.stdout.strip().split()[-1]
                        return version
            
            return None
        except:
            return None
    
    @staticmethod
    def get_major_version(version):
        """Extract major version number"""
        if version:
            return int(version.split('.')[0])
        return None


class AntiDetectionSystem:
    """Advanced anti-detection system"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        ]
        self.proxy_list = []
        self.current_proxy_index = 0
    
    def get_random_user_agent(self):
        return random.choice(self.user_agents)
    
    def get_proxy(self):
        if not self.proxy_list:
            return None
        proxy = self.proxy_list[self.current_proxy_index % len(self.proxy_list)]
        self.current_proxy_index += 1
        return proxy
    
    def load_proxies_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                proxies = f.read().strip().split('\n')
                self.proxy_list = [p.strip() for p in proxies if p.strip()]
            return len(self.proxy_list)
        except:
            return 0
    
    def get_chrome_options(self, use_proxy=False):
        options = uc.ChromeOptions()
        
        # Random user agent
        if ROTATE_USER_AGENT:
            options.add_argument(f'--user-agent={self.get_random_user_agent()}')
        
        # Anti-detection arguments
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        
        # Random window size
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f'--window-size={width},{height}')
        
        # Proxy if enabled
        if use_proxy and self.proxy_list:
            proxy = self.get_proxy()
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
        
        return options
    
    def apply_stealth_scripts(self, driver):
        scripts = [
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """,
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            """,
            """
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            """
        ]
        
        for script in scripts:
            try:
                driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': script
                })
            except:
                pass


class YouTubeViewWorker(threading.Thread):
    """Worker thread for YouTube view boosting"""
    
    def __init__(self, worker_id, video_title, channel_name, total_views, view_time_min, view_time_max, 
                 use_proxy=False, callback=None, log_callback=None):
        super().__init__()
        self.worker_id = worker_id
        self.video_title = video_title
        self.channel_name = channel_name
        self.total_views = total_views
        self.view_time_min = view_time_min
        self.view_time_max = view_time_max
        self.use_proxy = use_proxy
        self.is_running = True
        self.driver = None
        self.anti_detection = AntiDetectionSystem()
        self.completed_views = 0
        self.session_id = random.randint(1000, 9999)
        self.callback = callback
        self.log_callback = log_callback
        self.daemon = True
        self.current_status = "Initializing"
    
    def stop(self):
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def create_driver(self):
        try:
            # Get Chrome version
            chrome_version = ChromeVersionManager.get_chrome_version()
            if chrome_version:
                major_version = ChromeVersionManager.get_major_version(chrome_version)
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] Chrome version: {chrome_version}", "info")
            else:
                major_version = None
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] Could not detect Chrome version, using auto", "warning")
            
            options = self.anti_detection.get_chrome_options(self.use_proxy)
            
            # Use unique user data directory for each worker to avoid conflicts
            user_data_dir = os.path.join(os.getcwd(), f"chrome_profile_{self.worker_id}_{random.randint(1000, 9999)}")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Create driver with version specification if available
            if major_version:
                try:
                    self.driver = uc.Chrome(
                        options=options,
                        version_main=major_version,
                        headless=False
                    )
                except Exception as e:
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] Version-specific driver failed: {str(e)}", "warning")
                    # Fallback to auto-detection
                    self.driver = uc.Chrome(
                        options=options,
                        headless=False
                    )
            else:
                # Auto-detect version
                self.driver = uc.Chrome(
                    options=options,
                    headless=False
                )
            
            # Apply stealth scripts
            self.anti_detection.apply_stealth_scripts(self.driver)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "This version of ChromeDriver only supports Chrome version" in error_msg:
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] ChromeDriver version mismatch. Trying fallback...", "warning")
                # Try one more time with auto-detection
                try:
                    self.driver = uc.Chrome(
                        options=options,
                        headless=False
                    )
                    return True
                except Exception as e2:
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] Fallback also failed: {str(e2)}", "error")
                    return False
            else:
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] Failed to create driver: {str(e)}", "error")
                return False
    
    def run(self):
        if not self.create_driver():
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ❌ Failed to initialize driver, stopping worker", "error")
            return
        
        if self.log_callback:
            self.log_callback(f"[Worker {self.worker_id}] 🚀 Started for: {self.video_title}", "success")
        
        for view_num in range(1, self.total_views + 1):
            if not self.is_running:
                break
            
            self.current_status = f"View {view_num}/{self.total_views}"
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] 📹 Starting view {view_num}/{self.total_views}", "info")
            
            if self.watch_video():
                self.completed_views += 1
                if self.callback:
                    self.callback()
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] ✅ View {view_num}/{self.total_views} completed", "success")
            else:
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] ❌ View {view_num} failed, retrying...", "warning")
                time.sleep(5)
                if self.watch_video():
                    self.completed_views += 1
                    if self.callback:
                        self.callback()
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] ✅ View {view_num} completed (retry)", "success")
            
            if view_num < self.total_views and self.is_running:
                delay = random.randint(60, 180)
                if self.log_callback:
                    self.log_callback(f"[Worker {self.worker_id}] ⏳ Waiting {delay}s before next view...", "info")
                for i in range(delay):
                    if not self.is_running:
                        break
                    if i % 30 == 0 and i > 0:
                        self.current_status = f"Waiting {delay-i}s"
                    time.sleep(1)
        
        if self.log_callback:
            self.log_callback(f"[Worker {self.worker_id}] 🎉 Session completed! Total views: {self.completed_views}", "success")
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def random_human_behavior(self):
        if RANDOM_MOUSE_MOVEMENTS and random.random() < 0.3:
            try:
                action = ActionChains(self.driver)
                width = self.driver.execute_script("return window.innerWidth;")
                height = self.driver.execute_script("return window.innerHeight;")
                x = random.randint(100, width - 100)
                y = random.randint(100, height - 100)
                action.move_by_offset(x, y).perform()
            except:
                pass
        
        if RANDOM_SCROLLING and random.random() < 0.2:
            try:
                scroll_height = self.driver.execute_script("return document.body.scrollHeight")
                if scroll_height > 500:
                    scroll_position = random.randint(0, scroll_height - 500)
                    self.driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
            except:
                pass
        
        if RANDOM_PAUSES:
            time.sleep(random.uniform(0.5, 2))
    
    def watch_video(self):
        try:
            search_query = f"{self.video_title} {self.channel_name}"
            encoded_query = urllib.parse.quote(search_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] 🔍 Searching: {search_query}", "info")
            
            self.driver.get(search_url)
            
            # Wait for results
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer, ytd-rich-item-renderer")))
            
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] 📄 Page loaded, finding video...", "info")
            
            time.sleep(random.uniform(2, 4))
            
            # Find video
            video_element = self.find_video_by_channel()
            
            if not video_element:
                try:
                    video_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-video-renderer #thumbnail, ytd-rich-item-renderer #thumbnail")
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] Using first video as fallback", "warning")
                except:
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] No video found", "error")
                    return False
            
            # Click video
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ▶️ Clicking video...", "info")
            self.driver.execute_script("arguments[0].click();", video_element)
            
            # Wait for video page
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
            time.sleep(random.uniform(3, 5))
            
            # Start video playback
            self.ensure_video_plays()
            self.random_human_behavior()
            
            # Watch duration
            watch_duration = random.randint(self.view_time_min, self.view_time_max)
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ⏱️ Watching for {watch_duration}s...", "info")
            
            start_time = time.time()
            last_log_time = start_time
            
            while time.time() - start_time < watch_duration:
                if not self.is_running:
                    return False
                
                self.random_human_behavior()
                
                # Check if video is still playing
                try:
                    video = self.driver.find_element(By.CSS_SELECTOR, "video")
                    is_paused = self.driver.execute_script("return arguments[0].paused;", video)
                    if is_paused:
                        self.driver.execute_script("arguments[0].play();", video)
                        if self.log_callback:
                            self.log_callback(f"[Worker {self.worker_id}] ▶️ Video was paused, resuming...", "warning")
                except:
                    pass
                
                # Log progress every 15 seconds
                current_time = time.time()
                if current_time - last_log_time >= 15:
                    elapsed = int(current_time - start_time)
                    remaining = watch_duration - elapsed
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] ⏱️ {elapsed}s elapsed, {remaining}s remaining", "info")
                    last_log_time = current_time
                
                time.sleep(random.uniform(2, 5))
            
            # Random engagement
            self.random_engagement()
            
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ✅ Video watch completed", "success")
            
            return True
            
        except TimeoutException as e:
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ⏱️ Timeout: {str(e)}", "error")
            return False
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"[Worker {self.worker_id}] ❌ Error: {str(e)}", "error")
            return False
    
    def find_video_by_channel(self):
        try:
            selectors = ["ytd-video-renderer", "ytd-rich-item-renderer", "ytd-compact-video-renderer"]
            
            video_elements = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    video_elements.extend(elements)
                except:
                    continue
            
            for video in video_elements:
                try:
                    title_element = video.find_element(By.CSS_SELECTOR, "#video-title")
                    title_text = title_element.get_attribute("title") or title_element.text
                    
                    if self.channel_name.lower() in title_text.lower():
                        return title_element
                    
                    try:
                        channel_element = video.find_element(By.CSS_SELECTOR, "#channel-name a, yt-formatted-string#owner-name a")
                        channel_text = channel_element.text
                        if self.channel_name.lower() in channel_text.lower():
                            return title_element
                    except:
                        pass
                except:
                    continue
            
            return None
        except:
            return None
    
    def ensure_video_plays(self):
        try:
            video = self.driver.find_element(By.CSS_SELECTOR, "video")
            
            methods = [
                lambda: self.driver.execute_script("arguments[0].click();", video),
                lambda: self.driver.find_element(By.CSS_SELECTOR, ".ytp-large-play-button").click(),
                lambda: self.driver.find_element(By.CSS_SELECTOR, ".ytp-play-button").click(),
                lambda: self.driver.execute_script("document.querySelector('video').play();"),
            ]
            
            for method in methods:
                try:
                    method()
                    time.sleep(0.5)
                except:
                    continue
            
            time.sleep(2)
            is_playing = self.driver.execute_script("return !arguments[0].paused;", video)
            
            if not is_playing:
                self.driver.execute_script("arguments[0].play();", video)
                time.sleep(1)
            
        except Exception:
            pass
    
    def random_engagement(self):
        try:
            if random.random() < LIKE_PROBABILITY:
                try:
                    like_button = self.driver.find_element(By.CSS_SELECTOR, "ytd-toggle-button-renderer[aria-pressed='false'] #button")
                    self.driver.execute_script("arguments[0].click();", like_button)
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] 👍 Liked video!", "info")
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
            
            if random.random() < SUBSCRIBE_PROBABILITY:
                try:
                    subscribe_button = self.driver.find_element(By.CSS_SELECTOR, "ytd-subscribe-button-renderer #subscribe-button")
                    self.driver.execute_script("arguments[0].click();", subscribe_button)
                    if self.log_callback:
                        self.log_callback(f"[Worker {self.worker_id}] 🔔 Subscribed to channel!", "info")
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
        except:
            pass


class VidaiBotGUI:
    """Main GUI window for VidaiBot Pro"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.workers = []
        self.total_target_views = 0
        self.total_completed_views = 0
        self.is_running = False
        self.proxies_loaded = False
        self.proxy_file_path = ""
        self.search_terms = []
        self.log_auto_scroll = tk.BooleanVar(value=True)
        
        # Setup UI
        self.setup_ui()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Auto-start if configured
        self.auto_start = False
    
    def setup_ui(self):
        """Setup the UI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== Title =====
        title_frame = tk.Frame(main_frame, bg='#f0f0f0')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text=f"🎬 {APP_NAME}", font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(title_frame, text=f"v{APP_VERSION}", font=('Arial', 10), bg='#f0f0f0', fg='#666')
        version_label.pack(side=tk.LEFT, padx=10)
        
        # ===== Search Terms =====
        search_frame = tk.LabelFrame(main_frame, text="Search Terms", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333')
        search_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Input row
        input_frame = tk.Frame(search_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Video Title:", bg='#f0f0f0').grid(row=0, column=0, padx=(5, 5), sticky=tk.W)
        self.video_title_entry = tk.Entry(input_frame, width=35, font=('Arial', 10))
        self.video_title_entry.grid(row=0, column=1, padx=(0, 15), sticky=tk.W+tk.E)
        
        tk.Label(input_frame, text="Channel Name:", bg='#f0f0f0').grid(row=0, column=2, padx=(5, 5), sticky=tk.W)
        self.channel_name_entry = tk.Entry(input_frame, width=35, font=('Arial', 10))
        self.channel_name_entry.grid(row=0, column=3, padx=(0, 15), sticky=tk.W+tk.E)
        
        add_btn = tk.Button(input_frame, text="+ Add", command=self.add_search_term, 
                           bg='#4CAF50', fg='white', font=('Arial', 10), padx=15, cursor='hand2')
        add_btn.grid(row=0, column=4, padx=(0, 5))
        
        clear_btn = tk.Button(input_frame, text="Clear", command=self.clear_terms,
                             bg='#f44336', fg='white', font=('Arial', 10), padx=15, cursor='hand2')
        clear_btn.grid(row=0, column=5)
        
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Search terms listbox
        list_frame = tk.Frame(search_frame, bg='#f0f0f0')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.terms_listbox = tk.Listbox(list_frame, height=3, font=('Arial', 10), bg='white')
        self.terms_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.terms_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terms_listbox.config(yscrollcommand=scrollbar.set)
        
        # Count label
        self.term_count_label = tk.Label(search_frame, text="Number of search terms: 0", bg='#f0f0f0', font=('Arial', 9))
        self.term_count_label.pack(anchor=tk.W, pady=(5, 0))
        
        # ===== Proxy Settings =====
        proxy_frame = tk.LabelFrame(main_frame, text="Proxy Settings", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333')
        proxy_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        proxy_inner = tk.Frame(proxy_frame, bg='#f0f0f0')
        proxy_inner.pack(fill=tk.X, pady=5)
        
        self.import_proxy_btn = tk.Button(proxy_inner, text="📁 Import Proxies", command=self.import_proxies,
                                         bg='#2196F3', fg='white', font=('Arial', 10), padx=15, cursor='hand2')
        self.import_proxy_btn.pack(side=tk.LEFT, padx=(5, 10))
        
        self.proxy_file_label = tk.Label(proxy_inner, text="No file selected", bg='#f0f0f0', fg='gray', font=('Arial', 9))
        self.proxy_file_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.use_proxy_var = tk.BooleanVar()
        self.use_proxy_check = tk.Checkbutton(proxy_inner, text="🌐 Use Proxy", variable=self.use_proxy_var,
                                             bg='#f0f0f0', font=('Arial', 10))
        self.use_proxy_check.pack(side=tk.LEFT)
        
        # ===== Settings =====
        settings_frame = tk.LabelFrame(main_frame, text="Settings", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333')
        settings_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        settings_grid = tk.Frame(settings_frame, bg='#f0f0f0')
        settings_grid.pack(fill=tk.X, pady=5, padx=5)
        
        # Row 1
        tk.Label(settings_grid, text="No. of Views:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.views_spinbox = tk.Spinbox(settings_grid, from_=1, to=10000, width=12, font=('Arial', 10))
        self.views_spinbox.delete(0, tk.END)
        self.views_spinbox.insert(0, "2")
        self.views_spinbox.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)
        
        tk.Label(settings_grid, text="No. of Threads:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.threads_spinbox = tk.Spinbox(settings_grid, from_=1, to=MAX_THREADS, width=12, font=('Arial', 10))
        self.threads_spinbox.delete(0, tk.END)
        self.threads_spinbox.insert(0, "1")
        self.threads_spinbox.grid(row=0, column=3, padx=(0, 20), sticky=tk.W)
        
        # Row 2
        tk.Label(settings_grid, text="Min. View Time (s):", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, padx=(0, 5), sticky=tk.W, pady=(5, 0))
        self.min_time_spinbox = tk.Spinbox(settings_grid, from_=10, to=600, width=12, font=('Arial', 10))
        self.min_time_spinbox.delete(0, tk.END)
        self.min_time_spinbox.insert(0, "30")
        self.min_time_spinbox.grid(row=1, column=1, padx=(0, 20), sticky=tk.W, pady=(5, 0))
        
        tk.Label(settings_grid, text="Max. View Time (s):", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=2, padx=(0, 5), sticky=tk.W, pady=(5, 0))
        self.max_time_spinbox = tk.Spinbox(settings_grid, from_=10, to=600, width=12, font=('Arial', 10))
        self.max_time_spinbox.delete(0, tk.END)
        self.max_time_spinbox.insert(0, "60")
        self.max_time_spinbox.grid(row=1, column=3, padx=(0, 20), sticky=tk.W, pady=(5, 0))
        
        settings_grid.columnconfigure(1, weight=1)
        settings_grid.columnconfigure(3, weight=1)
        
        # ===== Status =====
        status_frame = tk.LabelFrame(main_frame, text="Status", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333')
        status_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        status_grid = tk.Frame(status_frame, bg='#f0f0f0')
        status_grid.pack(fill=tk.X, pady=5, padx=5)
        
        # Bot Status
        tk.Label(status_grid, text="Bot Status:", bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.status_label = tk.Label(status_grid, text="● Idle", bg='#f0f0f0', fg='gray', font=('Arial', 10))
        self.status_label.grid(row=0, column=1, padx=(0, 30), sticky=tk.W)
        
        # Target Views
        tk.Label(status_grid, text="Target Views:", bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.target_views_label = tk.Label(status_grid, text="0", bg='#f0f0f0', font=('Arial', 10))
        self.target_views_label.grid(row=0, column=3, padx=(0, 30), sticky=tk.W)
        
        # Views Done
        tk.Label(status_grid, text="Views Done:", bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=(0, 5), sticky=tk.W, pady=(5, 0))
        self.views_done_label = tk.Label(status_grid, text="0", bg='#f0f0f0', font=('Arial', 10))
        self.views_done_label.grid(row=1, column=1, padx=(0, 30), sticky=tk.W, pady=(5, 0))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # ===== Log Output =====
        log_frame = tk.LabelFrame(main_frame, text="Log Output", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=5)
        
        # Log controls
        log_control_frame = tk.Frame(log_frame, bg='#f0f0f0')
        log_control_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.auto_scroll_check = tk.Checkbutton(log_control_frame, text="Auto-scroll", 
                                               variable=self.log_auto_scroll, bg='#f0f0f0')
        self.auto_scroll_check.pack(side=tk.LEFT)
        
        clear_log_btn = tk.Button(log_control_frame, text="Clear Log", command=self.clear_log,
                                 bg='#FF9800', fg='white', font=('Arial', 9), padx=10, cursor='hand2')
        clear_log_btn.pack(side=tk.RIGHT)
        
        self.log_output = scrolledtext.ScrolledText(log_frame, height=6, font=('Consolas', 9), bg='#1e1e1e', fg='#d4d4d4')
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure log colors for dark theme
        self.log_output.tag_configure("info", foreground="#87CEEB")  # Light blue
        self.log_output.tag_configure("warning", foreground="#FFA500")  # Orange
        self.log_output.tag_configure("error", foreground="#FF6B6B")  # Red
        self.log_output.tag_configure("success", foreground="#4CAF50")  # Green
        
        # ===== CONTROL BUTTONS =====
        button_frame = tk.Frame(main_frame, bg='#f0f0f0', height=80)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        button_frame.pack_propagate(False)
        
        # Center the buttons
        center_frame = tk.Frame(button_frame, bg='#f0f0f0')
        center_frame.pack(expand=True)
        
        # START Button
        self.start_btn = tk.Button(
            center_frame,
            text="▶  START",
            command=self.start_bot,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=40,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            width=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # STOP Button
        self.stop_btn = tk.Button(
            center_frame,
            text="⏹  STOP",
            command=self.stop_bot,
            bg='#f44336',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=40,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            width=12,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Button hover effects
        def on_enter_start(e):
            self.start_btn.config(bg='#45a049')
        def on_leave_start(e):
            self.start_btn.config(bg='#4CAF50')
        def on_enter_stop(e):
            self.stop_btn.config(bg='#da190b')
        def on_leave_stop(e):
            self.stop_btn.config(bg='#f44336')
        
        self.start_btn.bind('<Enter>', on_enter_start)
        self.start_btn.bind('<Leave>', on_leave_start)
        self.stop_btn.bind('<Enter>', on_enter_stop)
        self.stop_btn.bind('<Leave>', on_leave_stop)
    
    def clear_log(self):
        """Clear the log output"""
        self.log_output.config(state='normal')
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state='disabled')
    
    def add_search_term(self):
        video_title = self.video_title_entry.get().strip()
        channel_name = self.channel_name_entry.get().strip()
        
        if not video_title or not channel_name:
            messagebox.showwarning("Input Error", "Please enter both video title and channel name.")
            return
        
        term = f"{video_title} | {channel_name}"
        self.terms_listbox.insert(tk.END, term)
        self.search_terms.append((video_title, channel_name))
        
        self.video_title_entry.delete(0, tk.END)
        self.channel_name_entry.delete(0, tk.END)
        self.update_term_count()
    
    def clear_terms(self):
        self.terms_listbox.delete(0, tk.END)
        self.search_terms.clear()
        self.update_term_count()
    
    def update_term_count(self):
        count = len(self.search_terms)
        self.term_count_label.config(text=f"Number of search terms: {count}")
    
    def import_proxies(self):
        file_path = filedialog.askopenfilename(
            title="Import Proxies",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.proxy_file_path = file_path
            self.proxy_file_label.config(text=os.path.basename(file_path), fg='green')
            self.proxies_loaded = True
            self.log_message(f"📁 Proxies loaded from: {file_path}", "info")
    
    def log_message(self, message, msg_type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, f"[{timestamp}] {message}\n", msg_type)
        if self.log_auto_scroll.get():
            self.log_output.see(tk.END)
        self.log_output.config(state='disabled')
    
    def start_bot(self):
        if not self.search_terms:
            messagebox.showwarning("Input Error", "Please add at least one search term.")
            return
        
        total_views = int(self.views_spinbox.get())
        num_threads = int(self.threads_spinbox.get())
        min_time = int(self.min_time_spinbox.get())
        max_time = int(self.max_time_spinbox.get())
        use_proxy = self.use_proxy_var.get()
        
        if not self.proxies_loaded and use_proxy:
            reply = messagebox.askyesno(
                "No Proxies",
                "Proxy is enabled but no proxies are loaded. Continue without proxies?"
            )
            if not reply:
                return
            use_proxy = False
        
        if min_time >= max_time:
            messagebox.showwarning("Input Error", "Min view time must be less than max view time.")
            return
        
        # Update UI
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, bg='#cccccc')
        self.stop_btn.config(state=tk.NORMAL, bg='#f44336')
        self.status_label.config(text="● Running", fg='green')
        
        self.total_target_views = total_views * num_threads * len(self.search_terms)
        self.target_views_label.config(text=str(self.total_target_views))
        self.total_completed_views = 0
        self.views_done_label.config(text="0")
        self.progress_bar['value'] = 0
        
        self.log_message("=" * 70, "info")
        self.log_message(f"🚀 Starting bot with {num_threads} threads", "success")
        self.log_message(f"🎯 Target: {total_views} views per term", "info")
        self.log_message(f"📹 Search terms: {len(self.search_terms)}", "info")
        self.log_message(f"⏱️  Watch time: {min_time}-{max_time} seconds", "info")
        self.log_message("=" * 70, "info")
        
        # Clear existing workers
        for worker in self.workers:
            worker.stop()
        self.workers.clear()
        
        # Create workers
        worker_id = 1
        for video_title, channel_name in self.search_terms:
            for i in range(num_threads):
                worker = YouTubeViewWorker(
                    worker_id,
                    video_title, channel_name, total_views,
                    min_time, max_time, use_proxy,
                    callback=self.update_progress,
                    log_callback=self.log_message
                )
                self.workers.append(worker)
                worker_id += 1
        
        # Start all workers
        for worker in self.workers:
            worker.start()
        
        self.status_var.set(f"Bot running with {len(self.workers)} workers...")
        self.log_message(f"✅ Started {len(self.workers)} worker threads", "success")
    
    def stop_bot(self):
        self.is_running = False
        self.status_label.config(text="● Stopping...", fg='orange')
        
        for worker in self.workers:
            worker.stop()
        
        self.start_btn.config(state=tk.NORMAL, bg='#4CAF50')
        self.stop_btn.config(state=tk.DISABLED, bg='#cccccc')
        self.status_label.config(text="● Stopped", fg='red')
        self.status_var.set("Bot stopped")
        self.log_message("⏹ Bot stopped by user", "warning")
    
    def update_progress(self):
        def update():
            self.total_completed_views += 1
            self.views_done_label.config(text=str(self.total_completed_views))
            
            if self.total_target_views > 0:
                progress = int((self.total_completed_views / self.total_target_views) * 100)
                self.progress_bar['value'] = progress
            
            self.status_var.set(f"Progress: {self.total_completed_views}/{self.total_target_views} ({progress}%)")
            
            if self.total_completed_views >= self.total_target_views:
                self.root.after(100, self.finish_bot)
        
        self.root.after(0, update)
    
    def finish_bot(self):
        self.stop_bot()
        self.log_message("🎉 All views completed successfully!", "success")
        messagebox.showinfo("Complete", f"All {self.total_completed_views} views completed successfully!")


def main():
    root = tk.Tk()
    app = VidaiBotGUI(root)
    
    def on_closing():
        if app.is_running:
            app.stop_bot()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()