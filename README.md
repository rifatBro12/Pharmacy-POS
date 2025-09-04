# Pharmacy POS System

This is a Flask-based Point of Sale (POS) system designed for a medical pharmacy to manage medications, sales, and prescription tracking. It includes features like inventory management with expiration dates, prescription ID validation, and compliance with basic pharmacy regulations. The system features a modern, dark-themed UI optimized for pharmacy workflows.

## Features
- **Dashboard**: Displays medication count, total sales, revenue, and medications expiring soon (within 30 days), with a revenue chart using Chart.js.
- **Inventory Management**: Add, update, or delete medications with details like price, quantity, expiry date, and prescription requirements. Export inventory as CSV.
- **Sell Medication**: Record sales with quantity and optional prescription ID, with real-time total price calculation and stock updates.
- **Sales History**: View all sales with medication details, quantities, totals, prescription IDs, and timestamps. Export sales as CSV.
- **Pharmacy-Specific Features**: Tracks expiration dates, enforces prescription requirements, and generates unique prescription IDs.
- **Responsive Design**: Mobile-friendly with a sticky header, hover effects, and a pharmacy-themed color scheme.

## Project Structure
```
├── app.py          # Main Flask application with routes and logic
├── utils.py        # Helper functions for data handling and CSV operations
├── templates.py    # In-memory HTML templates for the application
├── inventory.csv   # Generated file for storing medication inventory
├── sales.csv       # Generated file for storing sales data
└── README.md       # This file
```

## Prerequisites
- **Python**: Version 3.6 or higher
- **Visual Studio Code**: For development and running the application
- **Flask**: Installed via pip
- **Internet Connection**: Required for loading Chart.js and Google Fonts (Roboto) from CDNs

## Setup Instructions
Follow these steps to run the application in Visual Studio Code:

1. **Create the Project Directory**:
   - Create a new directory for the project.
   - Save `app.py`, `utils.py`, and `templates.py` in this directory.

2. **Open in VS Code**:
   - Launch VS Code and open the project directory (`File > Open Folder`).

3. **Set Up a Virtual Environment**:
   - Open the terminal in VS Code (`Ctrl+~` or `View > Terminal`).
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - Windows:
       ```bash
       venv\Scripts\activate
       ```
     - macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies**:
   - Install Flask:
     ```bash
     pip install flask
     ```

5. **Run the Application**:
   - In the terminal, run:
     ```bash
     python app.py
     ```
   - The Flask development server will start at `http://127.0.0.1:5000`.

6. **Access the Application**:
   - Open a browser and navigate to `http://127.0.0.1:5000`.
   - Use the navigation bar to access Home, Inventory, Sell Medication, and Sales pages.

## Usage
- **Home**: View key metrics and a revenue chart by medication.
- **Inventory**: Add medications with price, quantity, expiry date, and prescription requirements. Update or delete medications and export the inventory as CSV.
- **Sell Medication**: Select a medication, specify quantity, and provide a prescription ID if required. The system checks stock and prescription requirements before processing sales.
- **Sales**: View all sales with details and export as CSV.

## Notes
- Templates are defined in-memory in `templates.py`, eliminating the need for separate HTML files.
- Data is stored in `inventory.csv` and `sales.csv`, created automatically when adding medications or recording sales.
- The application runs in debug mode (`debug=True`) for development. Disable this in production.
- Ensure an internet connection for Chart.js and Google Fonts to load.
- The system includes basic compliance features (e.g., prescription ID validation, expiry tracking) but does not fully implement HIPAA or other regulations, which would require additional security measures in a production environment.

## Troubleshooting
- **Flask Not Found**: Ensure Flask is installed (`pip install flask`).
- **Port Conflict**: If port 5000 is in use, change the port: `python app.py --port 5001`.
- **CSV Files Not Created**: Verify write permissions in the project directory.
- **Chart Not Displaying**: Check your internet connection for CDN access.
- **Date Format Issues**: Ensure expiry dates are entered in YYYY-MM-DD format.

## License
This project is for educational purposes and does not include a specific license. Use and modify as needed for learning or personal projects.
