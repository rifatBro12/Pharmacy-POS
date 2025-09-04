base_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Pharmacy POS System</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: #0a192f;
            color: #e6f1ff;
            margin: 0;
            padding: 0;
        }
        header {
            background: linear-gradient(to right, #003087, #0052cc);
            color: white;
            padding: 1rem;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        nav a {
            margin: 0 15px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        nav a:hover {
            color: #80bfff;
        }
        .container {
            width: 85%;
            margin: 2rem auto;
            background: #172a45;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #334874;
            text-align: left;
        }
        th {
            background: #003087;
            color: white;
        }
        .btn {
            padding: 8px 16px;
            margin: 6px 0;
            background: #0052cc;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: #003087;
            transform: scale(1.05);
        }
        .btn-danger {
            background: #e63946;
        }
        .btn-danger:hover {
            background: #b32d39;
            transform: scale(1.05);
        }
        .success, .error {
            font-weight: bold;
            animation: fadeIn 0.5s ease-in-out;
        }
        .success { color: #00cc99; }
        .error { color: #ff4d4d; }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .med-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        .card {
            background: #1f4068;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        input, select {
            padding: 8px;
            margin: 6px 0;
            background: #2a4b7c;
            color: #e6f1ff;
            border: 1px solid #4d6d9a;
            border-radius: 6px;
        }
        @media (max-width: 768px) {
            .container {
                width: 95%;
            }
            nav a {
                display: block;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Pharmacy POS System</h1>
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('manage_inventory') }}">Inventory</a>
            <a href="{{ url_for('sell_medication') }}">Sell Medication</a>
            <a href="{{ url_for('view_sales') }}">Sales</a>
        </nav>
    </header>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

home_template = """
{% extends "base.html" %}
{% block content %}
    <h2>Welcome to the Pharmacy POS</h2>
    <p>Manage your pharmacy's inventory, sales, and prescriptions efficiently.</p>
    <h3>Dashboard</h3>
    <p>Number of Medications: {{ num_products }}</p>
    <p>Number of Sales: {{ total_sales }}</p>
    <p>Total Revenue: ${{ "%.2f"|format(total_revenue) }}</p>
    <p>Medications Expiring Soon (within 30 days): {{ expiring_soon }}</p>
    {% if labels %}
    <canvas id="myChart" width="600" height="300"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: {{ labels | tojson }},
            datasets: [{
                label: 'Revenue by Medication',
                data: {{ data | tojson }},
                backgroundColor: 'rgba(0, 82, 204, 0.4)',
                borderColor: 'rgba(0, 82, 204, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#4d6d9a' }
                },
                x: {
                    grid: { color: '#4d6d9a' }
                }
            },
            plugins: {
                legend: { labels: { color: '#e6f1ff' } }
            }
        }
    });
    </script>
    {% endif %}
{% endblock %}
"""

inventory_template = """
{% extends "base.html" %}
{% block content %}
    <h2>Medication Inventory</h2>
    <form method="post">
        <input type="text" name="name" placeholder="Medication Name" required>
        <input type="number" step="0.01" name="price" placeholder="Price" required>
        <input type="number" name="quantity" placeholder="Quantity" required>
        <input type="date" name="expiry" placeholder="Expiry Date (YYYY-MM-DD)" required>
        <label><input type="checkbox" name="prescription_required"> Prescription Required</label>
        <button class="btn" type="submit">Add Medication</button>
    </form>
    <br>
    <div class="med-grid">
        {% for name, data in inventory.items() %}
        <div class="card">
            <h3>{{ name }}</h3>
            <p>Price: ${{ "%.2f"|format(data.price) }}</p>
            <p>Quantity: {{ data.quantity }}</p>
            <p>Expiry: {{ data.expiry }}</p>
            <p>Prescription: {{ 'Required' if data.prescription_required else 'Not Required' }}</p>
            <form method="post">
                <input type="hidden" name="action" value="update">
                <input type="hidden" name="name" value="{{ name }}">
                <input type="number" step="0.01" name="price" value="{{ "%.2f"|format(data.price) }}" required>
                <input type="number" name="quantity" value="{{ data.quantity }}" required>
                <input type="date" name="expiry" value="{{ data.expiry }}" required>
                <button type="submit" class="btn">Update</button>
            </form>
            <form method="post">
                <input type="hidden" name="action" value="delete">
                <input type="hidden" name="name" value="{{ name }}">
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
        {% endfor %}
    </div>
    <br>
    <a class="btn" href="{{ url_for('export_inventory') }}">Export Inventory CSV</a>
{% endblock %}
"""

sell_template = """
{% extends "base.html" %}
{% block content %}
    <h2>Sell Medication</h2>
    <form method="post">
        <select name="name" required>
            {% for name in inventory.keys() %}
            <option value="{{ name }}">{{ name }}</option>
            {% endfor %}
        </select>
        <input type="number" name="quantity" min="1" value="1" required>
        <input type="text" name="prescription_id" placeholder="Prescription ID (if required)">
        <button class="btn" type="submit">Sell</button>
    </form>
    <p id="total">Total: $0.00</p>
    {% if message %}
        <p class="{{ 'success' if 'Sold' in message else 'error' }}">{{ message }}</p>
    {% endif %}
    <script>
    var inventory = {{ inventory | tojson }};
    function updateTotal() {
        var name = document.querySelector('select[name="name"]').value;
        var qty = parseInt(document.querySelector('input[name="quantity"]').value) || 1;
        var total = (inventory[name]?.price || 0) * qty;
        document.getElementById('total').innerHTML = 'Total: $' + total.toFixed(2);
    }
    document.querySelector('select[name="name"]').addEventListener('change', updateTotal);
    document.querySelector('input[name="quantity"]').addEventListener('input', updateTotal);
    updateTotal();
    </script>
{% endblock %}
"""

sales_template = """
{% extends "base.html" %}
{% block content %}
    <h2>Sales History</h2>
    <table>
        <tr><th>Medication</th><th>Quantity</th><th>Total</th><th>Prescription ID</th><th>Date</th></tr>
        {% for sale in sales %}
        <tr>
            <td>{{ sale[0] }}</td>
            <td>{{ sale[1] }}</td>
            <td>${{ "%.2f"|format(sale[2]) }}</td>
            <td>{{ sale[3] }}</td>
            <td>{{ sale[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    <p>Total Revenue: ${{ "%.2f"|format(total) }}</p>
    <br>
    <a class="btn" href="{{ url_for('export_sales') }}">Export Sales CSV</a>
{% endblock %}
"""