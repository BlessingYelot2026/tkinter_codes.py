import tkinter as tk

root = tk.Tk()
root.title("Temperature converter")
root.geometry("350x200")
label = tk.Label(root, text="Enter Temperature in celcius", font=("Arial", 12))
label.pack(pady=20)
celcius_entry=tk.Entry(
    root,
    font=("Arial",16)
)
celcius_entry.pack(pady=12)
result_label=tk.Label(root, text="Fahrenheit:",
                     font=("Arial",16),
                     fg="blue"
)
result_label.pack(pady=10)


def convert_temperature():
    celcius=float(celcius_entry.get())
    fahrenheit=celcius*9/5+32
    result_label.config(text=f"fahrenheit:{fahrenheit}")
    
tk.Button(
    root,
    text="Convert",
    font=("Arial", 11),
    command=convert_temperature
    ).pack(pady=10)    
    
root.mainloop()
