import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool - Hide & Extract Messages")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = tk.StringVar()
        self.original_image = None
        self.modified_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main container with scrollbar
        canvas = tk.Canvas(self.root, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main frame inside scrollable area
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Steganography Tool", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Image selection frame
        image_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="5")
        image_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        image_frame.columnconfigure(1, weight=1)
        
        ttk.Label(image_frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(image_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, 
                                                                           sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(image_frame, text="Browse", command=self.browse_image).grid(row=0, column=2, pady=5)
        
        # Image preview frame with fixed height
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="5")
        preview_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        
        # Create a frame with fixed height for image preview
        image_container = tk.Frame(preview_frame, height=250, bg="white")
        image_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        image_container.pack_propagate(False)  # Don't let children control the size
        image_container.columnconfigure(0, weight=1)
        image_container.rowconfigure(0, weight=1)
        
        self.image_label = ttk.Label(image_container, text="No image selected")
        self.image_label.grid(row=0, column=0)
        
        # Notebook for hide/extract tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Hide message tab
        hide_frame = ttk.Frame(notebook, padding="10")
        notebook.add(hide_frame, text="Hide Message")
        self.setup_hide_tab(hide_frame)
        
        # Extract message tab
        extract_frame = ttk.Frame(notebook, padding="10")
        notebook.add(extract_frame, text="Extract Message")
        self.setup_extract_tab(extract_frame)
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux
    
    def setup_hide_tab(self, parent):
        # Configure parent to expand properly
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Message input
        ttk.Label(parent, text="Secret Message:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.message_text = scrolledtext.ScrolledText(parent, height=6, width=70)
        self.message_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Password frame
        password_frame = ttk.Frame(parent)
        password_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        password_frame.columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="Password (optional):").grid(row=0, column=0, sticky=tk.W)
        self.hide_password = ttk.Entry(password_frame, show="*", width=30)
        self.hide_password.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Hide Message", 
                  command=self.hide_message, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Save Image", 
                  command=self.save_image, width=15).pack(side=tk.LEFT)
    
    def setup_extract_tab(self, parent):
        # Configure parent to expand properly
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Password frame
        password_frame = ttk.Frame(parent)
        password_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        password_frame.columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="Password (if used):").grid(row=0, column=0, sticky=tk.W)
        self.extract_password = ttk.Entry(password_frame, show="*", width=30)
        self.extract_password.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Extract button
        ttk.Button(parent, text="Extract Message", 
                  command=self.extract_message, width=15).grid(row=1, column=0, pady=(0, 15))
        
        # Extracted message display
        ttk.Label(parent, text="Extracted Message:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        self.extracted_text = scrolledtext.ScrolledText(parent, height=8, width=70, state='disabled')
        self.extracted_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path.set(file_path)
            self.load_image_preview()
    
    def load_image_preview(self):
        try:
            # Load and resize image for preview
            image = Image.open(self.image_path.get())
            self.original_image = image.copy()
            
            # Resize for preview with fixed maximum size to prevent UI issues
            max_size = (200, 200)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def generate_key_from_password(self, password):
        """Generate encryption key from password"""
        password_bytes = password.encode()
        salt = b'steganography_salt'  # In production, use random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def text_to_binary(self, text):
        """Convert text to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    def binary_to_text(self, binary):
        """Convert binary string to text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def hide_message(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide!")
            return
        
        try:
            # Encrypt message if password provided
            password = self.hide_password.get()
            if password:
                key = self.generate_key_from_password(password)
                fernet = Fernet(key)
                message = fernet.encrypt(message.encode()).decode()
            
            # Add delimiter to mark end of message
            message += "###END###"
            
            # Convert message to binary
            binary_message = self.text_to_binary(message)
            
            # Check if image can hold the message
            image = self.original_image.copy()
            pixels = list(image.getdata())
            
            if len(binary_message) > len(pixels) * 3:  # RGB channels
                messagebox.showerror("Error", "Message too long for this image!")
                return
            
            # Hide message in LSB of pixels
            data_index = 0
            new_pixels = []
            
            for pixel in pixels:
                if isinstance(pixel, tuple):
                    r, g, b = pixel[:3]
                    alpha = pixel[3] if len(pixel) == 4 else None
                else:
                    # Grayscale
                    r = g = b = pixel
                    alpha = None
                
                # Modify LSB of each color channel
                if data_index < len(binary_message):
                    r = (r & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if data_index < len(binary_message):
                    g = (g & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if data_index < len(binary_message):
                    b = (b & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if alpha is not None:
                    new_pixels.append((r, g, b, alpha))
                else:
                    new_pixels.append((r, g, b))
            
            # Create new image with hidden message
            self.modified_image = Image.new(image.mode, image.size)
            self.modified_image.putdata(new_pixels)
            
            messagebox.showinfo("Success", "Message hidden successfully! Click 'Save Image' to save.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide message: {str(e)}")
    
    def save_image(self):
        if not self.modified_image:
            messagebox.showerror("Error", "No modified image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.modified_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def extract_message(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        try:
            # Extract binary data from LSB of pixels
            image = Image.open(self.image_path.get())
            pixels = list(image.getdata())
            
            binary_message = ""
            
            for pixel in pixels:
                if isinstance(pixel, tuple):
                    r, g, b = pixel[:3]
                else:
                    r = g = b = pixel
                
                # Extract LSB from each color channel
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)
            
            # Convert binary to text
            message = self.binary_to_text(binary_message)
            
            # Find the end delimiter
            end_marker = "###END###"
            if end_marker in message:
                message = message[:message.index(end_marker)]
            else:
                raise ValueError("No hidden message found or message corrupted")
            
            # Decrypt if password provided
            password = self.extract_password.get()
            if password:
                try:
                    key = self.generate_key_from_password(password)
                    fernet = Fernet(key)
                    message = fernet.decrypt(message.encode()).decode()
                except Exception:
                    messagebox.showerror("Error", "Wrong password or message not encrypted!")
                    return
            
            # Display extracted message
            self.extracted_text.config(state='normal')
            self.extracted_text.delete(1.0, tk.END)
            self.extracted_text.insert(1.0, message)
            self.extracted_text.config(state='disabled')
            
            messagebox.showinfo("Success", "Message extracted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")

def main():
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()