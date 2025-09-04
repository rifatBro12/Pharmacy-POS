import csv
import random
import string
import os
from datetime import datetime

inventory_file = "inventory.csv"
sales_file = "sales.csv"

inventory = {}
sales = []

def load_inventory():
    global inventory
    if os.path.exists(inventory_file):
        with open(inventory_file, mode="r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    inventory[row[0]] = {
                        "price": float(row[1]),
                        "quantity": int(row[2]),
                        "expiry": row[3],
                        "prescription_required": row[4] == "True"
                    }

def load_sales():
    global sales
    sales = []
    if os.path.exists(sales_file):
        with open(sales_file, mode="r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    sales.append([row[0], int(row[1]), float(row[2]), row[3], row[4]])

def save_inventory():
    with open(inventory_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        for name, data in inventory.items():
            writer.writerow([name, data["price"], data["quantity"], data["expiry"], data["prescription_required"]])

def save_sales():
    with open(sales_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        for sale in sales:
            writer.writerow(sale)

def generate_prescription_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))