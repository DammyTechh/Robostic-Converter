import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from pathlib import Path
import webbrowser
from file_converter import FileConverter
from gui_components import *
from pdf_editor_window import PDFEditorWindow

class ConverterApp:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Converter | Space by Dammytech")
        self.root.geometry("1600x1000")
        self.root.resizable(True, True)
        
        # Set minimum and maximum window sizes for flexibility
        self.root.minsize(1200, 800)
        self.root.maxsize(2400, 1600)
        
        # Configure colors
        self.colors = {
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
        }
        
        self.converter = FileConverter()
        self.current_file = None
        self.selected_images = []  # For multi-image PDF conversion
        self.save_location = None
        self.setup_ui()
        
    def setup_ui(self):
        # Configure root
        self.root.configure(fg_color=self.colors['bg_primary'])
        
        # Title frame with enhanced gradient effect
        self.title_frame = ctk.CTkFrame(
            self.root,
            height=100,
            fg_color=self.colors['bg_secondary'],
            corner_radius=25
        )
        self.title_frame.pack(fill="x", padx=15, pady=(15, 8))
        self.title_frame.pack_propagate(False)
        
        # Main title with enhanced 3D effect
        title_label = ctk.CTkLabel(
            self.title_frame,
            text="🚀 CONVERTER | SPACE 🚀",
            font=ctk.CTkFont(family="Arial Black", size=32, weight="bold"),
            text_color=self.colors['accent_purple']
        )
        title_label.pack(pady=(12, 4))
        
        subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="by Dammytech - Advanced File Conversion Suite with PDF Editor",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['accent_pink']
        )
        subtitle_label.pack()
        
        version_label = ctk.CTkLabel(
            self.title_frame,
            text="Version 2.0 - Professional Edition",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['text_secondary']
        )
        version_label.pack()
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Create main panels
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        
        # Status bar
        self.create_status_bar()
        
    def create_left_panel(self):
        # Left panel for file selection and import
        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            width=400,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20
        )
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # File Import Section
        import_section = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        import_section.pack(fill="x", padx=15, pady=15)
        
        section_title = ctk.CTkLabel(
            import_section,
            text="📂 File Import & Selection",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        section_title.pack(pady=(0, 15))
        
        # Enhanced file drop area
        self.file_drop_area = FileDropArea(
            import_section,
            height=100,
            on_file_drop=self.handle_file_import,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=15
        )
        self.file_drop_area.pack(fill="x", pady=(0, 15))
        
        # File path display
        self.file_path_var = tk.StringVar()
        self.file_entry = ctk.CTkEntry(
            import_section,
            textvariable=self.file_path_var,
            placeholder_text="No file selected - Browse or drag & drop...",
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=15,
            state="readonly"
        )
        self.file_entry.pack(fill="x", pady=(0, 10))
        
        # Enhanced browse buttons
        buttons_frame = ctk.CTkFrame(import_section, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)
        
        self.browse_btn = ModernButton(
            buttons_frame,
            text="🔍 Browse Files",
            command=self.browse_file,
            width=160,
            height=40,
            bg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink'],
            corner_radius=20,
            font_size=12
        )
        self.browse_btn.pack(side="left", padx=(0, 10))
        
        # Multi-image button for image to PDF conversion
        self.multi_image_btn = ModernButton(
            buttons_frame,
            text="🖼️ Multi-Image",
            command=self.browse_multiple_images,
            width=120,
            height=40,
            bg_color=self.colors['accent_blue'],
            hover_color="#1976d2",
            corner_radius=20,
            font_size=11
        )
        self.multi_image_btn.pack(side="left", padx=(0, 10))
        
        self.clear_btn = ModernButton(
            buttons_frame,
            text="🗑️ Clear",
            command=self.clear_file,
            width=80,
            height=40,
            bg_color=self.colors['error'],
            hover_color="#d32f2f",
            corner_radius=20,
            font_size=11
        )
        self.clear_btn.pack(side="right")
        
        # File information display
        self.create_file_info_section(self.left_panel)
        
    def create_center_panel(self):
        # Center panel for conversion options
        self.center_panel = ctk.CTkFrame(
            self.main_frame,
            width=350,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20
        )
        self.center_panel.pack(side="left", fill="both", expand=True, padx=8)
        
        # Conversion options
        options_section = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        options_section.pack(fill="both", expand=True, padx=15, pady=15)
        
        options_title = ctk.CTkLabel(
            options_section,
            text="⚙️ Conversion Options",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent_pink']
        )
        options_title.pack(pady=(0, 20))
        
        # Conversion type selection with enhanced styling
        self.conversion_type = ctk.StringVar(value="pdf_to_word")
        
        conversions = [
            ("PDF → Word", "pdf_to_word", "📄→📝", "Convert PDF to editable Word document"),
            ("Word → PDF", "word_to_pdf", "📝→📄", "Convert Word document to PDF"),
            ("Word → PowerPoint", "word_to_ppt", "📝→📊", "Transform Word content to slides"),
            ("PowerPoint → Word", "ppt_to_word", "📊→📝", "Extract presentation text"),
            ("Image → PDF", "image_to_pdf", "🖼️→📄", "Convert images to PDF"),
            ("PDF Editor", "edit_pdf", "✏️📄", "Open advanced PDF editor")
        ]
        
        for i, (display_text, value, icon, description) in enumerate(conversions):
            option_frame = ctk.CTkFrame(
                options_section, 
                fg_color=self.colors['bg_tertiary'],
                corner_radius=12,
                height=55
            )
            option_frame.pack(fill="x", pady=5)
            option_frame.pack_propagate(False)
            
            radio = ctk.CTkRadioButton(
                option_frame,
                text=f"{icon} {display_text}",
                variable=self.conversion_type,
                value=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors['text_primary'],
                fg_color=self.colors['accent_purple'],
                hover_color=self.colors['accent_pink']
            )
            radio.pack(side="left", padx=12, pady=12)
            
            desc_label = ctk.CTkLabel(
                option_frame,
                text=description,
                font=ctk.CTkFont(size=10),
                text_color=self.colors['text_secondary']
            )
            desc_label.pack(side="right", padx=12, pady=12)
        
        # Action buttons
        self.create_action_buttons(options_section)
        
    def create_right_panel(self):
        # Right panel for preview and progress
        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            width=400,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20
        )
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        # Preview section
        preview_section = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        preview_section.pack(fill="both", expand=True, padx=15, pady=15)
        
        preview_title = ctk.CTkLabel(
            preview_section,
            text="👁️ File Preview & Status",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        preview_title.pack(pady=(0, 15))
        
        # Enhanced preview area
        self.preview_area = ctk.CTkTextbox(
            preview_section,
            height=300,
            corner_radius=15,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=self.colors['bg_primary'],
            text_color=self.colors['text_primary']
        )
        self.preview_area.pack(fill="both", expand=True, pady=(0, 20))
        self.update_preview_placeholder()
        
        # Progress section
        self.create_progress_section(preview_section)
        
    def create_file_info_section(self, parent):
        # File information section
        info_section = ctk.CTkFrame(parent, fg_color="transparent")
        info_section.pack(fill="x", padx=15, pady=(0, 15))
        
        info_title = ctk.CTkLabel(
            info_section,
            text="📋 File Information",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        info_title.pack(pady=(0, 10))
        
        self.file_info_area = ctk.CTkTextbox(
            info_section,
            height=120,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=self.colors['bg_primary'],
            text_color=self.colors['text_secondary']
        )
        self.file_info_area.pack(fill="x")
        self.file_info_area.insert("1.0", "No file selected\nFile information will appear here...")
        
    def create_action_buttons(self, parent):
        # Action buttons section
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", pady=20)
        
        # Main convert button
        self.convert_btn = ModernButton(
            actions_frame,
            text="🚀 Start Conversion",
            command=self.start_conversion,
            width=250,
            height=50,
            bg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink'],
            corner_radius=25,
            font_size=14
        )
        self.convert_btn.pack(pady=(0, 15))
        
        # Secondary buttons
        secondary_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        secondary_frame.pack(fill="x")
        
        self.save_location_btn = ModernButton(
            secondary_frame,
            text="💾 Save Location",
            command=self.choose_save_location,
            width=120,
            height=40,
            bg_color=self.colors['bg_primary'],
            hover_color=self.colors['hover'],
            corner_radius=20,
            font_size=11
        )
        self.save_location_btn.pack(side="left", padx=(0, 10))
        
        self.batch_btn = ModernButton(
            secondary_frame,
            text="📦 Batch Mode",
            command=self.open_batch_converter,
            width=120,
            height=40,
            bg_color=self.colors['accent_blue'],
            hover_color="#1976d2",
            corner_radius=20,
            font_size=11
        )
        self.batch_btn.pack(side="right")
        
    def create_progress_section(self, parent):
        # Progress section
        progress_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        progress_frame.pack(fill="x", pady=10)
        
        progress_title = ctk.CTkLabel(
            progress_frame,
            text="📊 Conversion Progress",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        )
        progress_title.pack(pady=(10, 5))
        
        # Enhanced progress bar
        self.progress = AnimatedProgressBar(
            progress_frame,
            width=350,
            height=25,
            corner_radius=12,
            progress_color=self.colors['accent_purple']
        )
        self.progress.pack(padx=15, pady=(0, 5))
        
        # Progress percentage
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary']
        )
        self.progress_label.pack(pady=(0, 10))
        
    def create_status_bar(self):
        # Enhanced status bar
        self.status_frame = ctk.CTkFrame(
            self.root,
            height=60,
            fg_color=self.colors['bg_secondary'],
            corner_radius=15
        )
        self.status_frame.pack(fill="x", padx=15, pady=(8, 15))
        self.status_frame.pack_propagate(False)
        
        # Status indicator
        self.status_indicator = StatusIndicator(self.status_frame)
        self.status_indicator.pack(side="left", padx=15, pady=12)
        self.status_indicator.set_status("Ready - Select a file to begin", "info")
        
        # Contact and info section
        contact_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        contact_frame.pack(side="right", padx=15, pady=8)
        
        contact_title = ctk.CTkLabel(
            contact_frame,
            text="Support & Contact:",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=self.colors['text_secondary']
        )
        contact_title.pack()
        
        buttons_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        buttons_frame.pack(pady=5)
        
        website_btn = ctk.CTkButton(
            buttons_frame,
            text="🌐 dammytech.netlify.app",
            command=lambda: webbrowser.open("https://dammytech.netlify.app"),
            width=160,
            height=28,
            corner_radius=15,
            fg_color="transparent",
            text_color=self.colors['accent_purple'],
            hover_color=self.colors['hover'],
            font=ctk.CTkFont(size=9)
        )
        website_btn.pack(side="left", padx=2)
        
        support_btn = ctk.CTkButton(
            buttons_frame,
            text="📧 Support",
            command=lambda: webbrowser.open("mailto:petersdamilare5@gmail.com"),
            width=70,
            height=28,
            corner_radius=15,
            fg_color=self.colors['accent_pink'],
            hover_color=self.colors['accent_purple'],
            font=ctk.CTkFont(size=9)
        )
        support_btn.pack(side="right", padx=2)
        
    def handle_file_import(self, files):
        """Handle imported files from drag & drop or browse"""
        if files and len(files) > 0:
            file_path = files[0] if isinstance(files, list) else files
            self.current_file = file_path
            self.file_path_var.set(file_path)
            self.update_file_info(file_path)
            self.update_preview_with_file(file_path)
            self.status_indicator.set_status(f"File loaded: {Path(file_path).name}", "success")
            
    def browse_file(self):
        """Enhanced file browser with better file type filtering"""
        file_types = [
            ("All Supported", "*.pdf;*.docx;*.doc;*.pptx;*.ppt;*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx;*.doc"),
            ("PowerPoint files", "*.pptx;*.ppt"),
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select file to convert - Converter | Space by Dammytech",
            filetypes=file_types
        )
        
        if filename:
            self.handle_file_import(filename)
            
    def browse_multiple_images(self):
        """Browse and select multiple images for PDF conversion"""
        file_types = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
            ("All files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select multiple images for PDF conversion",
            filetypes=file_types
        )
        
        if filenames:
            self.selected_images = list(filenames)
            self.current_file = None  # Clear single file selection
            self.file_path_var.set(f"{len(filenames)} images selected for PDF conversion")
            self.update_multi_image_info()
            self.status_indicator.set_status(f"{len(filenames)} images selected", "success")
            
    def update_multi_image_info(self):
        """Update file info for multiple images"""
        if self.selected_images:
            total_size = sum(os.path.getsize(img) for img in self.selected_images)
            info_text = f"""Multi-Image PDF Conversion
Images Selected: {len(self.selected_images)}
Total Size: {self.format_file_size(total_size)}

Selected Images:"""
            
            for i, img_path in enumerate(self.selected_images[:10], 1):  # Show first 10
                info_text += f"\n{i}. {Path(img_path).name}"
            
            if len(self.selected_images) > 10:
                info_text += f"\n... and {len(self.selected_images) - 10} more images"
            
            self.file_info_area.delete("1.0", tk.END)
            self.file_info_area.insert("1.0", info_text)
            
            # Update preview
            preview_text = f"""
🖼️ MULTI-IMAGE PDF CONVERSION
{'='*50}
📁 Images Selected: {len(self.selected_images)}
📏 Total Size: {self.format_file_size(total_size)}

⚙️ CONVERSION SETTINGS
{'='*50}
🎯 Operation: Multiple Images → PDF
📤 Output: Single PDF document
💾 Save Location: {self.save_location or 'Same as first image'}

✨ STATUS
{'='*50}
✅ Ready for multi-image PDF conversion

🚀 Click 'Start Conversion' to create PDF!
            """
            
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.insert("1.0", preview_text.strip())
            
    def clear_file(self):
        """Clear selected file"""
        self.current_file = None
        self.selected_images = []
        self.file_path_var.set("")
        self.file_info_area.delete("1.0", tk.END)
        self.file_info_area.insert("1.0", "No file selected\nFile information will appear here...")
        self.update_preview_placeholder()
        self.status_indicator.set_status("File cleared - Ready for new selection", "info")
        
    def update_file_info(self, filepath):
        """Update file information display"""
        try:
            file_info = self.converter.get_file_info(filepath)
            info_text = f"""File: {file_info['name']}
Size: {self.format_file_size(file_info['size'])}
Type: {file_info['type']}
Format: {file_info['extension'].upper()}
Modified: {file_info['modified'].strftime("%Y-%m-%d %H:%M:%S")}

Additional Info:"""
            
            if file_info['type'] == 'PDF Document':
                info_text += f"\nPages: {file_info.get('pages', 'Unknown')}"
                info_text += f"\nEncrypted: {'Yes' if file_info.get('encrypted', False) else 'No'}"
            elif 'Word' in file_info['type']:
                info_text += f"\nParagraphs: {file_info.get('paragraphs', 'Unknown')}"
            elif 'PowerPoint' in file_info['type']:
                info_text += f"\nSlides: {file_info.get('slides', 'Unknown')}"
            elif 'Image' in file_info['type']:
                info_text += f"\nDimensions: {file_info.get('dimensions', 'Unknown')}"
                info_text += f"\nColor Mode: {file_info.get('mode', 'Unknown')}"
            
            self.file_info_area.delete("1.0", tk.END)
            self.file_info_area.insert("1.0", info_text)
            
        except Exception as e:
            self.file_info_area.delete("1.0", tk.END)
            self.file_info_area.insert("1.0", f"Error reading file info:\n{str(e)}")
            
    def update_preview_with_file(self, filepath):
        """Update preview area with file-specific information"""
        conversion_type = self.conversion_type.get()
        file_path = Path(filepath)
        
        preview_text = f"""
🔍 SELECTED FILE
{'='*50}
📁 File: {file_path.name}
📂 Location: {file_path.parent}
📏 Size: {self.format_file_size(os.path.getsize(filepath))}
📅 Modified: {self.get_file_modified_time(filepath)}

⚙️ CONVERSION SETTINGS
{'='*50}
🎯 Selected Operation: {self.get_conversion_display_name()}
📤 Output Format: {self.get_output_format()}
💾 Save Location: {self.save_location or 'Same as source file'}

✨ STATUS
{'='*50}
{self.get_conversion_status_message()}

🚀 Ready to process your file!
Click 'Start Conversion' to begin.
        """
        
        self.preview_area.delete("1.0", tk.END)
        self.preview_area.insert("1.0", preview_text.strip())
        
    def update_preview_placeholder(self):
        """Update preview with placeholder content"""
        placeholder_text = """
📋 FILE PREVIEW
{'='*50}
No file selected yet.

Please:
1. 📂 Browse for a file, or
2. 🔥 Drag & drop a file into the drop area

Supported formats:
• PDF Documents
• Word Documents (.docx, .doc)
• PowerPoint Presentations (.pptx, .ppt)
• Images (PNG, JPG, GIF, BMP, TIFF, WebP)

Select a conversion type and file to get started!
        """
        
        self.preview_area.delete("1.0", tk.END)
        self.preview_area.insert("1.0", placeholder_text.strip())
        
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
        
    def get_file_modified_time(self, filepath):
        """Get formatted file modification time"""
        import datetime
        timestamp = os.path.getmtime(filepath)
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
    def get_conversion_display_name(self):
        """Get display name for conversion type"""
        conversion_names = {
            "pdf_to_word": "PDF to Word Document",
            "word_to_pdf": "Word Document to PDF",
            "word_to_ppt": "Word to PowerPoint Presentation",
            "ppt_to_word": "PowerPoint to Word Document",
            "image_to_pdf": "Image to PDF Document",
            "edit_pdf": "Advanced PDF Editor"
        }
        return conversion_names.get(self.conversion_type.get(), "Unknown Operation")
        
    def get_output_format(self):
        """Get output format for conversion"""
        output_formats = {
            "pdf_to_word": ".docx",
            "word_to_pdf": ".pdf",
            "word_to_ppt": ".pptx",
            "ppt_to_word": ".docx",
            "image_to_pdf": ".pdf",
            "edit_pdf": ".pdf"
        }
        return output_formats.get(self.conversion_type.get(), "Unknown")
        
    def get_conversion_status_message(self):
        """Get status message for current conversion setup"""
        if not self.current_file and not self.selected_images:
            return "⚠️ No file selected"
        
        conversion = self.conversion_type.get()
        
        # Handle multi-image conversion
        if self.selected_images and conversion == "image_to_pdf":
            return "✅ Multiple images ready for PDF conversion"
        
        if not self.current_file:
            return "⚠️ No file selected"
            
        file_ext = Path(self.current_file).suffix.lower()
        
        # Validate file type for conversion
        valid_combinations = {
            "pdf_to_word": [".pdf"],
            "word_to_pdf": [".docx", ".doc"],
            "word_to_ppt": [".docx", ".doc"],
            "ppt_to_word": [".pptx", ".ppt"],
            "image_to_pdf": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
            "edit_pdf": [".pdf"]
        }
        
        if file_ext in valid_combinations.get(conversion, []):
            return "✅ File and conversion type are compatible"
        else:
            return f"❌ Selected file type ({file_ext}) is not compatible with {self.get_conversion_display_name()}"
            
    def choose_save_location(self):
        """Choose save location for converted files"""
        save_path = filedialog.askdirectory(
            title="Choose save location - Converter | Space by Dammytech"
        )
        if save_path:
            self.save_location = save_path
            self.status_indicator.set_status(f"Save location: {Path(save_path).name}", "success")
            if self.current_file or self.selected_images:
                self.update_preview_with_file(self.current_file)
                
    def start_conversion(self):
        """Start the conversion process"""
        if not self.current_file and not self.selected_images:
            messagebox.showerror("No File Selected", "Please select a file to convert first!")
            return
            
        conversion_type = self.conversion_type.get()
        
        # Special handling for PDF editor
        if conversion_type == "edit_pdf":
            self.open_pdf_editor()
            return
            
        # Handle multi-image conversion
        if self.selected_images and conversion_type == "image_to_pdf":
            if not self.save_location:
                self.save_location = Path(self.selected_images[0]).parent
        else:
            # Validate single file conversion
            if not self.current_file:
                messagebox.showerror("No File Selected", "Please select a file to convert!")
                return
                
            file_ext = Path(self.current_file).suffix.lower()
            if not self.validate_conversion(file_ext, conversion_type):
                messagebox.showerror(
                    "Invalid File Type", 
                    f"Selected file type ({file_ext}) is not compatible with {self.get_conversion_display_name()}"
                )
                return
            
            if not self.save_location:
                self.save_location = Path(self.current_file).parent
            
        # Start conversion in separate thread
        self.conversion_thread = threading.Thread(target=self.perform_conversion)
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
        
    def validate_conversion(self, file_ext, conversion_type):
        """Validate if file extension is compatible with conversion type"""
        valid_combinations = {
            "pdf_to_word": [".pdf"],
            "word_to_pdf": [".docx", ".doc"],
            "word_to_ppt": [".docx", ".doc"],
            "ppt_to_word": [".pptx", ".ppt"],
            "image_to_pdf": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]
        }
        
        return file_ext in valid_combinations.get(conversion_type, [])
        
    def open_pdf_editor(self):
        """Open the dedicated PDF editor window"""
        if not self.current_file or not Path(self.current_file).suffix.lower() == '.pdf':
            messagebox.showerror("Invalid File", "Please select a PDF file to edit!")
            return
            
        try:
            # Create and open PDF editor window
            editor_window = PDFEditorWindow(
                parent=self.root,
                pdf_file=self.current_file,
                save_callback=self.on_pdf_saved,
                colors=self.colors
            )
            self.status_indicator.set_status("PDF Editor opened", "info")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF editor:\n{str(e)}")
            
    def on_pdf_saved(self, saved_path):
        """Callback when PDF is saved from editor"""
        self.status_indicator.set_status(f"PDF saved: {Path(saved_path).name}", "success")
        messagebox.showinfo("Success", f"PDF successfully saved to:\n{saved_path}")
        
    def perform_conversion(self):
        """Perform the actual conversion"""
        try:
            self.status_indicator.set_status("Processing... Please wait", "processing")
            self.progress.animate_to(0.1)
            self.progress_label.configure(text="10%")
            
            conversion_type = self.conversion_type.get()
            
            # Update progress
            self.progress.animate_to(0.3)
            self.progress_label.configure(text="30%")
            
            # Perform conversion based on type
            if conversion_type == "image_to_pdf" and self.selected_images:
                # Multi-image conversion
                output_file = self.converter.multi_image_to_pdf(self.selected_images, self.save_location)
            else:
                # Single file conversion
                input_file = self.current_file
                if conversion_type == "pdf_to_word":
                    output_file = self.converter.pdf_to_word(input_file, self.save_location)
                elif conversion_type == "word_to_pdf":
                    output_file = self.converter.word_to_pdf(input_file, self.save_location)
                elif conversion_type == "word_to_ppt":
                    output_file = self.converter.word_to_ppt(input_file, self.save_location)
                elif conversion_type == "ppt_to_word":
                    output_file = self.converter.ppt_to_word(input_file, self.save_location)
                elif conversion_type == "image_to_pdf":
                    output_file = self.converter.image_to_pdf(input_file, self.save_location)
                
            self.progress.animate_to(0.9)
            self.progress_label.configure(text="90%")
            
            # Complete
            self.progress.animate_to(1.0)
            self.progress_label.configure(text="100%")
            self.status_indicator.set_status(f"Conversion completed successfully!", "success")
            
            # Show completion dialog with enhanced options
            self.show_completion_dialog(output_file)
            
        except Exception as e:
            self.progress.animate_to(0)
            self.progress_label.configure(text="0%")
            self.status_indicator.set_status(f"Conversion failed: {str(e)}", "error")
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n\n{str(e)}")
            
    def show_completion_dialog(self, output_file):
        """Show enhanced completion dialog"""
        file_name = Path(output_file).name
        file_size = self.format_file_size(os.path.getsize(output_file))
        
        result = messagebox.askyesnocancel(
            "Conversion Complete! 🎉",
            f"File successfully converted!\n\n"
            f"📄 Output: {file_name}\n"
            f"📏 Size: {file_size}\n"
            f"📂 Location: {Path(output_file).parent}\n\n"
            f"Would you like to:\n"
            f"• YES - Open the output folder\n"
            f"• NO - Convert another file\n"
            f"• CANCEL - Do nothing"
        )
        
        if result is True:  # Yes - Open folder
            self.open_file_location(output_file)
        elif result is False:  # No - Convert another
            self.clear_file()
            
    def open_file_location(self, file_path):
        """Open file location in system file manager"""
        try:
            import subprocess
            import sys
            if os.name == 'nt':  # Windows
                os.startfile(Path(file_path).parent)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', Path(file_path).parent])
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not open file location:\n{str(e)}")
            
    def open_batch_converter(self):
        """Open batch conversion window (placeholder for future implementation)"""
        messagebox.showinfo(
            "Coming Soon", 
            "Batch conversion feature will be available in the next update!\n\n"
            "Stay tuned for more awesome features."
        )
        
    def run(self):
        """Run the application"""
        # Center window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Adaptive window sizing based on screen resolution
        if screen_width >= 1920:  # Large screens
            window_width, window_height = 1600, 1000
        elif screen_width >= 1366:  # Medium screens
            window_width, window_height = 1400, 900
        else:  # Small screens
            window_width, window_height = 1200, 800
            
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Set minimum and maximum window sizes for flexibility
        self.root.minsize(1200, 800)
        self.root.maxsize(2400, 1600)
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ConverterApp()
    app.run()