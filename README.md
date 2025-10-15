Inventory Management & Billing System -- Python Console Application

Project Overview:
A comprehensive Python-based Inventory Management and Billing System that allows businesses to manage product inventory, process customer orders, generate bills, and track sales. The system uses CSV files for data persistence and provides a console-based interface.

Project Structure:
INVENTORY MANAGMENT/
│
├── inventory.csv
├── main.py
└── sales.csv

Features:
Product Management - Add, update, delete, search products
Billing System - Cart, discounts, checkout, receipts
Inventory Tracking - Real-time stock updates
Sales Reports - Daily sales and custom date ranges
Low Stock Alerts - Automatic restocking notifications
Data Export - CSV/TXT bills and reports

Product Search: Find products by ID or name

Data Storage:
inventory.csv - Product ID, Name, Price, Stock
sales.csv - DateTime, Total, Discount, Final Amount
Bill Files - bill_YYYYMMDD_HHMMSS.txt/csv receipts
Product data with pricing and inventory levels
Sales transactions with discount tracking
Individual customer receipts for each transaction

Billing System:
Cart Management - Add/remove items with quantity validation
Discount System - Percentage or fixed amount discounts
Checkout Process - Finalize sale and update inventory
Bill Generation - Create TXT/CSV receipts automatically
Payment Calculation - Subtotal, discount, final amount

Reports & Analytics:
Sales Reports - Custom date range reports
Daily Sales - Daily transaction summaries
Low Stock Alerts - Products needing restocking
Product Statistics - Inventory value and stock levels

Main Menu Options:
Product Management Menu
Adding a Product
Select option 1 from main menu

Choose "1. Add Product"

Enter:

Product ID: Unique identifier (e.g., "P001")

Name: Product name (e.g., "Laptop")

Price: Unit price (e.g., 999.99)

Stock Quantity: Initial stock (e.g., 50)

Updating a Product
Use "2. Update Product" to modify existing products

Leave fields blank to keep current values

Searching Products
Search by product ID or name (partial matches supported)

2. Billing Process
Adding Items to Cart
Select "2. Billing" from main menu

Choose "1. Add to Cart"

Enter Product ID and quantity

System validates stock availability

Applying Discounts
Percentage Discount: Enter percentage (e.g., 10 for 10% off)

Fixed Discount: Enter amount (e.g., 50 for $50 off)

Checkout
Review cart with "3. View Cart"

Apply discounts if needed

Select "5. Checkout" to complete sale

Choose to save bill in TXT or CSV format

3. Reports
Daily Sales Report
View sales for any specific date

Shows transaction count and total revenue

Defaults to current date if no date specified

Low Stock Report
Identifies products below threshold (default: 5 units)

Customizable threshold value
