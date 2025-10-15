## Inventory Management & Billing System -- Python Console Application

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
1. Inventory Management

View, add, update, delete, and search products

Manage product details, prices, and stock quantities

2. Billing & Sales

Cart management with add/remove items

Apply discounts and complete checkout

Generate printable receipts

3. Reports & Analytics

Daily sales reports with revenue tracking

Low stock alerts for inventory management

4. Exit

Close application
