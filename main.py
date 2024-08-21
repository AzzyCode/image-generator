import requests
import io
import tkinter as tk
import os

from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from ttkbootstrap import Style
from dotenv import load_dotenv


load_dotenv()

CATEGORY_OPTIONS = ["Choose Category",
                    "Nature",
                    "Technology",
                    "Food",
                    "Travel",
                    "Animals",
                    "Science"]

def create_gui(category_options):
    global category_var, generate_btn, download_btn, label
    
    root = tk.Tk()
    root.title("Image Generator")
    root.geometry("700x500")
    root.config(bg="white")
    root.resizable(False, False)
    style = Style(theme="sandstone")
    
    category_var = tk.StringVar(value="Choose Category")      
    category_dropdown = ttk.OptionMenu(root, category_var, *category_options, command=enable_button)
    category_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    category_dropdown.config(width=14)
    
    generate_btn = ttk.Button(text="Generate Image", state="disabled", command=display_image)
    generate_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    download_btn = ttk.Button(text="Dowload Image", state="disabled", command=lambda: download_image())
    download_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")    
    
    label_text = tk.StringVar(value="Waiting for image category")
    label = tk.Label(root, textvariable=label_text, background="white")
    label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    
    root.columnconfigure([0, 1, 2], weight=1)
    root.rowconfigure(1, weight=1)
    root.mainloop()    


def display_image():
    global img
    
    category = category_var.get()
    if category == "Choose Category":
        return
    
    label.config(text="Loading image...", image="")
    
    try:
        KEY = os.getenv('API_KEY')
        URL = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id={KEY}"
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        
        img_data = requests.get(data["urls"]["regular"]).content
        img = Image.open(io.BytesIO(img_data)).resize((600, 400), resample=Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        label.config(image=photo)
        label.image = photo
        
        download_btn.config(state="normal")
    except Exception as e:
        print(f"An error occurred: {e}")
        

def download_image():
    if img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img.save(file_path)
            
            
def enable_button(*args):
    generate_btn.config(state="normal" if category_var.get() != "Choose Category" else "disabled")

if __name__ == "__main__":
    create_gui(CATEGORY_OPTIONS)

