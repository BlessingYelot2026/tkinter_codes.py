import tkinter as tk
from tkinter import ttk
import csv
import os
import math
from datetime import datetime
# Name of the CSV file
CSV_FILE = "inventory_purchases.csv"
# Column headings for the CSV file
HEADERS = [
    "Date and Time",
    "Product Name",
    "Quantity",
    "Unit Price (NGN)",
    "Total Cost (NGN)"
]
# 1. Create the CSV file if it does not exist
def create_csv_file():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
# 2. Clear the input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_name.focus_set()
    status_label.config(
        text="Fields cleared. Saved records are safe.",
        fg="blue"
    )
# 3. Display saved records in the table
def refresh_records():
    # Remove old rows from the table
    for row in records_table.get_children():
        records_table.delete(row)
    total_spent = 0.0
    record_count = 0
    try:
        create_csv_file()
        with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for record in reader:
                date_time = record.get("Date and Time", "")
                name = record.get("Product Name", "")
                quantity = record.get("Quantity", "")
                unit_price = float(
                    record.get("Unit Price (NGN)", "0") or 0
                )
                total_cost = float(
                    record.get("Total Cost (NGN)", "0") or 0
                )
                # Add this record to the table
                records_table.insert(
                    "",
                    tk.END,
                    values=(
                        date_time,
                        name,
                        quantity,
                        f"{unit_price:,.2f}",
                        f"{total_cost:,.2f}"
                    )
                )
                # Add the cost to the total expenditure
                total_spent += total_cost
                record_count += 1
        total_label.config(
            text=f"Total recorded purchases: ₦{total_spent:,.2f} "
                 f"| Records: {record_count}"
        )
        status_label.config(
            text=f"Loaded {record_count} purchase record(s).",
            fg="blue"
        )
    except (OSError, ValueError, csv.Error) as error:
        status_label.config(
            text=f"Could not load records: {error}",
            fg="red"
        )
# 4. Validate and save a new purchase
def save_purchase():
    # Get the information entered by the user
    name = entry_name.get().strip()
    quantity_text = entry_quantity.get().strip()
    price_text = entry_price.get().strip().replace(",", "")
    # Check the product name
    if not name:
        status_label.config(
            text="Please enter a product name.",
            fg="red"
        )
        return
    # Convert quantity into an integer
    try:
        quantity = int(quantity_text)
    except ValueError:
        status_label.config(
            text="Quantity must be a whole number, such as 2 or 10.",
            fg="red"
        )
        return
    if quantity <= 0:
        status_label.config(
            text="Quantity must be greater than zero.",
            fg="red"
        )
        return
    # Convert price into a number
    try:
        unit_price = float(price_text)
    except ValueError:
        status_label.config(
            text="Enter a valid price, such as 2500 or 2500.50.",
            fg="red"
        )
        return
    if not math.isfinite(unit_price) or unit_price < 0:
        status_label.config(
            text="Price must be a valid, non-negative number.",
            fg="red"
        )
        return
    # Calculate the total purchase cost
    total_cost = quantity * unit_price
    # Put the purchase information into a dictionary
    record = {
        "Date and Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "Product Name": name,
        "Quantity": quantity,
        "Unit Price (NGN)": f"{unit_price:.2f}",
        "Total Cost (NGN)": f"{total_cost:.2f}"
    }
    # Save the record in the CSV file
    try:
        create_csv_file()
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writerow(record)
        # Update the table
        refresh_records()
        # Clear the input boxes
        entry_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_name.focus_set()
        # Show a success message inside the window
        status_label.config(
            text=f"Saved {name}: {quantity} unit(s), "
                 f"total ₦{total_cost:,.2f}.",
            fg="green"
        )
    except (OSError, csv.Error) as error:
        status_label.config(
            text=f"Could not save purchase: {error}",
            fg="red"
        )
# 5. Create the main window
root = tk.Tk()
root.title("Beginner Inventory - Goods Purchased")
root.geometry("900x600")
root.minsize(760, 500)
# Application title
title_label = tk.Label(
    root,
    text="Mini Inventory - Goods Purchased",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=12)
# 6. Create the input form
form_frame = tk.LabelFrame(
    root,
    text="Enter a new purchase",
    padx=10,
    pady=10
)
form_frame.pack(fill="x", padx=12, pady=5)
# Product name
tk.Label(form_frame, text="Product name:").grid(
    row=0, column=0, sticky="w", padx=5, pady=6
)
entry_name = tk.Entry(form_frame, width=25)
entry_name.grid(
    row=0, column=1, sticky="ew", padx=5, pady=6
)
# Quantity
tk.Label(form_frame, text="Quantity bought:").grid(
    row=0, column=2, sticky="w", padx=5, pady=6
)
entry_quantity = tk.Entry(form_frame, width=15)
entry_quantity.grid(
    row=0, column=3, sticky="ew", padx=5, pady=6
)
# Unit price
tk.Label(form_frame, text="Unit price (NGN):").grid(
    row=1, column=0, sticky="w", padx=5, pady=6
)
entry_price = tk.Entry(form_frame, width=25)
entry_price.grid(
    row=1, column=1, sticky="ew", padx=5, pady=6
)
# Allow input columns to expand
form_frame.columnconfigure(1, weight=1)
form_frame.columnconfigure(3, weight=1)
# 7. Create the buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=12, pady=8)
tk.Button(
    button_frame,
    text="Save Purchase",
    command=save_purchase,
    bg="#2E8B57",
    fg="white",
    padx=10,
    pady=5
).pack(side="left", padx=4)
tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    padx=10,
    pady=5
).pack(side="left", padx=4)
tk.Button(
    button_frame,
    text="Refresh Records",
    command=refresh_records,
    padx=10,
    pady=5
).pack(side="left", padx=4)
# 8. Create the records table
table_frame = tk.LabelFrame(
    root,
    text="Saved purchase records",
    padx=6,
    pady=6
)
table_frame.pack(
    fill="both", expand=True, padx=12, pady=5
)
columns = (
    "date",
    "product",
    "quantity",
    "unit_price",
    "total"
)
records_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)
# Table headings
records_table.heading("date", text="Date and Time")
records_table.heading("product", text="Product Name")
records_table.heading("quantity", text="Quantity")
records_table.heading("unit_price", text="Unit Price (₦)")
records_table.heading("total", text="Total Cost (₦)")
# Table column sizes and alignment
records_table.column("date", width=145, anchor="w")
records_table.column("product", width=200, anchor="w")
records_table.column("quantity", width=80, anchor="center")
records_table.column("unit_price", width=130, anchor="e")
records_table.column("total", width=130, anchor="e")
# Scrollbar
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=records_table.yview
)
records_table.configure(
    yscrollcommand=scrollbar.set
)
records_table.pack(
    side="left", fill="both", expand=True
)
scrollbar.pack(side="right", fill="y")
# 9. Display total expenditure
total_label = tk.Label(
    root,
    text="Total recorded purchases: ₦0.00",
    font=("Arial", 10, "bold")
)
total_label.pack(anchor="e", padx=14, pady=4)
# 10. Display status and error messages
status_label = tk.Label(
    root,
    text="Ready. Enter a purchase to begin.",
    fg="blue",
    wraplength=850
)
status_label.pack(fill="x", padx=12, pady=8)
# Create the CSV file and display any existing records
create_csv_file()
refresh_records()
# Keep the window running
root.mainloop()
   