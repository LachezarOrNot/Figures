import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import math

class ShapeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Generator - Генератор на Фигури")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        self.rectangle_running = False
        self.triangle_running = False
        self.circle_running = False
        
        #Нишки
        self.rectangle_thread = None
        self.triangle_thread = None
        self.circle_thread = None
        
        self.rectangle_count = 0
        self.triangle_count = 0
        self.circle_count = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        title_label = tk.Label(
            self.root, 
            text="Генератор на фигури", 
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Start.TButton', font=('Arial', 11, 'bold'))
        style.configure('Stop.TButton', font=('Arial', 11, 'bold'))
        
        rect_frame = tk.Frame(button_frame, bg='#2c3e50')
        rect_frame.grid(row=0, column=0, padx=15, pady=5)
        
        self.rect_btn = ttk.Button(
            rect_frame, 
            text="🟦 Правоъгълник", 
            command=self.toggle_rectangle,
            style='Start.TButton',
            width=15
        )
        self.rect_btn.pack(pady=2)
        
        self.rect_status = tk.Label(
            rect_frame, 
            text="Спряно", 
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#e74c3c'
        )
        self.rect_status.pack()
        
        self.rect_counter = tk.Label(
            rect_frame, 
            text="Брой: 0", 
            font=("Arial", 8),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.rect_counter.pack()
        
        tri_frame = tk.Frame(button_frame, bg='#2c3e50')
        tri_frame.grid(row=0, column=1, padx=15, pady=5)
        
        self.tri_btn = ttk.Button(
            tri_frame, 
            text="🔺 Триъгълник", 
            command=self.toggle_triangle,
            style='Start.TButton',
            width=15
        )
        self.tri_btn.pack(pady=2)
        
        self.tri_status = tk.Label(
            tri_frame, 
            text="Спряно", 
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#e74c3c'
        )
        self.tri_status.pack()
        
        self.tri_counter = tk.Label(
            tri_frame, 
            text="Брой: 0", 
            font=("Arial", 8),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.tri_counter.pack()
        
        circle_frame = tk.Frame(button_frame, bg='#2c3e50')
        circle_frame.grid(row=0, column=2, padx=15, pady=5)
        
        self.circle_btn = ttk.Button(
            circle_frame, 
            text="🔴 Кръг", 
            command=self.toggle_circle,
            style='Start.TButton',
            width=15
        )
        self.circle_btn.pack(pady=2)
        
        self.circle_status = tk.Label(
            circle_frame, 
            text="Спряно", 
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#e74c3c'
        )
        self.circle_status.pack()
        
        self.circle_counter = tk.Label(
            circle_frame, 
            text="Брой: 0", 
            font=("Arial", 8),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.circle_counter.pack()
        
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        self.stop_all_btn = ttk.Button(
            control_frame, 
            text="⏹️ Спри всички", 
            command=self.stop_all,
            style='Stop.TButton',
            width=20
        )
        self.stop_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            control_frame, 
            text="🗑️ Изчисти", 
            command=self.clear_canvas,
            style='Stop.TButton',
            width=20
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        canvas_frame = tk.Frame(self.root, bg='#34495e', relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='#ecf0f1',
            width=800,
            height=450,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=5)
        
        self.info_label = tk.Label(
            info_frame,
            text="Готово за генериране на фигури! Натиснете бутон за започване.",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.info_label.pack()
        
    def get_canvas_size(self):
        self.canvas.update()
        return self.canvas.winfo_width(), self.canvas.winfo_height()
    
    def generate_random_color(self, base_colors):
        return random.choice(base_colors)
    
    def toggle_rectangle(self):
        if not self.rectangle_running:
            self.start_rectangle()
        else:
            self.stop_rectangle()
    
    def start_rectangle(self):
        self.rectangle_running = True
        self.rect_btn.configure(text="⏸️ Спри правоъгълник")
        self.rect_status.configure(text="Активно", fg='#27ae60')

        #Нишки
        self.rectangle_thread = threading.Thread(target=self.rectangle_generator, daemon=True)
        self.rectangle_thread.start()
    
    def stop_rectangle(self):
        self.rectangle_running = False
        self.rect_btn.configure(text="🟦 Правоъгълник")
        self.rect_status.configure(text="Спряно", fg='#e74c3c')
    
    def rectangle_generator(self):
        colors = ['#3498db', '#2980b9', '#5dade2', '#85c1e9', '#aed6f1']
        
        while self.rectangle_running:
            try:
                width, height = self.get_canvas_size()
                
                rect_width = random.randint(20, min(150, width//3))
                rect_height = random.randint(20, min(150, height//3))
                
                x = random.randint(0, max(0, width - rect_width))
                y = random.randint(0, max(0, height - rect_height))
                
                color = self.generate_random_color(colors)
                
                self.canvas.create_rectangle(
                    x, y, x + rect_width, y + rect_height,
                    fill=color, outline='#2c3e50', width=2
                )
                
                self.rectangle_count += 1
                self.rect_counter.configure(text=f"Брой: {self.rectangle_count}")
                
                time.sleep(3)
            except Exception as e:
                print(f"Грешка в rectangle_generator: {e}")
                break
    
    def toggle_triangle(self):
        if not self.triangle_running:
            self.start_triangle()
        else:
            self.stop_triangle()
    
    def start_triangle(self):
        self.triangle_running = True
        self.tri_btn.configure(text="⏸️ Спри триъгълник")
        self.tri_status.configure(text="Активно", fg='#27ae60')
        
        #Нишки
        self.triangle_thread = threading.Thread(target=self.triangle_generator, daemon=True)
        self.triangle_thread.start()
    
    def stop_triangle(self):
        self.triangle_running = False
        self.tri_btn.configure(text="🔺 Триъгълник")
        self.tri_status.configure(text="Спряно", fg='#e74c3c')
    
    def triangle_generator(self):
        colors = ['#e74c3c', '#c0392b', '#ec7063', '#f1948a', '#fadbd8']
        
        while self.triangle_running:
            try:
                width, height = self.get_canvas_size()
                
                size = random.randint(20, min(120, width//4, height//4))
                
                center_x = random.randint(size, width - size)
                center_y = random.randint(size, height - size)
                
                points = [
                    center_x, center_y - size,  
                    center_x - size, center_y + size//2, 
                    center_x + size, center_y + size//2   
                ]
                
                color = self.generate_random_color(colors)
                
                self.canvas.create_polygon(
                    points, fill=color, outline='#2c3e50', width=2
                )
                
                self.triangle_count += 1
                self.tri_counter.configure(text=f"Брой: {self.triangle_count}")
                
                time.sleep(2)
            except Exception as e:
                print(f"Грешка в triangle_generator: {e}")
                break
    
    def toggle_circle(self):
        if not self.circle_running:
            self.start_circle()
        else:
            self.stop_circle()
    
    def start_circle(self):
        self.circle_running = True
        self.circle_btn.configure(text="⏸️ Спри кръг")
        self.circle_status.configure(text="Активно", fg='#27ae60')

        #Нишки
        self.circle_thread = threading.Thread(target=self.circle_generator, daemon=True)
        self.circle_thread.start()
    
    def stop_circle(self):
        self.circle_running = False
        self.circle_btn.configure(text="🔴 Кръг")
        self.circle_status.configure(text="Спряно", fg='#e74c3c')
    
    def circle_generator(self):
        colors = ['#f39c12', '#e67e22', '#f7dc6f', '#f8c471', '#fdeaa7']
        
        while self.circle_running:
            try:
                width, height = self.get_canvas_size()
                
                radius = random.randint(15, min(80, width//6, height//6))
                
                center_x = random.randint(radius, width - radius)
                center_y = random.randint(radius, height - radius)
                
                color = self.generate_random_color(colors)
                
                self.canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    fill=color, outline='#2c3e50', width=2
                )
                
                self.circle_count += 1
                self.circle_counter.configure(text=f"Брой: {self.circle_count}")
                
                time.sleep(4)
            except Exception as e:
                print(f"Грешка в circle_generator: {e}")
                break
    
    def stop_all(self):
        """Спира всички генератори"""
        self.rectangle_running = False
        self.triangle_running = False
        self.circle_running = False
        
        self.rect_btn.configure(text="🟦 Правоъгълник")
        self.tri_btn.configure(text="🔺 Триъгълник")
        self.circle_btn.configure(text="🔴 Кръг")
        
        self.rect_status.configure(text="Спряно", fg='#e74c3c')
        self.tri_status.configure(text="Спряно", fg='#e74c3c')
        self.circle_status.configure(text="Спряно", fg='#e74c3c')
        
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.rectangle_count = 0
        self.triangle_count = 0
        self.circle_count = 0
        
        self.rect_counter.configure(text="Брой: 0")
        self.tri_counter.configure(text="Брой: 0")
        self.circle_counter.configure(text="Брой: 0")
        

def main():
    root = tk.Tk()
    app = ShapeGeneratorApp(root)
    
    def on_closing():
        app.stop_all()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
