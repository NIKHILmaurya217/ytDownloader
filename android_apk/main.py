from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
import yt_dlp
import threading
import os
import time

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

Screen:
    canvas.before:
        Color:
            rgba: get_color_from_hex("#f5f5f7")
        Rectangle:
            pos: self.pos
            size: self.size
            
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        
        MDCard:
            orientation: "vertical"
            padding: dp(16)
            elevation: 4
            radius: [15, 15, 15, 15]
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                
                MDLabel:
                    text: "YouTube Downloader"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#e91e63")
                    font_style: "H5"
                    halign: "center"
                    bold: True
                
                MDTextField:
                    id: url_input
                    hint_text: "Enter YouTube URL"
                    mode: "rectangle"
                    icon_right: "youtube"
                    helper_text: "Paste a YouTube video URL here"
                    helper_text_mode: "on_focus"
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    adaptive_height: True
                    
                    MDTextField:
                        id: folder_input
                        hint_text: "Download Folder"
                        mode: "rectangle"
                        text: "/storage/emulated/0/Download"
                        icon_right: "folder"
                        size_hint_x: 0.8
                    
                    MDRaisedButton:
                        text: "Browse"
                        size_hint_x: 0.2
                        on_release: app.show_file_chooser()
                
                MDLabel:
                    text: "Video Quality:"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: dp(30)
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    adaptive_height: True
                    
                    MDRaisedButton:
                        text: "360p"
                        size_hint_x: 0.25
                        md_bg_color: [0.2, 0.2, 0.2, 1] if app.selected_quality == "360" else [0.7, 0.7, 0.7, 1]
                        on_release: app.set_quality_direct("360")
                        
                    MDRaisedButton:
                        text: "480p"
                        size_hint_x: 0.25
                        md_bg_color: [0.2, 0.2, 0.2, 1] if app.selected_quality == "480" else [0.7, 0.7, 0.7, 1]
                        on_release: app.set_quality_direct("480")
                        
                    MDRaisedButton:
                        text: "720p"
                        size_hint_x: 0.25
                        md_bg_color: [0.2, 0.2, 0.2, 1] if app.selected_quality == "720" else [0.7, 0.7, 0.7, 1]
                        on_release: app.set_quality_direct("720")
                        
                    MDRaisedButton:
                        text: "1080p"
                        size_hint_x: 0.25
                        md_bg_color: [0.2, 0.2, 0.2, 1] if app.selected_quality == "1080" else [0.7, 0.7, 0.7, 1]
                        on_release: app.set_quality_direct("1080")

                    MDRaisedButton:
                        text: "best"
                        size_hint_x: 0.25
                        md_bg_color: [0.2, 0.2, 0.2, 1] if app.selected_quality == "1080" else [0.7, 0.7, 0.7, 1]
                        on_release: app.set_quality_direct("best")
                
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: [0, dp(10), 0, 0]
                    
                    MDProgressBar:
                        id: progress_bar
                        value: 0
                        color: get_color_from_hex("#e91e63")
                        back_color: get_color_from_hex("#f0f0f0")
                        size_hint_y: None
                        height: dp(10)
                    
                    MDLabel:
                        id: progress_label
                        text: "Ready to download"
                        halign: "center"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(15)
                    padding: [0, dp(10), 0, 0]
                    adaptive_height: True
                    
                    MDRaisedButton:
                        id: download_btn
                        text: "DOWNLOAD"
                        md_bg_color: get_color_from_hex("#e91e63")
                        size_hint_x: 0.5
                        on_release: app.start_download()
                    
                    MDRaisedButton:
                        id: cancel_btn
                        text: "CANCEL"
                        md_bg_color: get_color_from_hex("#9e9e9e")
                        size_hint_x: 0.5
                        on_release: app.cancel_download()
'''

class YouTubeDownloaderApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_quality = "720"  # Default quality
        
    def build(self):
        self.screen = Builder.load_string(KV)
        self.stop_download = False
        self.quality_menu = None
        self.download_thread = None
        self.ydl = None
        self.dialog = None
        self.theme_cls.primary_palette = "Pink"
        return self.screen
    def set_quality_direct(self, quality):
        """Set quality directly via quality buttons"""
        self.selected_quality = quality
        # Force update of button colors - this is safer than dispatching an event
        Clock.schedule_once(lambda dt: self.update_quality_buttons())
    def update_quality_buttons(self):
        """Update the colors of quality buttons based on selection"""
        for resolution in ["360", "480", "720", "1080","best"]:
            # Find all buttons in the layout
            for child in self.screen.walk():
            # Look for the button with matching text (e.g., "720p")
              if hasattr(child, 'text') and child.text == f"{resolution}p":
                # Update its color based on whether it's selected
                child.md_bg_color = [0.2, 0.2, 0.2, 1] if self.selected_quality == resolution else [0.7, 0.7, 0.7, 1]
    
    def show_file_chooser(self):
        """Show a simplified folder selection dialog"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        common_folders = [
            {"name": "Downloads", "path": "/storage/emulated/0/Download"},
            {"name": "Pictures", "path": "/storage/emulated/0/Pictures"},
            {"name": "Documents", "path": "/storage/emulated/0/Documents"},
            {"name": "Movies", "path": "/storage/emulated/0/Movies"},
            {"name": "DCIM", "path": "/storage/emulated/0/DCIM"},
            '''{"name": "Desktop", "path": "C:/Users/nikhi/Desktop"},'''
        ]
        
        # Create the dialog content
        content = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None, height=400)
        
        # Add folder options
        for folder in common_folders:
            btn = MDRaisedButton(
                text=folder["name"],
                size_hint_x=1,
                on_release=lambda x, path=folder["path"]: self.select_folder(path)
            )
            content.add_widget(btn)
            
        # Add custom folder input option
        custom_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        custom_input = MDTextField(
            hint_text="Enter custom path",
            mode="rectangle",
            size_hint_x=0.7
        )
        custom_btn = MDRaisedButton(
            text="Set",
            size_hint_x=0.3,
            on_release=lambda x: self.select_folder(custom_input.text)
        )
        custom_box.add_widget(custom_input)
        custom_box.add_widget(custom_btn)
        content.add_widget(custom_box)
            
        self.dialog = MDDialog(
            title="Select Download Location",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def select_folder(self, path):
        """Set the selected folder path"""
        if path:
            self.screen.ids.folder_input.text = path
            
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
    
    def update_progress(self, value, text):
        self.screen.ids.progress_bar.value = value
        self.screen.ids.progress_label.text = text
    
    def progress_hook(self, d):
        if self.stop_download:
            raise Exception("Download canceled by user")
            
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                Clock.schedule_once(lambda dt: self.update_progress(percent, f"{int(percent)}% complete"))
            else:
                # If we can't get total size, show downloaded size instead
                downloaded_mb = downloaded / (1024 * 1024)
                Clock.schedule_once(lambda dt: self.update_progress(
                    50, f"Downloaded: {downloaded_mb:.1f} MB"))
        
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_progress(100, "Processing video..."))
    
    def toggle_ui_state(self, downloading=False):
        """Enable/disable UI elements based on download state"""
        Clock.schedule_once(lambda dt: self._toggle_ui_state(downloading))
    
    def _toggle_ui_state(self, downloading):
        """Actually update the UI elements from the main thread"""
        self.screen.ids.download_btn.disabled = downloading
        self.screen.ids.url_input.disabled = downloading
        
        # Change button colors based on state
        if downloading:
            self.screen.ids.download_btn.md_bg_color = [0.7, 0.7, 0.7, 1]  # Grey
            self.screen.ids.cancel_btn.md_bg_color = [0.9, 0.1, 0.1, 1]    # Red
        else:
            self.screen.ids.download_btn.md_bg_color = [0.91, 0.12, 0.39, 1]  # Pink
            self.screen.ids.cancel_btn.md_bg_color = [0.6, 0.6, 0.6, 1]       # Grey
    
    def clear_input(self):
        """Clear the URL input after successful download"""
        self.screen.ids.url_input.text = ""
    
    def start_download(self):
        url = self.screen.ids.url_input.text.strip()
        folder = self.screen.ids.folder_input.text
        quality = self.selected_quality
        
        if not url:
            self.update_progress(0, "Please enter a YouTube URL")
            return
        
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        if not ("youtube.com" in url or "youtu.be" in url):
            self.update_progress(0, "Please enter a valid YouTube URL")
            return
        
        # Try to create folder if it doesn't exist
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                self.update_progress(0, f"Folder error: {str(e)[:30]}")
                return
        
        # Reset state and update UI
        self.stop_download = False
        self.toggle_ui_state(downloading=True)
        self.update_progress(0, "Starting download...")
        
        ydl_opts = {
            'outtmpl': os.path.join(folder, "%(title)s.%(ext)s"),
            'noplaylist': True,
            'progress_hooks': [self.progress_hook],
            'merge_output_format': 'mp4'
        }
        
        if quality and quality.isdigit():
            ydl_opts['format'] = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"
        else:
            ydl_opts['format'] = "bestvideo+bestaudio/best"
        
        def run_download():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.ydl = ydl  # Store reference for potential cancellation
                    ydl.download([url])
                    self.ydl = None
                
                if not self.stop_download:
                    # Only clear input and show completion if not canceled
                    Clock.schedule_once(lambda dt: self.update_progress(100, "Download Complete!"))
                    Clock.schedule_once(lambda dt: self.clear_input())
            except Exception as e:
                error_msg = str(e)
                if "canceled by user" in error_msg:
                    Clock.schedule_once(lambda dt: self.update_progress(0, "Download Canceled"))
                else:
                    Clock.schedule_once(lambda dt: self.update_progress(0, f"Error: {error_msg[:40]}"))
            finally:
                self.toggle_ui_state(downloading=False)
                self.ydl = None
        
        self.download_thread = threading.Thread(target=run_download, daemon=True)
        self.download_thread.start()
    
    def cancel_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.stop_download = True
            self.update_progress(0, "Canceling download...")
            
            # The thread will detect the stop_download flag on the next progress update
            if self.ydl:
                # Try to forcibly terminate the download if possible
                try:
                    self.ydl._finish_multiline_status()
                except:
                    pass
            
            # Give download thread a moment to terminate gracefully
            Clock.schedule_once(lambda dt: self.toggle_ui_state(downloading=False), 1)

if __name__ == "__main__":
    YouTubeDownloaderApp().run()