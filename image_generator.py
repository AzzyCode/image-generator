import requests
import io
import tkinter as tk
import os
import logging

from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

CATEGORY_OPTIONS = ["Choose Category",
                    "Nature", "Technology", "Food",
                    "Travel", "Animals", "Science"]

class ImageGenerator:
    def __init__(self, category_options):
        self.category_options = category_options
        self.api_key = os.getenv('API_KEY')
        
        if not self.api_key:
            logger.error("API key is missing.")
            raise ValueError("API key not found. Please set API_KEY in the environment variables.")
        
        self.img = None
        self.setup_gui()
        
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Image Generator")
        self.root.geometry("700x500")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        style = Style(theme="sandstone")
        
        self.category_var = tk.StringVar(value="Choose Category")      
        category_dropdown = ttk.OptionMenu(self.root, self.category_var, *self.category_options, command=self.enable_button)
        category_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        category_dropdown.config(width=14)
        
        self.generate_btn = ttk.Button(text="Generate Image", state="disabled", command=self.display_image)
        self.generate_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.download_btn = ttk.Button(text="Download Image", state="disabled", command=self.download_image)
        self.download_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")    
        
        self.label_text = tk.StringVar(value="Waiting for image category")
        self.label = tk.Label(self.root, textvariable=self.label_text, background="white")
        self.label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.root.columnconfigure([0, 1, 2], weight=1)
        self.root.rowconfigure(1, weight=1)  

        self.root.update_idletasks()
        
        
    def display_image(self):
        category = self.category_var.get()
        if category == "Choose Category":
            return
        
        self.label.config(text="Loading image...", image="")
        
        try:
            img_data = self.fetch_image_data(category) 
            self.img = self.process_image(img_data)
            
            photo = ImageTk.PhotoImage(self.img)
            self.label.config(image=photo)
            self.label.image = photo
            
            self.download_btn.config(state="normal")
        except Exception as e:
            logger.error("An error occurred: %s", e)
            messagebox.showerror("Error", "Failed to load image. Please try again.")
        
        
    def fetch_image_data(self, category):
        URL = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id={self.api_key}"
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return requests.get(data["urls"]["regular"]).content
    
    
    def process_image(self, img_data):
        return Image.open(io.BytesIO(img_data)).resize((600, 400), resample=Image.LANCZOS)
    
    
    def download_image(self):
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.img.save(file_path)
            else:
                logger.error("Save dialog canceled by user.")
            
            
    def enable_button(self, *args):
        self.generate_btn.config(state="normal" if self.category_var.get() != "Choose Category" else "disabled")


if __name__ == "__main__":
    app = ImageGenerator(CATEGORY_OPTIONS)
    app.root.mainloop()
