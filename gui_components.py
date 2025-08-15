import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import threading
import time

class ModernButton(ctk.CTkButton):
    """Enhanced button with 3D effects and animations"""
    
    def __init__(self, parent, text, command, width=200, height=40, 
                 bg_color="#7209b7", hover_color="#e91e63", corner_radius=20, font_size=12, **kwargs):
        
        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=bg_color,
            hover_color=hover_color,
            font=ctk.CTkFont(size=font_size, weight="bold"),
            **kwargs
        )
        
        # Bind hover events for enhanced animation
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def on_enter(self, event):
        """Enhanced hover effect"""
        self.configure(cursor="hand2")
        
    def on_leave(self, event):
        """Reset hover effect"""
        self.configure(cursor="")
        
    def on_click(self, event):
        """Click animation"""
        pass
        
    def on_release(self, event):
        """Release animation"""
        pass

class AnimatedProgressBar(ctk.CTkProgressBar):
    """Progress bar with smooth animations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.target_value = 0
        self.current_value = 0
        self.animation_speed = 0.02
        
    def animate_to(self, target_value):
        """Smoothly animate to target value"""
        self.target_value = max(0, min(1, target_value))  # Clamp between 0 and 1
        self.animate_progress()
        
    def animate_progress(self):
        """Internal animation method"""
        if abs(self.current_value - self.target_value) > 0.001:
            # Calculate step
            step = (self.target_value - self.current_value) * 0.15
            self.current_value += step
            self.set(self.current_value)
            
            # Schedule next animation frame
            self.after(20, self.animate_progress)

class FileDropArea(ctk.CTkFrame):
    """Enhanced drag and drop area for files"""
    
    def __init__(self, parent, on_file_drop=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_file_drop = on_file_drop
        
        # Create drop area UI with modern styling
        self.drop_label = ctk.CTkLabel(
            self,
            text="📁\n\nDrag & Drop Files Here\nor Click to Browse\n\nSupported: PDF, Word, PowerPoint, Images\n\n🖼️ Use Multi-Image for multiple images → PDF",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888",
            justify="center"
        )
        self.drop_label.pack(expand=True, fill="both", padx=15, pady=15)
        
        # Bind click events
        self.drop_label.bind("<Button-1>", self.on_click)
        self.bind("<Button-1>", self.on_click)
        
        # Visual feedback for hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.drop_label.bind("<Enter>", self.on_enter)
        self.drop_label.bind("<Leave>", self.on_leave)
        
        # Setup drag and drop if available
        try:
            self.setup_drag_drop()
        except:
            pass
    
    def on_enter(self, event):
        """Hover effect"""
        self.configure(border_width=2, border_color="#7209b7")
        self.drop_label.configure(text_color="#7209b7")
        
    def on_leave(self, event):
        """Reset hover effect"""
        self.configure(border_width=1, border_color="#333333")
        self.drop_label.configure(text_color="#888888")
            
    def on_click(self, event):
        """Handle click to browse files"""
        if self.on_file_drop:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Select File to Convert",
                filetypes=[
                    ("All Supported", "*.pdf;*.docx;*.doc;*.pptx;*.ppt;*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
                    ("PDF files", "*.pdf"),
                    ("Word documents", "*.docx;*.doc"),
                    ("PowerPoint files", "*.pptx;*.ppt"),
                    ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
                    ("All files", "*.*")
                ]
            )
            if filename:
                self.on_file_drop([filename])
                
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            import tkinterdnd2 as tkdnd
            self.drop_target_register(tkdnd.DND_FILES)
            self.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            # Drag and drop not available
            pass
            
    def on_drop(self, event):
        """Handle dropped files"""
        try:
            files = self.tk.splitlist(event.data)
            if self.on_file_drop and files:
                self.on_file_drop(files)
        except:
            pass

class StatusIndicator(ctk.CTkFrame):
    """Animated status indicator with modern styling"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Status icon and text
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=5, pady=5)
        
        self.status_icon = ctk.CTkLabel(
            self.status_frame,
            text="🔵",
            font=ctk.CTkFont(size=16)
        )
        self.status_icon.pack(side="left", padx=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)
        
        self.progress_dots = ""
        self.animation_running = False
        
    def set_status(self, status_text, status_type="info"):
        """Set status with icon and color"""
        icons = {
            "info": "🔵",
            "success": "🟢", 
            "error": "🔴",
            "warning": "🟡",
            "processing": "🟣"
        }
        
        colors = {
            "info": "#2196f3",
            "success": "#4caf50",
            "error": "#f44336", 
            "warning": "#ff9800",
            "processing": "#7209b7"
        }
        
        icon = icons.get(status_type, "🔵")
        color = colors.get(status_type, "#2196f3")
        
        self.status_icon.configure(text=icon)
        self.status_label.configure(text=status_text, text_color=color)
        
        if status_type == "processing":
            self.start_processing_animation()
        else:
            self.stop_processing_animation()
            
    def start_processing_animation(self):
        """Start animated dots for processing"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_processing()
            
    def animate_processing(self):
        """Animate processing dots"""
        if self.animation_running:
            self.progress_dots = (self.progress_dots + ".") if len(self.progress_dots) < 3 else ""
            current_text = self.status_label.cget("text").split(".")[0]
            self.status_label.configure(text=f"{current_text}{self.progress_dots}")
            self.after(500, self.animate_processing)
            
    def stop_processing_animation(self):
        """Stop processing animation"""
        self.animation_running = False
        self.progress_dots = ""

class ToolTip:
    """Modern tooltip for widgets"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Bind events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        
    def show_tooltip(self, event=None):
        """Show tooltip with modern styling"""
        if self.tooltip_window:
            return
            
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Modern styled tooltip
        frame = tk.Frame(
            self.tooltip_window,
            background="#1a1a2e",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=6
        )
        frame.pack()
        
        label = tk.Label(
            frame,
            text=self.text,
            background="#1a1a2e",
            foreground="white",
            font=("Segoe UI", 10),
            justify="left"
        )
        label.pack()
        
    def hide_tooltip(self, event=None):
        """Hide tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ThemeManager:
    """Enhanced theme management system"""
    
    def __init__(self):
        self.themes = {
            "dark_purple": {
                'bg_primary': '#0a0a0f',
                'bg_secondary': '#1a1a2e', 
                'bg_tertiary': '#2a2a4e',
                'accent_purple': '#7209b7',
                'accent_pink': '#e91e63',
                'accent_blue': '#2196f3',
                'text_primary': '#ffffff',
                'text_secondary': '#b3b3b3',
                'success': '#4caf50',
                'error': '#f44336',
                'warning': '#ff9800',
                'hover': '#16213e'
            },
            "cyberpunk": {
                'bg_primary': '#0f0f0f',
                'bg_secondary': '#1a0033',
                'bg_tertiary': '#330066',
                'accent_purple': '#ff00ff',
                'accent_pink': '#00ffff',
                'accent_blue': '#ff0080',
                'text_primary': '#ffffff',
                'text_secondary': '#cccccc',
                'success': '#00ff00',
                'error': '#ff0040',
                'warning': '#ffff00',
                'hover': '#4d0099'
            },
            "ocean_blue": {
                'bg_primary': '#0a1929',
                'bg_secondary': '#1a2332',
                'bg_tertiary': '#2a3441',
                'accent_purple': '#1976d2',
                'accent_pink': '#00acc1',
                'accent_blue': '#0288d1',
                'text_primary': '#ffffff',
                'text_secondary': '#b3b3b3',
                'success': '#2e7d32',
                'error': '#d32f2f',
                'warning': '#f57c00',
                'hover': '#263238'
            }
        }
        
        self.current_theme = "dark_purple"
        
    def get_theme(self, theme_name=None):
        """Get theme colors"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["dark_purple"])
        
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            appearance_mode = "dark" if theme_name != "light_mode" else "light"
            ctk.set_appearance_mode(appearance_mode)
            
    def get_available_themes(self):
        """Get list of available themes"""
        return list(self.themes.keys())

class EnhancedScrollableFrame(ctk.CTkScrollableFrame):
    """Enhanced scrollable frame with better styling"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure scrollbar styling
        self._parent_canvas.configure(highlightthickness=0)
        
class LoadingSpinner(ctk.CTkFrame):
    """Animated loading spinner"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_char = 0
        self.spinning = False
        
        self.spinner_label = ctk.CTkLabel(
            self,
            text="⠋",
            font=ctk.CTkFont(size=20),
            text_color="#7209b7"
        )
        self.spinner_label.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=ctk.CTkFont(size=12),
            text_color="#b3b3b3"
        )
        self.status_label.pack()
        
    def start_spinning(self, status_text="Loading..."):
        """Start spinner animation"""
        self.status_label.configure(text=status_text)
        self.spinning = True
        self.spin()
        
    def stop_spinning(self):
        """Stop spinner animation"""
        self.spinning = False
        
    def spin(self):
        """Animate spinner"""
        if self.spinning:
            self.spinner_label.configure(text=self.spinner_chars[self.current_char])
            self.current_char = (self.current_char + 1) % len(self.spinner_chars)
            self.after(100, self.spin)

class AnimationUtils:
    """Utility class for smooth animations"""
    
    @staticmethod
    def fade_in(widget, duration=300, steps=15):
        """Fade in animation"""
        step_time = duration // steps
        
        def animate_step(current_step=0):
            if current_step <= steps:
                alpha = current_step / steps
                # Note: CustomTkinter doesn't support alpha directly
                # This is a placeholder for potential future implementation
                widget.after(step_time, lambda: animate_step(current_step + 1))
        
        animate_step()
        
    @staticmethod
    def slide_in(widget, direction="left", distance=100, duration=300):
        """Slide in animation"""
        # Placeholder for slide animation implementation
        pass
        
    @staticmethod
    def bounce_effect(widget, intensity=5, duration=200):
        """Bounce effect animation"""
        try:
            original_width = widget.cget("width")
            original_height = widget.cget("height")
            
            def bounce_step(step=0, direction=1):
                if step < 4:
                    scale = 1 + (intensity * direction * (4 - step) / 100)
                    new_width = int(original_width * scale)
                    new_height = int(original_height * scale)
                    
                    widget.configure(width=new_width, height=new_height)
                    widget.after(duration // 8, 
                               lambda: bounce_step(step + 1, -direction if step == 1 else direction))
                else:
                    widget.configure(width=original_width, height=original_height)
            
            bounce_step()
        except:
            # Skip animation if widget doesn't support resizing
            pass