import os
import csv
from datetime import datetime, date, timedelta

class Product:
    def __init__(self, product_id, name, price, stock_quantity):  # Fixed: double underscores
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock_quantity': self.stock_quantity
        }

class OrderItem:
    def __init__(self, product, quantity):  # Fixed: double underscores
        self.product = product
        self.quantity = quantity
        self.total = product.price * quantity

class Sale:
    def __init__(self, items, total_amount, sale_datetime, discount=0):  # Fixed: double underscores
        self.items = items
        self.total_amount = total_amount
        self.datetime = sale_datetime
        self.discount = discount
        self.final_amount = total_amount - discount

class InventoryManager:
    def __init__(self, data_file='inventory.csv'):  # Fixed: double underscores
        self.data_file = data_file
        self.products = self.load_data()
    
    def load_data(self):
        products = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            product = Product(
                                row['product_id'],
                                row['name'],
                                float(row['price']),
                                int(row['stock_quantity'])
                            )
                            products[product.product_id] = product
                        except (ValueError, KeyError):
                            continue
            except Exception:
                pass
        return products
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['product_id', 'name', 'price', 'stock_quantity']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for product in self.products.values():
                    writer.writerow(product.to_dict())
            return True
        except Exception:
            return False
    
    def add_product(self, product_id, name, price, stock_quantity):
        if product_id in self.products:
            print("Product ID already exists!")
            return False
        
        if price <= 0:
            print("Price must be greater than zero!")
            return False
        
        if stock_quantity < 0:
            print("Stock quantity cannot be negative!")
            return False
        
        self.products[product_id] = Product(product_id, name, price, stock_quantity)
        if self.save_data():
            print("Product added successfully!")
            return True
        return False
    
    def update_product(self, product_id, name=None, price=None, stock_quantity=None):
        if product_id not in self.products:
            print("Product not found!")
            return False
        
        product = self.products[product_id]
        if name is not None:
            product.name = name
        if price is not None:
            if price <= 0:
                print("Price must be greater than zero!")
                return False
            product.price = price
        if stock_quantity is not None:
            if stock_quantity < 0:
                print("Stock quantity cannot be negative!")
                return False
            product.stock_quantity = stock_quantity
        
        if self.save_data():
            print("Product updated successfully!")
            return True
        return False
    
    def delete_product(self, product_id):
        if product_id not in self.products:
            print("Product not found!")
            return False
        
        del self.products[product_id]
        if self.save_data():
            print("Product deleted successfully!")
            return True
        return False
    
    def search_product(self, keyword):
        results = []
        for product in self.products.values():
            if (keyword.lower() in product.name.lower() or 
                keyword.lower() == product.product_id.lower()):
                results.append(product)
        return results
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def view_all_products(self):
        if not self.products:
            print("No products available!")
            return
        
        print("\n" + "="*60)
        print("ALL PRODUCTS")
        print("="*60)
        print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
        print("-"*60)
        for product in self.products.values():
            print(f"{product.product_id:<10} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10}")
        print("="*60)

class BillingSystem:
    def __init__(self, inventory_manager, sales_file='sales.csv'):  # Fixed: double underscores
        self.inventory_manager = inventory_manager
        self.sales_file = sales_file
        self.cart = []
        self.sales = self.load_sales()
    
    def load_sales(self):
        sales = []
        if os.path.exists(self.sales_file):
            try:
                with open(self.sales_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            total_amount = float(row['total_amount'])
                            discount = float(row.get('discount', 0))
                            sale_datetime = datetime.fromisoformat(row['datetime'])
                            sale = Sale([], total_amount, sale_datetime, discount)
                            sales.append(sale)
                        except (ValueError, KeyError):
                            continue
            except Exception:
                pass
        return sales
    
    def save_sales(self):
        try:
            with open(self.sales_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['datetime', 'total_amount', 'discount', 'final_amount']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for sale in self.sales:
                    writer.writerow({
                        'datetime': sale.datetime.isoformat(),
                        'total_amount': sale.total_amount,
                        'discount': sale.discount,
                        'final_amount': sale.final_amount
                    })
            return True
        except Exception:
            return False
    
    def add_to_cart(self, product_id, quantity):
        product = self.inventory_manager.get_product(product_id)
        if not product:
            print("Product not found!")
            return False
        
        if quantity <= 0:
            print("Quantity must be greater than zero!")
            return False
        
        if product.stock_quantity < quantity:
            print(f"Insufficient stock! Only {product.stock_quantity} available.")
            return False
        
        for item in self.cart:
            if item.product.product_id == product_id:
                item.quantity += quantity
                item.total = item.product.price * item.quantity
                print("Item quantity updated in cart!")
                return True
        
        self.cart.append(OrderItem(product, quantity))
        print("Item added to cart!")
        return True
    
    def remove_from_cart(self, product_id, quantity=None):
        for i, item in enumerate(self.cart):
            if item.product.product_id == product_id:
                if quantity is None or quantity >= item.quantity:
                    self.cart.pop(i)
                    print("Item removed from cart!")
                else:
                    item.quantity -= quantity
                    item.total = item.product.price * item.quantity
                    print("Item quantity updated in cart!")
                return True
        print("Item not found in cart!")
        return False
    
    def view_cart(self):
        if not self.cart:
            print("Cart is empty!")
            return
        
        print("\n" + "="*60)
        print("SHOPPING CART")
        print("="*60)
        total = 0
        for i, item in enumerate(self.cart, 1):
            print(f"{i}. {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}")
            total += item.total
        
        print("-"*60)
        print(f"Total: ${total:.2f}")
        print("="*60)
    
    def apply_discount(self, discount_type, value):
        if not self.cart:
            print("Cart is empty!")
            return 0
        
        total = sum(item.total for item in self.cart)
        
        if discount_type == "percentage":
            if value < 0 or value > 100:
                print("Discount percentage must be between 0 and 100!")
                return 0
            discount = total * (value / 100)
        elif discount_type == "fixed":
            if value < 0 or value > total:
                print(f"Fixed discount must be between 0 and {total}!")
                return 0
            discount = value
        else:
            print("Invalid discount type! Use 'percentage' or 'fixed'.")
            return 0
        
        print(f"Discount applied: ${discount:.2f}")
        return discount
    
    def checkout(self, discount=0):
        if not self.cart:
            print("Cart is empty!")
            return None
        
        total = sum(item.total for item in self.cart)
        
        if discount < 0 or discount > total:
            print("Invalid discount amount!")
            return None
        
        # Update inventory and create sale
        for item in self.cart:
            product = self.inventory_manager.get_product(item.product.product_id)
            if product.stock_quantity < item.quantity:
                print(f"Error: Insufficient stock for {product.name}. Only {product.stock_quantity} available.")
                return None
        
        sale = Sale(self.cart.copy(), total, datetime.now(), discount)
        self.sales.append(sale)
        self.save_sales()
        
        # Update inventory after successful sale
        for item in self.cart:
            product = self.inventory_manager.get_product(item.product.product_id)
            product.stock_quantity -= item.quantity
        self.inventory_manager.save_data()
        
        self.cart.clear()
        
        print("Checkout completed successfully!")
        return sale
    
    def generate_bill(self, sale, file_format='txt'):
        if file_format not in ['txt', 'csv']:
            print("Invalid file format! Choose 'txt' or 'csv'.")
            return False
        
        filename = f"bill_{sale.datetime.strftime('%Y%m%d_%H%M%S')}.{file_format}"
        
        try:
            if file_format == 'txt':
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("="*50 + "\n")
                    file.write("BILL\n")
                    file.write("="*50 + "\n")
                    file.write(f"Date: {sale.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write("-"*50 + "\n")
                    file.write("Items:\n")
                    for item in sale.items:
                        file.write(f"  {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}\n")
                    file.write("-"*50 + "\n")
                    file.write(f"Subtotal: ${sale.total_amount:.2f}\n")
                    if sale.discount > 0:
                        file.write(f"Discount: -${sale.discount:.2f}\n")
                    file.write(f"Total: ${sale.final_amount:.2f}\n")
                    file.write("="*50 + "\n")
            else:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['BILL'])
                    writer.writerow(['Date', sale.datetime.strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    writer.writerow(['Product', 'Quantity', 'Unit Price', 'Total'])
                    for item in sale.items:
                        writer.writerow([item.product.name, item.quantity, f"${item.product.price:.2f}", f"${item.total:.2f}"])
                    writer.writerow([])
                    writer.writerow(['Subtotal', '', '', f"${sale.total_amount:.2f}"])
                    if sale.discount > 0:
                        writer.writerow(['Discount', '', '', f"-${sale.discount:.2f}"])
                    writer.writerow(['Total', '', '', f"${sale.final_amount:.2f}"])
            
            print(f"Bill saved as {filename}")
            return True
        except Exception as e:
            print(f"Error generating bill: {e}")
            return False
    
    def get_daily_sales(self, target_date=None):
        if target_date is None:
            target_date = datetime.now().date()
        
        daily_sales = []
        for sale in self.sales:
            if sale.datetime.date() == target_date:
                daily_sales.append(sale)
        
        return daily_sales
    
    def get_low_stock_products(self, threshold=5):
        low_stock = []
        for product in self.inventory_manager.products.values():
            if product.stock_quantity <= threshold:
                low_stock.append(product)
        return low_stock

def main():
    inventory_manager = InventoryManager()
    billing_system = BillingSystem(inventory_manager)
    
    while True:
        print("\n" + "="*60)
        print("INVENTORY MANAGEMENT & BILLING SYSTEM")
        print("="*60)
        print("1. Product Management")
        print("2. Billing")
        print("3. Reports")
        print("4. Exit")
        print("="*60)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            product_management_menu(inventory_manager)
        elif choice == '2':
            billing_menu(billing_system)
        elif choice == '3':
            reports_menu(billing_system, inventory_manager)
        elif choice == '4':
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please try again.")

def product_management_menu(inventory_manager):
    while True:
        print("\n" + "="*60)
        print("PRODUCT MANAGEMENT")
        print("="*60)
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Search Product")
        print("5. View All Products")
        print("6. Back to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            product_id = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            try:
                price = float(input("Enter Price: "))
                stock_quantity = int(input("Enter Stock Quantity: "))
                inventory_manager.add_product(product_id, name, price, stock_quantity)
            except ValueError:
                print("Invalid input! Price must be a number and stock quantity must be an integer.")
        
        elif choice == '2':
            product_id = input("Enter Product ID to update: ").strip()
            if product_id not in inventory_manager.products:
                print("Product not found!")
                continue
                
            current = inventory_manager.products[product_id]
            print(f"Current: Name={current.name}, Price=${current.price}, Stock={current.stock_quantity}")
            
            name = input("Enter new Name (leave blank to keep current): ").strip()
            price_str = input("Enter new Price (leave blank to keep current): ").strip()
            stock_str = input("Enter new Stock Quantity (leave blank to keep current): ").strip()
            
            price = float(price_str) if price_str else None
            stock_quantity = int(stock_str) if stock_str else None
            name = name if name else None
            
            inventory_manager.update_product(product_id, name, price, stock_quantity)
        
        elif choice == '3':
            product_id = input("Enter Product ID to delete: ").strip()
            inventory_manager.delete_product(product_id)
        
        elif choice == '4':
            keyword = input("Enter Product ID or Name to search: ").strip()
            results = inventory_manager.search_product(keyword)
            if results:
                print("\nSearch Results:")
                print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
                print("-"*60)
                for product in results:
                    print(f"{product.product_id:<10} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10}")
            else:
                print("No products found!")
        
        elif choice == '5':
            inventory_manager.view_all_products()
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice! Please try again.")

def billing_menu(billing_system):
    while True:
        print("\n" + "="*60)
        print("BILLING")
        print("="*60)
        print("1. Add to Cart")
        print("2. Remove from Cart")
        print("3. View Cart")
        print("4. Apply Discount")
        print("5. Checkout")
        print("6. Back to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            billing_system.inventory_manager.view_all_products()
            product_id = input("Enter Product ID: ").strip()
            try:
                quantity = int(input("Enter Quantity: "))
                billing_system.add_to_cart(product_id, quantity)
            except ValueError:
                print("Quantity must be an integer!")
        
        elif choice == '2':
            if not billing_system.cart:
                print("Cart is empty!")
                continue
                
            billing_system.view_cart()
            product_id = input("Enter Product ID: ").strip()
            quantity_str = input("Enter Quantity to remove (leave blank to remove all): ").strip()
            quantity = int(quantity_str) if quantity_str else None
            billing_system.remove_from_cart(product_id, quantity)
        
        elif choice == '3':
            billing_system.view_cart()
        
        elif choice == '4':
            if not billing_system.cart:
                print("Cart is empty!")
                continue
                
            discount_type = input("Enter discount type (percentage/fixed): ").strip().lower()
            try:
                value = float(input("Enter discount value: "))
                discount = billing_system.apply_discount(discount_type, value)
            except ValueError:
                print("Discount value must be a number!")
        
        elif choice == '5':
            sale = billing_system.checkout()
            if sale:
                save_bill = input("Do you want to save the bill? (y/n): ").strip().lower()
                if save_bill == 'y':
                    format_choice = input("Enter format (txt/csv): ").strip().lower()
                    billing_system.generate_bill(sale, format_choice)
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice! Please try again.")

def reports_menu(billing_system, inventory_manager):
    while True:
        print("\n" + "="*60)
        print("REPORTS")
        print("="*60)
        print("1. Daily Sales Report")
        print("2. Low Stock Report")
        print("3. Back to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
            try:
                if date_str:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                else:
                    target_date = datetime.now().date()
                
                daily_sales = billing_system.get_daily_sales(target_date)
                total_amount = sum(sale.final_amount for sale in daily_sales)
                
                print(f"\nSales Report for {target_date}:")
                print(f"Number of transactions: {len(daily_sales)}")
                print(f"Total sales: ${total_amount:.2f}")
                
                if daily_sales:
                    print("\nTransactions:")
                    for i, sale in enumerate(daily_sales, 1):
                        print(f"{i}. {sale.datetime.strftime('%H:%M:%S')} - ${sale.final_amount:.2f}")
            
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")
        
        elif choice == '2':
            threshold_str = input("Enter low stock threshold (default 5): ").strip()
            threshold = int(threshold_str) if threshold_str else 5
            
            low_stock = billing_system.get_low_stock_products(threshold)
            
            if low_stock:
                print(f"\nLow Stock Products (threshold: {threshold}):")
                print(f"{'ID':<10} {'Name':<20} {'Stock':<10}")
                print("-"*60)
                for product in low_stock:
                    print(f"{product.product_id:<10} {product.name:<20} {product.stock_quantity:<10}")
            else:
                print("No low stock products!")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":  # Fixed: double underscores around name and main
    main()
