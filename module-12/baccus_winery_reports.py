# MAKE SURE TO DO pip install pandas, matplotlib, before running this script. If you have issues installing,
# Try using pip install --user pandas matplotlib or pandas to install in your local environment.

import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ------------ Report 1: Supplier Delivery Performance ------------
# This report evaluates supplier on-time delivery by calculating the difference 
# between the 'Order date' and 'Arrive by' dates for delivered orders.
# Orders with a "skipped" status are excluded from the analysis.
# The report shows the average delivery time per vendor and per month.

purchase_orders_data = {
    'Order': ['P3', 'P1', 'P2', 'P0', 'P1', 'P1'],
    'Category': ['Bottles and Corks', 'Labels and Boxes', 'Vats and Tubiing', 'Bottles and Corks', 'Labels and Boxes', 'Vats and Tubing'],
    'Status': ['Ordered', 'Delivered', 'Delivered', 'skipped', 'Delivered', 'Shipped'],
    'Order date': ['5/1/2024', '5/1/2024', '5/1/2024', 'N/A', '6/1/2024', '6/1/2024'],
    'Arrive by': ['tbd', '6/28/2024', '6/30/2024', 'N/A', '7/3/2024', '7/2/2024'],
    'Point of contact': ['vendor 1', 'vendor 2', 'vendor 3', 'vendor 1', 'vendor 2', 'vendor 3'],
}

df_purchase_orders = pd.DataFrame(purchase_orders_data)

date_format = "%m/%d/%Y"
df_purchase_orders['Order date'] = pd.to_datetime(df_purchase_orders['Order date'], format=date_format, errors='coerce')
df_purchase_orders['Arrive by'] = pd.to_datetime(df_purchase_orders['Arrive by'], format=date_format, errors='coerce')

# Remove skipped orders
df_filtered = df_purchase_orders[(df_purchase_orders['Status'] != 'skipped')].copy()

df_filtered.loc[df_filtered['Status'] == 'Delivered', 'delivery_time'] = (
    df_filtered['Arrive by'] - df_filtered['Order date']
).dt.days

monthly_delivery_time = df_filtered.groupby(['Point of contact', pd.Grouper(key='Order date', freq='MS')])['delivery_time'].mean().reset_index()
monthly_delivery_time = monthly_delivery_time.rename(columns={'delivery_time': 'avg_delivery_time_days'})

print("\n--- Report 1: Supplier Delivery Performance ---\n")
print(monthly_delivery_time.fillna('Not Delivered Yet'))  


# Plotting Report 1
plt.figure(figsize=(12, 6))
for vendor in monthly_delivery_time['Point of contact'].unique():
    vendor_data = monthly_delivery_time[monthly_delivery_time['Point of contact'] == vendor]
    # Only plot delivered bars
    plt.bar(vendor_data['Order date'], vendor_data['avg_delivery_time_days'].dropna(), label=vendor) 

plt.xlabel('Order Date')
plt.ylabel('Average Delivery Time (days)')
plt.title('Supplier Delivery Performance by Month')
plt.legend()
plt.xticks(rotation=45)
plt.show()



# ------------ Report 2: Wine Distribution and Sales ------------
# This report analyzes wine sales by product and sales platform (online vs. in-store).
# It helps identify the top-selling products and the most effective sales channels.

# Data for Sales Orders
sales_orders_data = {
    'Order': ['P0', 'P1', 'P2', 'P3'],
    'Product': ['Chardonnay', 'Merlot', 'Chablis', 'Cabernet'],
    'Status': ['Shipped', 'Delivered', 'Delivered', 'Shipped'],
    'Order Date/Last Sold': ['7/10/2024', '7/9/2024', '6/12/2024', '6/30/2024'],
    'Sales Platform': ['Online', 'In store', 'In store', 'Online'],
    'How many orders/sales?': [65, 78, 12, 23]
}

df_sales_orders = pd.DataFrame(sales_orders_data)

df_included_orders = df_sales_orders.copy()

df_included_orders = df_included_orders.rename(columns={'How many orders/sales?': 'Sales/Orders'})

# Aggregate sales by Product and Sales Platform (including all statuses)
sales_by_product_platform = df_included_orders.groupby(['Product', 'Sales Platform', 'Status'])['Sales/Orders'].sum().reset_index()

print("\n--- Report 2: Wine Distribution and Sales ---\n")
print(sales_by_product_platform)

# Plotting Report 2 
plt.figure(figsize=(10, 6))

products = df_sales_orders['Product'].unique()
platforms = df_sales_orders['Sales Platform'].unique()

# Colors for different statuses
status_colors = {'Delivered': 'skyblue', 'Shipped': 'lightgreen'}
hatch_patterns = {'Delivered': '', 'Shipped': '///'}  

for i, product in enumerate(products):
    for j, platform in enumerate(platforms):
        # Get sales/orders for the current product and platform
        order_data = sales_by_product_platform[(sales_by_product_platform['Product'] == product) & (sales_by_product_platform['Sales Platform'] == platform)]

        # Handle the case where there are no sales/orders for a specific combination
        if len(order_data) == 0:
            continue
            
        sales_orders = order_data['Sales/Orders'].values[0]  # Extract sales/orders from the filtered DataFrame
        status = order_data['Status'].values[0]  # Extract status from the filtered DataFrame

        # Plot bars with different colors and hatch patterns based on status
        plt.bar(i + (j - 1) * 0.2, sales_orders, width=0.2, label=f"{platform} ({status})" if i == 0 else "", color=status_colors[status], hatch=hatch_patterns[status])


# Add labels and title
plt.xlabel('Product')
plt.ylabel('Sales/Orders')
plt.title('Wine Sales/Orders by Product and Platform')
plt.xticks(range(len(products)), products)
plt.legend()

plt.show()

# ------------ Report 3: Employee Hours Summary and Analysis ------------
# This report provides a summary and analysis of employee hours worked based on quarterly data. 
# It includes total hours worked per employee, summary statistics, and a histogram visualizing 
# the distribution of hours worked.

# Data for Employee Hours (Corrected column name)
employee_hours_data = {
    'Employee': ['Janet Collins', 'Roz Murphy', 'Bob Ulrich', 'Henry Doyle', 'Maria Costanza'],
    'Q1': [520.00, 450.00, 300.00, 400.00, 439.00],
    'Q2': [522.00, 452.00, 500.00, 300.00, 271.00],
    'Q3': [530.00, 350.00, 437.00, 235.00, 237.00],
    'Q4': [500.00, 400.00, 232.00, 348.00, 245.00],
}
df_employee_hours = pd.DataFrame(employee_hours_data)

# Calculate total hours per employee
df_employee_hours['Total Hours'] = df_employee_hours['Q1'] + df_employee_hours['Q2'] + df_employee_hours['Q3'] + df_employee_hours['Q4']

# Display summary statistics
print("\n--- Report 3: Employee Hours Summary and Analysis ---\n")
print("Summary Statistics:")
print(df_employee_hours['Total Hours'].describe())
print("\n")

# Display hours worked for each employee
print("Hours Worked by Employee:")
print(df_employee_hours[['Employee', 'Total Hours']])
print("\n")

# Create and display histogram
plt.figure(figsize=(10, 6))
plt.hist(df_employee_hours['Total Hours'], bins=10, edgecolor='k', alpha=0.3)
plt.xlabel('Total Hours Worked')
plt.ylabel('Number of Employees')
plt.title('Distribution of Total Hours Worked by Employees')
plt.grid(axis='y', alpha=0.5)

plt.show()