
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt  # Step 1

# Function to connect to MySQL database
# Function to connect to MySQL database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sujaldhamne",
            database="inventory"
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {err}")
        return None, None

# Function to create the inventory table if it doesn't exist
def create_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL
            )
        """)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating table: {err}")

# Function to insert item into the inventory
def add_item(name, quantity, cursor, conn):
    try:
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s)", (name, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Item added to inventory")
    except mysql.connector.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error adding item: {err}")

# Function to display inventory
def display_inventory(cursor):
    try:
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error displaying inventory: {err}")
        return []

# Function to update item quantity
def update_item(name, new_quantity, cursor, conn):
    try:
        cursor.execute("UPDATE inventory SET quantity = %s WHERE name = %s", (new_quantity, name))
        conn.commit()
        messagebox.showinfo("Success", "Item quantity updated")
    except mysql.connector.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating item quantity: {err}")

# Function to delete item from inventory
def delete_item(name, cursor, conn):
    try:
        cursor.execute("SELECT * FROM inventory WHERE name = %s", (name,))
        item = cursor.fetchone()  # Fetch one row
        if item:
            cursor.execute("DELETE FROM inventory WHERE name = %s", (name,))
            conn.commit()
            messagebox.showinfo("Success", "Item deleted from inventory")
        else:
            messagebox.showwarning("Warning", f"Item '{name}' is not in the inventory")
    except mysql.connector.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error deleting item: {err}")


# Tkinter GUI
def main():
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("500x300")
    root.config(bg="#f0f0f0")

    # Connect to database
    conn, cursor = connect_to_db()
    if conn and cursor:
        create_table(cursor)

        # Add item to inventory
        def add_item_to_inventory():
            name = name_entry.get()
            quantity = quantity_entry.get()
            if name and quantity:
                add_item(name, quantity, cursor, conn)
            else:
                messagebox.showwarning("Warning", "Please enter both name and quantity")

        # Display inventory
        # Function to display inventory with sorting option and search feature for product name
        def display_inventory_gui():
            def sort_by_mixed_case_name():
                inventory_data.sort(key=lambda x: x[1].lower())
                update_display()

            def search_items():
                search_name = search_name_entry.get().strip().lower()
                search_results = []
                for item in inventory_data:
                    item_name = item[1].lower()
                    if search_name in item_name:
                        search_results.append(item)
                update_display(search_results)

            def update_display(data=None):
                display_inventory_tree.delete(*display_inventory_tree.get_children())
                data = data if data else inventory_data
                for row in data:
                    display_inventory_tree.insert("", "end", values=row)

            inventory_data = display_inventory(cursor)
            if inventory_data:
                display_window = tk.Toplevel(root)
                display_window.title("Inventory")
                display_window.geometry("600x300")
                display_window.configure(bg="#f0f0f0")

                tree_frame = tk.Frame(display_window, bg="#f0f0f0")
                tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                display_inventory_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Quantity"), show="headings",
                                                      style="Custom.Treeview")
                display_inventory_tree.heading("ID", text="ID")
                display_inventory_tree.heading("Name", text="Name", command=sort_by_mixed_case_name)
                display_inventory_tree.heading("Quantity", text="Quantity")

                for row in inventory_data:
                    display_inventory_tree.insert("", "end", values=row)

                display_inventory_tree.pack(fill=tk.BOTH, expand=True)

                sort_label = tk.Label(display_window, text="Sort by:", font=("Arial", 10), bg="#f0f0f0")
                sort_label.pack(pady=(10, 5))

                sort_button = tk.Button(display_window, text="Product Name",
                                        command=sort_by_mixed_case_name, font=("Arial", 10), bg="#4CAF50", fg="white")
                sort_button.pack(pady=5)

                search_frame = tk.Frame(display_window, bg="#f0f0f0")
                search_frame.pack(pady=(10, 5))

                search_name_label = tk.Label(search_frame, text="Search Product Name:", font=("Arial", 10),
                                             bg="#f0f0f0")
                search_name_label.grid(row=0, column=0, padx=(0, 5))

                search_name_entry = tk.Entry(search_frame, font=("Arial", 10))
                search_name_entry.grid(row=0, column=1, padx=(0, 5))

                search_button = tk.Button(search_frame, text="Search", command=search_items, font=("Arial", 10),
                                          bg="#008CBA", fg="white")
                search_button.grid(row=0, column=2, padx=(0, 5))

                clear_button = tk.Button(search_frame, text="Clear", command=update_display, font=("Arial", 10),
                                         bg="#FF6347", fg="white")
                clear_button.grid(row=0, column=3)

                # Button to display pie chart
                pie_chart_button = tk.Button(display_window, text="Display Pie Chart", command=display_pie_chart,
                                              font=("Arial", 10),bg="#4CAF50", fg="white")
                pie_chart_button.pack(pady=5)

            else:
                messagebox.showinfo("Inventory", "Inventory is empty")

        # Function to update item quantity
        def update_quantity():
            def update():
                name = name_var.get()
                new_quantity = new_quantity_entry.get()
                if name and new_quantity:
                    update_item(name, new_quantity, cursor, conn)
                    update_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please enter both name and new quantity")

            update_window = tk.Toplevel(root)
            update_window.title("Update Quantity")
            update_window.geometry("300x150")
            update_window.configure(bg="#f0f0f0")

            label_font = ("Arial", 12)

            update_label = tk.Label(update_window, text="Enter Product Name:", font=label_font, bg="#f0f0f0")
            update_label.grid(row=0, column=0, padx=10, pady=5)

            name_var = tk.StringVar()
            name_entry = tk.Entry(update_window, textvariable=name_var, font=label_font)
            name_entry.grid(row=0, column=1, padx=10, pady=5)

            new_quantity_label = tk.Label(update_window, text="New Quantity:", font=label_font, bg="#f0f0f0")
            new_quantity_label.grid(row=1, column=0, padx=10, pady=5)

            new_quantity_entry = tk.Entry(update_window, font=label_font)
            new_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

            update_button = tk.Button(update_window, text="Update", command=update, font=label_font, bg="#4CAF50", fg="white")
            update_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Function to delete item
        def delete_product():
            def delete():
                name = name_var.get()
                if name:
                    delete_item(name, cursor, conn)
                    delete_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please enter product name")

            delete_window = tk.Toplevel(root)
            delete_window.title("Delete Product")
            delete_window.geometry("300x100")
            delete_window.configure(bg="#f0f0f0")

            label_font = ("Arial", 12)

            delete_label = tk.Label(delete_window, text="Enter Product Name:", font=label_font, bg="#f0f0f0")
            delete_label.grid(row=0, column=0, padx=10, pady=5)

            name_var = tk.StringVar()
            name_entry = tk.Entry(delete_window, textvariable=name_var, font=label_font)
            name_entry.grid(row=0, column=1, padx=10, pady=5)

            delete_button = tk.Button(delete_window, text="Delete", command=delete, font=label_font, bg="#FF6347", fg="white")
            delete_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Function to display pie chart
        def display_pie_chart():
            inventory_data = display_inventory(cursor)
            if inventory_data:
                names = [row[1] for row in inventory_data]
                quantities = [row[2] for row in inventory_data]

                plt.figure(figsize=(6, 6))
                plt.pie(quantities, labels=names, autopct='%1.1f%%', startangle=140)
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.title('Inventory Distribution')

                plt.show()
            else:
                messagebox.showinfo("Inventory", "Inventory is empty")

        label_font = ("Arial", 12)
        entry_font = ("Arial", 10)

        name_label = tk.Label(root, text="Item Name:", font=label_font, bg="#f0f0f0")
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(root, font=entry_font)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        quantity_label = tk.Label(root, text="Quantity:", font=label_font, bg="#f0f0f0")
        quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        quantity_entry = tk.Entry(root, font=entry_font)
        quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        add_button = tk.Button(root, text="Add Item", command=add_item_to_inventory, font=label_font, bg="#4CAF50", fg="white")
        add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        display_button = tk.Button(root, text="Display Inventory", command=display_inventory_gui, font=label_font, bg="#008CBA", fg="white")
        display_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        action_frame = tk.Frame(root, bg="#f0f0f0")
        action_frame.grid(row=4, column=0, columnspan=2, pady=10)

        update_button = tk.Button(action_frame, text="Update Quantity", command=update_quantity, font=label_font, bg="#FFD700", fg="black")
        update_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(action_frame, text="Delete Product", command=delete_product, font=label_font, bg="#FF6347", fg="white")
        delete_button.grid(row=0, column=1, padx=5)

        root.mainloop()
        cursor.close()
        conn.close()
    else:
        root.destroy()

if __name__ == "__main__":
    main()
