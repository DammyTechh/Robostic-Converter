import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from pathlib import Path
import threading
from pypdf import PdfReader, PdfWriter
from pypdf.generic import TextStringObject
import tempfile
import os

class PDFEditorWindow:
    def __init__(self, parent, pdf_file, save_callback=None, colors=None):
        self.parent = parent
        self.pdf_file = pdf_file
        self.save_callback = save_callback
        self.colors = colors or self.get_default_colors()
        
        # PDF data
        self.pdf_reader = None
        self.pdf_writer = None
        self.current_page = 0
        self.total_pages = 0
        self.modified = False
        
        self.create_editor_window()
        self.load_pdf()
        
    def get_default_colors(self):
        return {
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
        
    def create_editor_window(self):
        # Create editor window
        self.editor_window = ctk.CTkToplevel(self.parent)
        self.editor_window.title(f"PDF Editor - {Path(self.pdf_file).name}")
        
        # Adaptive window sizing
        screen_width = self.editor_window.winfo_screenwidth()
        screen_height = self.editor_window.winfo_screenheight()
        
        if screen_width >= 1920:
            window_width, window_height = 1400, 900
        elif screen_width >= 1366:
            window_width, window_height = 1200, 800
        else:
            window_width, window_height = 1000, 700
            
        self.editor_window.geometry(f"{window_width}x{window_height}")
        self.editor_window.minsize(1000, 700)
        self.editor_window.maxsize(1800, 1200)
        self.editor_window.configure(fg_color=self.colors['bg_primary'])
        
        # Make window modal
        self.editor_window.transient(self.parent)
        self.editor_window.grab_set()
        
        # Create main layout
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()
        
        # Center window
        self.center_window()
        
        # Bind close event
        self.editor_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_toolbar(self):
        # Toolbar frame
        self.toolbar = ctk.CTkFrame(
            self.editor_window,
            height=70,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        self.toolbar.pack(fill="x", padx=0, pady=0)
        self.toolbar.pack_propagate(False)
        
        # Toolbar title
        title_label = ctk.CTkLabel(
            self.toolbar,
            text="🛠️ PDF Editor - Advanced Tools",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent_purple']
        )
        title_label.pack(side="left", padx=15, pady=20)
        
        # Toolbar buttons
        buttons_frame = ctk.CTkFrame(self.toolbar, fg_color="transparent")
        buttons_frame.pack(side="right", padx=15, pady=12)
        
        # File operations
        file_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        file_frame.pack(side="left", padx=10)
        
        save_btn = ctk.CTkButton(
            file_frame,
            text="💾 Save",
            command=self.save_pdf,
            width=70,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink'],
            font=ctk.CTkFont(size=11)
        )
        save_btn.pack(side="left", padx=2)
        
        save_as_btn = ctk.CTkButton(
            file_frame,
            text="💾 Save As",
            command=self.save_as_pdf,
            width=80,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_blue'],
            hover_color="#1976d2",
            font=ctk.CTkFont(size=11)
        )
        save_as_btn.pack(side="left", padx=2)
        
        # Edit operations
        edit_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        edit_frame.pack(side="left", padx=10)
        
        rotate_left_btn = ctk.CTkButton(
            edit_frame,
            text="↺ Rotate L",
            command=lambda: self.rotate_page(-90),
            width=80,
            height=32,
            corner_radius=16,
            fg_color=self.colors['success'],
            hover_color="#388e3c",
            font=ctk.CTkFont(size=11)
        )
        rotate_left_btn.pack(side="left", padx=2)
        
        rotate_right_btn = ctk.CTkButton(
            edit_frame,
            text="↻ Rotate R",
            command=lambda: self.rotate_page(90),
            width=80,
            height=32,
            corner_radius=16,
            fg_color=self.colors['success'],
            hover_color="#388e3c",
            font=ctk.CTkFont(size=11)
        )
        rotate_right_btn.pack(side="left", padx=2)
        
        delete_page_btn = ctk.CTkButton(
            edit_frame,
            text="🗑️ Delete",
            command=self.delete_current_page,
            width=70,
            height=32,
            corner_radius=16,
            fg_color=self.colors['error'],
            hover_color="#d32f2f",
            font=ctk.CTkFont(size=11)
        )
        delete_page_btn.pack(side="left", padx=2)
        
        # Tools operations
        tools_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        tools_frame.pack(side="left", padx=10)
        
        merge_btn = ctk.CTkButton(
            tools_frame,
            text="🔗 Merge",
            command=self.merge_pdf,
            width=70,
            height=32,
            corner_radius=16,
            fg_color=self.colors['warning'],
            hover_color="#f57c00",
            font=ctk.CTkFont(size=11)
        )
        merge_btn.pack(side="left", padx=2)
        
        extract_btn = ctk.CTkButton(
            tools_frame,
            text="📤 Extract",
            command=self.extract_pages,
            width=80,
            height=32,
            corner_radius=16,
            fg_color=self.colors['warning'],
            hover_color="#f57c00",
            font=ctk.CTkFont(size=11)
        )
        extract_btn.pack(side="left", padx=2)
        
        # Advanced tools
        advanced_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        advanced_frame.pack(side="left", padx=10)
        
        text_extract_btn = ctk.CTkButton(
            advanced_frame,
            text="📝 Extract Text",
            command=self.extract_all_text,
            width=90,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_blue'],
            hover_color="#1976d2",
            font=ctk.CTkFont(size=11)
        )
        text_extract_btn.pack(side="left", padx=2)
        
        search_btn = ctk.CTkButton(
            advanced_frame,
            text="🔍 Search",
            command=self.search_text,
            width=70,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink'],
            font=ctk.CTkFont(size=11)
        )
        search_btn.pack(side="left", padx=2)
        
    def create_main_content(self):
        # Main content area
        self.content_frame = ctk.CTkFrame(
            self.editor_window,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=8, pady=4)
        
        # Left sidebar for pages
        self.create_sidebar()
        
        # Center area for page preview
        self.create_preview_area()
        
        # Right panel for properties
        self.create_properties_panel()
        
    def create_sidebar(self):
        # Sidebar for page navigation
        self.sidebar = ctk.CTkFrame(
            self.content_frame,
            width=220,
            fg_color=self.colors['bg_secondary'],
            corner_radius=15
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 4))
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="📄 Pages",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        sidebar_title.pack(pady=(12, 8))
        
        # Page navigation
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=12, pady=(0, 8))
        
        prev_btn = ctk.CTkButton(
            nav_frame,
            text="◀",
            command=self.prev_page,
            width=45,
            height=28,
            corner_radius=15,
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink']
        )
        prev_btn.pack(side="left")
        
        self.page_label = ctk.CTkLabel(
            nav_frame,
            text="0 / 0",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_primary']
        )
        self.page_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text="▶",
            command=self.next_page,
            width=45,
            height=28,
            corner_radius=15,
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink']
        )
        next_btn.pack(side="right")
        
        # Pages list
        self.pages_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            label_text="Page List",
            label_fg_color=self.colors['accent_blue']
        )
        self.pages_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
    def create_preview_area(self):
        # Preview area
        self.preview_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_secondary'],
            corner_radius=15
        )
        self.preview_frame.pack(side="left", fill="both", expand=True, padx=4)
        
        # Preview title
        preview_title = ctk.CTkLabel(
            self.preview_frame,
            text="👁️ Page Preview",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        preview_title.pack(pady=(12, 8))
        
        # Preview area (placeholder)
        self.preview_area = ctk.CTkTextbox(
            self.preview_frame,
            fg_color=self.colors['bg_primary'],
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.preview_area.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
    def create_properties_panel(self):
        # Properties panel
        self.properties_panel = ctk.CTkFrame(
            self.content_frame,
            width=280,
            fg_color=self.colors['bg_secondary'],
            corner_radius=15
        )
        self.properties_panel.pack(side="right", fill="y", padx=(4, 0))
        
        # Properties title
        props_title = ctk.CTkLabel(
            self.properties_panel,
            text="📋 Document Properties",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors['accent_blue']
        )
        props_title.pack(pady=(12, 8))
        
        # Document info
        self.doc_info_area = ctk.CTkTextbox(
            self.properties_panel,
            height=180,
            fg_color=self.colors['bg_primary'],
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=9)
        )
        self.doc_info_area.pack(fill="x", padx=12, pady=(0, 12))
        
        # Page operations
        operations_label = ctk.CTkLabel(
            self.properties_panel,
            text="🔧 Page Operations",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['accent_pink']
        )
        operations_label.pack(pady=(8, 8))
        
        # Page size info
        self.page_info_area = ctk.CTkTextbox(
            self.properties_panel,
            height=130,
            fg_color=self.colors['bg_primary'],
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=9)
        )
        self.page_info_area.pack(fill="x", padx=12, pady=(0, 12))
        
        # Advanced operations
        advanced_label = ctk.CTkLabel(
            self.properties_panel,
            text="🎛️ Advanced Tools",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['accent_pink']
        )
        advanced_label.pack(pady=(8, 8))
        
        # Compression
        compress_btn = ctk.CTkButton(
            self.properties_panel,
            text="🗜️ Compress PDF",
            command=self.compress_pdf,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_pink']
        )
        compress_btn.pack(fill="x", padx=12, pady=2)
        
        # Optimize
        optimize_btn = ctk.CTkButton(
            self.properties_panel,
            text="⚡ Optimize",
            command=self.optimize_pdf,
            height=32,
            corner_radius=16,
            fg_color=self.colors['success'],
            hover_color="#388e3c"
        )
        optimize_btn.pack(fill="x", padx=12, pady=2)
        
        # Add watermark
        watermark_btn = ctk.CTkButton(
            self.properties_panel,
            text="💧 Watermark",
            command=self.add_watermark,
            height=32,
            corner_radius=16,
            fg_color=self.colors['accent_blue'],
            hover_color="#1976d2"
        )
        watermark_btn.pack(fill="x", padx=12, pady=2)
        
        # Password protection
        password_btn = ctk.CTkButton(
            self.properties_panel,
            text="🔒 Password Protect",
            command=self.add_password_protection,
            height=32,
            corner_radius=16,
            fg_color=self.colors['error'],
            hover_color="#d32f2f"
        )
        password_btn.pack(fill="x", padx=12, pady=2)
        
    def create_status_bar(self):
        # Status bar
        self.status_bar = ctk.CTkFrame(
            self.editor_window,
            height=35,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="📄 PDF loaded successfully",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(side="left", padx=12, pady=8)
        
        # File info
        self.file_info_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=9),
            text_color=self.colors['text_secondary']
        )
        self.file_info_label.pack(side="right", padx=12, pady=8)
        
    def load_pdf(self):
        """Load the PDF file"""
        try:
            from pypdf import PdfReader, PdfWriter
            
            self.pdf_reader = PdfReader(self.pdf_file)
            self.pdf_writer = PdfWriter()
            
            # Copy all pages to writer
            for page in self.pdf_reader.pages:
                self.pdf_writer.add_page(page)
                
            self.total_pages = len(self.pdf_reader.pages)
            self.current_page = 0 if self.total_pages > 0 else -1
            
            self.update_display()
            self.populate_pages_list()
            self.update_document_info()
            
            self.status_label.configure(text=f"✅ PDF loaded: {self.total_pages} pages")
            self.file_info_label.configure(
                text=f"File: {Path(self.pdf_file).name} | Size: {self.get_file_size()}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{str(e)}")
            self.editor_window.destroy()
            
    def update_display(self):
        """Update the display with current page info"""
        if self.total_pages > 0:
            self.page_label.configure(text=f"{self.current_page + 1} / {self.total_pages}")
            self.update_page_preview()
            self.update_page_info()
        else:
            self.page_label.configure(text="0 / 0")
            
    def populate_pages_list(self):
        """Populate the pages list in sidebar"""
        # Clear existing pages
        for widget in self.pages_frame.winfo_children():
            widget.destroy()
            
        # Add page buttons
        for i in range(self.total_pages):
            page_btn = ctk.CTkButton(
                self.pages_frame,
                text=f"Page {i + 1}",
                command=lambda idx=i: self.goto_page(idx),
                height=28,
                corner_radius=15,
                fg_color=self.colors['bg_tertiary'],
                hover_color=self.colors['hover']
            )
            page_btn.pack(fill="x", pady=2)
            
    def update_page_preview(self):
        """Update the page preview area"""
        if self.current_page >= 0 and self.current_page < self.total_pages:
            page = self.pdf_reader.pages[self.current_page]
            
            # Extract text content
            try:
                text_content = page.extract_text()
                preview_text = f"""
PAGE {self.current_page + 1} CONTENT PREVIEW
{'='*50}

{text_content[:1000]}{'...' if len(text_content) > 1000 else ''}

{'='*50}
Note: This is a text extraction preview.
Use external PDF viewer for full visual preview.
                """
                
                self.preview_area.delete("1.0", tk.END)
                self.preview_area.insert("1.0", preview_text.strip())
                
            except Exception as e:
                self.preview_area.delete("1.0", tk.END)
                self.preview_area.insert("1.0", f"Preview not available:\n{str(e)}")
                
    def update_page_info(self):
        """Update page information panel"""
        if self.current_page >= 0 and self.current_page < self.total_pages:
            page = self.pdf_reader.pages[self.current_page]
            
            # Get page dimensions
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            page_info = f"""Current Page: {self.current_page + 1}
Width: {width:.1f} points
Height: {height:.1f} points
Orientation: {'Landscape' if width > height else 'Portrait'}
Rotation: {page.get('/Rotate', 0)}°

Page Resources:
- Images: Detecting...
- Fonts: Detecting...
- Annotations: Detecting...

Operations Available:
✓ Rotate page
✓ Delete page
✓ Extract text
✓ Compress
            """
            
            self.page_info_area.delete("1.0", tk.END)
            self.page_info_area.insert("1.0", page_info)
            
    def update_document_info(self):
        """Update document information"""
        try:
            info = self.pdf_reader.metadata
            doc_info = f"""DOCUMENT METADATA
{'='*30}

Title: {info.get('/Title', 'Not specified')}
Author: {info.get('/Author', 'Not specified')}
Subject: {info.get('/Subject', 'Not specified')}
Creator: {info.get('/Creator', 'Not specified')}
Producer: {info.get('/Producer', 'Not specified')}
Creation Date: {info.get('/CreationDate', 'Not specified')}

DOCUMENT STATISTICS
{'='*30}

Total Pages: {self.total_pages}
File Size: {self.get_file_size()}
Encrypted: {'Yes' if self.pdf_reader.is_encrypted else 'No'}

EDITING STATUS
{'='*30}

Modified: {'Yes' if self.modified else 'No'}
Changes: {'Pending save' if self.modified else 'None'}
            """
            
            self.doc_info_area.delete("1.0", tk.END)
            self.doc_info_area.insert("1.0", doc_info)
            
        except Exception as e:
            self.doc_info_area.delete("1.0", tk.END)
            self.doc_info_area.insert("1.0", f"Error loading document info:\n{str(e)}")
            
    def get_file_size(self):
        """Get formatted file size"""
        try:
            size = os.path.getsize(self.pdf_file)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return "Unknown"
            
    # Navigation methods
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()
            
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_display()
            
    def goto_page(self, page_index):
        if 0 <= page_index < self.total_pages:
            self.current_page = page_index
            self.update_display()
            
    # Edit operations
    def rotate_page(self, degrees):
        """Rotate current page"""
        if self.current_page >= 0 and self.current_page < self.total_pages:
            try:
                page = self.pdf_writer.pages[self.current_page]
                page.rotate(degrees)
                self.modified = True
                self.update_display()
                self.status_label.configure(text=f"✅ Page {self.current_page + 1} rotated {degrees}°")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rotate page:\n{str(e)}")
                
    def delete_current_page(self):
        """Delete current page"""
        if self.current_page >= 0 and self.current_page < self.total_pages:
            result = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete page {self.current_page + 1}?"
            )
            
            if result:
                try:
                    from pypdf import PdfWriter
                    # Create new writer without the deleted page
                    new_writer = PdfWriter()
                    for i, page in enumerate(self.pdf_writer.pages):
                        if i != self.current_page:
                            new_writer.add_page(page)
                            
                    self.pdf_writer = new_writer
                    self.total_pages -= 1
                    
                    if self.current_page >= self.total_pages:
                        self.current_page = max(0, self.total_pages - 1)
                        
                    self.modified = True
                    self.populate_pages_list()
                    self.update_display()
                    self.status_label.configure(text=f"✅ Page deleted. {self.total_pages} pages remaining")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete page:\n{str(e)}")
                    
    # File operations
    def save_pdf(self):
        """Save PDF to original location"""
        self.save_pdf_to_path(self.pdf_file)
        
    def save_as_pdf(self):
        """Save PDF to new location"""
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if save_path:
            self.save_pdf_to_path(save_path)
            
    def save_pdf_to_path(self, save_path):
        """Save PDF to specified path"""
        try:
            with open(save_path, 'wb') as output_file:
                self.pdf_writer.write(output_file)
                
            self.modified = False
            self.status_label.configure(text=f"✅ PDF saved successfully")
            
            if self.save_callback:
                self.save_callback(save_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")
            
    # Advanced operations
    def merge_pdf(self):
        """Merge with another PDF"""
        from tkinter import filedialog
        from pypdf import PdfReader
        file_path = filedialog.askopenfilename(
            title="Select PDF to merge",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            try:
                merge_reader = PdfReader(file_path)
                
                for page in merge_reader.pages:
                    self.pdf_writer.add_page(page)
                    
                self.total_pages = len(self.pdf_writer.pages)
                self.modified = True
                self.populate_pages_list()
                self.update_display()
                
                self.status_label.configure(text=f"✅ Merged with {Path(file_path).name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to merge PDF:\n{str(e)}")
                
    def extract_pages(self):
        """Extract pages to new PDF"""
        # Simple implementation - extract current page
        if self.current_page >= 0:
            from tkinter import filedialog
            from pypdf import PdfWriter
            save_path = filedialog.asksaveasfilename(
                title="Extract Page To",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if save_path:
                try:
                    extract_writer = PdfWriter()
                    extract_writer.add_page(self.pdf_writer.pages[self.current_page])
                    
                    with open(save_path, 'wb') as output_file:
                        extract_writer.write(output_file)
                        
                    self.status_label.configure(text=f"✅ Page extracted to {Path(save_path).name}")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to extract page:\n{str(e)}")
                    
    def extract_all_text(self):
        """Extract all text from PDF to a text file"""
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Text As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if save_path:
            try:
                all_text = ""
                for i, page in enumerate(self.pdf_reader.pages):
                    all_text += f"\n--- PAGE {i + 1} ---\n"
                    all_text += page.extract_text()
                    all_text += "\n"
                
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(all_text)
                
                self.status_label.configure(text=f"✅ Text extracted to {Path(save_path).name}")
                messagebox.showinfo("Success", f"Text extracted successfully!\nSaved to: {save_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract text:\n{str(e)}")
                
    def search_text(self):
        """Search for text in the PDF"""
        from tkinter import simpledialog
        search_term = simpledialog.askstring("Search PDF", "Enter text to search for:")
        
        if search_term:
            try:
                found_pages = []
                for i, page in enumerate(self.pdf_reader.pages):
                    text = page.extract_text().lower()
                    if search_term.lower() in text:
                        found_pages.append(i + 1)
                
                if found_pages:
                    result_text = f"Found '{search_term}' on pages: {', '.join(map(str, found_pages))}"
                    messagebox.showinfo("Search Results", result_text)
                    # Go to first found page
                    self.goto_page(found_pages[0] - 1)
                else:
                    messagebox.showinfo("Search Results", f"'{search_term}' not found in the document.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Search failed:\n{str(e)}")
                
    def compress_pdf(self):
        """Compress PDF (basic implementation)"""
        try:
            for page in self.pdf_writer.pages:
                page.compress_content_streams()
                
            self.modified = True
            self.status_label.configure(text="✅ PDF compressed")
            messagebox.showinfo("Success", "PDF compression applied! Save the file to see size reduction.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress PDF:\n{str(e)}")
            
    def optimize_pdf(self):
        """Optimize PDF"""
        try:
            # Basic optimization
            for page in self.pdf_writer.pages:
                page.compress_content_streams()
                
            self.modified = True
            self.status_label.configure(text="✅ PDF optimized")
            messagebox.showinfo("Success", "PDF optimization applied! Save the file to see improvements.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to optimize PDF:\n{str(e)}")
            
    def add_watermark(self):
        """Add watermark (placeholder)"""
        messagebox.showinfo(
            "Coming Soon", 
            "Watermark feature will be available in the next update!"
        )
        
    def add_password_protection(self):
        """Add password protection to PDF"""
        from tkinter import simpledialog
        password = simpledialog.askstring("Password Protection", "Enter password for PDF:", show='*')
        
        if password:
            try:
                # Encrypt the PDF
                self.pdf_writer.encrypt(password)
                self.modified = True
                self.status_label.configure(text="✅ Password protection added")
                messagebox.showinfo("Success", "Password protection added! Save the file to apply encryption.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add password protection:\n{str(e)}")
                
    def center_window(self):
        """Center the editor window"""
        self.editor_window.update_idletasks()
        screen_width = self.editor_window.winfo_screenwidth()
        screen_height = self.editor_window.winfo_screenheight()
        
        window_width = self.editor_window.winfo_width()
        window_height = self.editor_window.winfo_height()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.editor_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    def on_close(self):
        """Handle window close"""
        if self.modified:
            from tkinter import messagebox
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            
            if result is True:  # Save
                self.save_pdf()
                self.editor_window.destroy()
            elif result is False:  # Don't save
                self.editor_window.destroy()
            # Cancel - do nothing
        else:
            self.editor_window.destroy()