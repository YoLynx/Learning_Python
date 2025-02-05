import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt


class System:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")

        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()
        self.bill_no = tk.StringVar(value=str(datetime.now().strftime("%Y%m%d%H%M%S")))
        self.payment_mode = tk.StringVar(value="UPI")  # Default payment mode will be UPI.

        self.items = {
            "Burger": 100,
            "Pizza": 200,
            "Pasta": 150,
            "Sandwich": 80,
            "Salad": 90,
            "Fries": 50,
            "Noodles": 140,
            "Ice Cream": 70,
            "Coffee": 60,
            "Tea": 40,
            "Soda": 30,
            "Milkshake": 120,
        }

        self.orders = {}
        self.gst_percentage = 18

        self.db_file = "restaurant.db"  # SQLite database file.
        self.create_gui()
        self.init_db()

    def create_gui(self):
        # Here we take the customer details.
        details_frame = tk.LabelFrame(self.root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)

        name_label = tk.Label(details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        contact_label = tk.Label(details_frame, text="Contact:")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact)
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        bill_label = tk.Label(details_frame, text="Bill No:")
        bill_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        bill_entry = tk.Entry(details_frame, textvariable=self.bill_no, state="readonly")
        bill_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        date_label = tk.Label(details_frame, text="Date & Time:")
        date_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_value = tk.Label(details_frame, text=current_time)
        date_value.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Here we have Menu section.
        menu_frame = tk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity")
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        row = 1
        for item, price in self.items.items():
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantity_entry = tk.Entry(menu_frame, width=5)
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            self.orders[item] = {"quantity": quantity_entry}
            row += 1

        # Section for Buttons.
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup, bg="lightgreen")
        print_bill_button.pack(side="left", padx=5)

        past_record_button = tk.Button(buttons_frame, text="View Analysis", command=self.view_past_records, bg="lightblue")
        past_record_button.pack(side="left", padx=5)

        reset_order_button = tk.Button(buttons_frame, text="Reset Order", command=self.clear_selection, bg="lightcoral")
        reset_order_button.pack(side="left", padx=5)

        # Payment mode.
        payment_frame = tk.LabelFrame(self.root, text="Payment Mode")
        payment_frame.pack(fill="x", padx=10, pady=10)

        for mode in ["UPI", "Cash", "Card"]:
            radio_button = tk.Radiobutton(payment_frame, text=mode, value=mode, variable=self.payment_mode)
            radio_button.pack(side="left", padx=5)

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                customer_name TEXT,
                customer_contact TEXT,
                item_name TEXT,
                quantity INTEGER,
                total_price REAL
            )
        """)
        conn.commit()
        conn.close()

    def show_bill_popup(self):
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Please enter customer name.")
            return

        selected_items, total_price = self.get_selected_items_and_total_price()

        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item.")
            return

        gst_amount = (total_price * self.gst_percentage) / 100
        grand_total = total_price + gst_amount

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n"
        bill += f"Bill No: {self.bill_no.get()}\n"
        bill += f"Payment Mode: {self.payment_mode.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(grand_total)}"

        self.log_bill(selected_items, grand_total)
        messagebox.showinfo("Bill", bill)

    def log_bill(self, selected_items, grand_total):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for item, quantity in selected_items:
            cursor.execute("""
                INSERT INTO orders (date, customer_name, customer_contact, item_name, quantity, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (datetime.now().strftime("%Y-%m-%d"), self.customer_name.get(), self.customer_contact.get(),
                  item, quantity, grand_total))
        conn.commit()
        conn.close()

    def view_past_records(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, SUM(quantity) FROM orders GROUP BY item_name")
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showwarning("No Records", "No past records found.")
                return

            items = [row[0] for row in data]
            quantities = [row[1] for row in data]

            plt.bar(items, quantities, color="lightpink")
            plt.xlabel("Items")
            plt.ylabel("Quantity Sold")
            plt.title("Sales Analysis")
            plt.show()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_selection(self):
        for item, info in self.orders.items():
            info["quantity"].delete(0, tk.END)

    def get_selected_items_and_total_price(self):
        selected_items = []
        total_price = 0
        for item, info in self.orders.items():
            quantity = info["quantity"].get().strip()
            if quantity.isdigit() and int(quantity) > 0:
                quantity = int(quantity)
                selected_items.append((item, quantity))
                total_price += self.items[item] * quantity
        return selected_items, total_price

    @staticmethod
    def convert_to_inr(amount):
        return f"₹{amount:.2f}"


if __name__ == "__main__":
    root = tk.Tk()
    app = System(root)
    root.mainloop()

