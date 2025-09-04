from flask import Flask, render_template, request, send_file
from jinja2 import DictLoader
from utils import load_inventory, load_sales, save_inventory, save_sales, generate_prescription_id, inventory, sales
from templates import base_template, home_template, inventory_template, sell_template, sales_template
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Register in-memory templates
app.jinja_loader = DictLoader({
    "base.html": base_template,
    "home.html": home_template,
    "inventory.html": inventory_template,
    "sell.html": sell_template,
    "sales.html": sales_template,
})

# Routes
@app.route("/")
def home():
    sales_summary = defaultdict(float)
    for s in sales:
        sales_summary[s[0]] += s[2]
    labels = list(sales_summary.keys())
    data = list(sales_summary.values())
    num_products = len(inventory)
    total_sales = len(sales)
    total_revenue = sum(data)
    expiring_soon = sum(1 for item in inventory.values() if item['expiry'] and (datetime.strptime(item['expiry'], '%Y-%m-%d') - datetime.now()).days <= 30)
    return render_template("home.html", num_products=num_products, total_sales=total_sales, total_revenue=total_revenue, expiring_soon=expiring_soon, labels=labels, data=data)

@app.route("/inventory", methods=["GET", "POST"])
def manage_inventory():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "delete":
            name = request.form["name"]
            if name in inventory:
                del inventory[name]
                save_inventory()
        elif action == "update":
            name = request.form["name"]
            new_price = float(request.form["price"])
            new_quantity = int(request.form["quantity"])
            new_expiry = request.form["expiry"]
            if name in inventory:
                inventory[name].update({"price": new_price, "quantity": new_quantity, "expiry": new_expiry})
                save_inventory()
        else:
            name = request.form["name"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
            expiry = request.form["expiry"]
            prescription_required = request.form.get("prescription_required") == "on"
            inventory[name] = {"price": price, "quantity": quantity, "expiry": expiry, "prescription_required": prescription_required}
            save_inventory()
    return render_template("inventory.html", inventory=inventory)

@app.route("/sell", methods=["GET", "POST"])
def sell_medication():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        qty = int(request.form["quantity"])
        prescription_id = request.form.get("prescription_id", "")
        if name in inventory:
            if inventory[name]["quantity"] >= qty:
                if inventory[name]["prescription_required"] and not prescription_id:
                    message = f"Error: {name} requires a prescription ID."
                else:
                    total = inventory[name]["price"] * qty
                    prescription_id = prescription_id or generate_prescription_id()
                    sales.append([name, qty, total, prescription_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    inventory[name]["quantity"] -= qty
                    save_sales()
                    save_inventory()
                    message = f"Sold {qty} x {name} for ${total:.2f}. Prescription ID: {prescription_id}"
            else:
                message = f"Error: Insufficient stock for {name}. Available: {inventory[name]['quantity']}"
    return render_template("sell.html", inventory=inventory, message=message)

@app.route("/sales")
def view_sales():
    total = sum(s[2] for s in sales)
    return render_template("sales.html", sales=sales, total=total)

@app.route("/export/inventory")
def export_inventory():
    return send_file("inventory.csv", as_attachment=True)

@app.route("/export/sales")
def export_sales():
    return send_file("sales.csv", as_attachment=True)

# Startup
if __name__ == "__main__":
    load_inventory()
    load_sales()
    app.run(debug=True)