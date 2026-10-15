import tkinter as tk
root=tk.Tk()
root.title('MY PERSONAL CARD')
root.geometry('400x300')
Name_label = tk.Label(
    root,
    text="Name:Blessing",
    font=("Arial", 16),
    fg="pink",         
    bg="white"   
)
Name_label.pack(pady=10)     

Age_label=tk.Label(
            root,
            text="Age:30",
            font=("Arial",17),
            fg="blue",
            bg="grey"
)
Age_label.pack(pady=10)

City_label=tk.Label(
            root,
            text="City: Ibadan",
            font=("Arial",16),
            fg="grey",
            bg="blue"
)
City_label.pack(pady=10)

My_self_label=tk.Label(
                root,
                text="I am an aspiring data analyst",
                font=("Arial",16),
                fg="green",
                bg="white"
)
My_self_label.pack(pady=10)

root.mainloop()