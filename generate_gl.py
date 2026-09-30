import pandas as pd
import numpy as np
import datetime
import random

random.seed(42)
np.random.seed(42)

# Load existing dimension tables
accounts_df = pd.read_csv('seeds/D_Accounts.csv')
dealer_df = pd.read_csv('seeds/D_Dealer.csv')
ee_df = pd.read_csv('seeds/D_EE.csv')  # use 'seeds/D_EE.csv' if you moved D_EE into seeds
sku_df = pd.read_csv('seeds/D_SKU.csv')

# Filter SKU categories
veh_skus = sku_df[sku_df['SKU_Type'] == 'Vehicle']
part_skus = sku_df[sku_df['SKU_Type'] == 'Part']
svc_skus = sku_df[sku_df['SKU_Type'] == 'Service']

# Filter Employee types
ee_sales = ee_df[ee_df['Employee_Type'] == 'Sales']
ee_svc = ee_df[ee_df['Employee_Type'] == 'Service']
ee_parts = ee_df[ee_df['Employee_Type'] == 'Parts']

start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 12, 31)
days = (end_date - start_date).days + 1

rows = []
journal_id = 100001

for day_idx in range(days):
    curr_date = start_date + datetime.timedelta(days=day_idx)
    date_str = curr_date.strftime('%Y-%m-%d')
    
    for dealer_id in range(1, 5):
        
        # --- 1. Vehicle Sales ---
        # Only select vehicles mapped specifically to this dealership
        dealer_veh_skus = veh_skus[veh_skus['Dealership'] == dealer_id]
        
        num_veh_sales = random.randint(2, 5)
        for _ in range(num_veh_sales):
            is_new = random.random() < 0.6
            veh_sku_row = dealer_veh_skus.sample(1).iloc[0]
            sku_id = veh_sku_row['SKU']
            
            dealer_sales = ee_sales[ee_sales['Dealership_ID'] == dealer_id]
            ee_id = dealer_sales.sample(1).iloc[0]['Employee_ID'] if len(dealer_sales) > 0 else np.nan
            
            if is_new:
                sale_price = round(random.uniform(32000, 58000), 2)
                margin = random.uniform(0.04, 0.07)
                cogs = round(sale_price * (1 - margin), 2)
                rev_acc, cogs_acc = 8, 12
                desc_sale = f"New Vehicle Sale: {veh_sku_row['Description']}"
            else:
                sale_price = round(random.uniform(14000, 32000), 2)
                margin = random.uniform(0.10, 0.16)
                cogs = round(sale_price * (1 - margin), 2)
                rev_acc, cogs_acc = 9, 13
                desc_sale = f"Used Vehicle Sale: {veh_sku_row['Description']}"
                
            comm_amt = round(sale_price * random.uniform(0.02, 0.035), 2)
            
            rows.append([journal_id, date_str, dealer_id, 1, sku_id, ee_id, sale_price, 0.0, desc_sale])
            rows.append([journal_id, date_str, dealer_id, rev_acc, sku_id, ee_id, 0.0, sale_price, desc_sale])
            journal_id += 1
            
            rows.append([journal_id, date_str, dealer_id, cogs_acc, sku_id, ee_id, cogs, 0.0, f"COGS - {veh_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 3, sku_id, ee_id, 0.0, cogs, f"Inventory Relief - {veh_sku_row['Description']}"])
            journal_id += 1
            
            rows.append([journal_id, date_str, dealer_id, 16, sku_id, ee_id, comm_amt, 0.0, f"Commission - {veh_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 6, sku_id, ee_id, 0.0, comm_amt, f"Accrued Commission - {veh_sku_row['Description']}"])
            journal_id += 1

        # --- 2. Service Repair Orders ---
        # Select service SKUs mapped to this dealer OR universal (NaN / 5)
        dealer_svc_skus = svc_skus[(svc_skus['Dealership'] == dealer_id) | (svc_skus['Dealership'].isna()) | (svc_skus['Dealership'] == 5)]
        
        for _ in range(random.randint(5, 12)):
            svc_sku_row = dealer_svc_skus.sample(1).iloc[0]
            sku_id = svc_sku_row['SKU']
            
            dealer_svc_ees = ee_svc[ee_svc['Dealership_ID'] == dealer_id]
            ee_id = dealer_svc_ees.sample(1).iloc[0]['Employee_ID'] if len(dealer_svc_ees) > 0 else np.nan
            
            svc_rev = round(random.uniform(150, 950), 2)
            labor_cogs = round(svc_rev * random.uniform(0.32, 0.40), 2)
            
            rows.append([journal_id, date_str, dealer_id, 1, sku_id, ee_id, svc_rev, 0.0, f"Service - {svc_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 10, sku_id, ee_id, 0.0, svc_rev, f"Service Rev - {svc_sku_row['Description']}"])
            journal_id += 1
            
            rows.append([journal_id, date_str, dealer_id, 14, sku_id, ee_id, labor_cogs, 0.0, f"Service Labor COGS - {svc_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 17, sku_id, ee_id, 0.0, labor_cogs, f"Tech Payroll Accrual - {svc_sku_row['Description']}"])
            journal_id += 1

        # --- 3. Parts Sales ---
        # Select parts SKUs mapped to this dealer OR universal (NaN / 5)
        dealer_part_skus = part_skus[(part_skus['Dealership'] == dealer_id) | (part_skus['Dealership'].isna()) | (part_skus['Dealership'] == 5)]
        
        for _ in range(random.randint(4, 10)):
            part_sku_row = dealer_part_skus.sample(1).iloc[0]
            sku_id = part_sku_row['SKU']
            
            dealer_parts_ees = ee_parts[ee_parts['Dealership_ID'] == dealer_id]
            ee_id = dealer_parts_ees.sample(1).iloc[0]['Employee_ID'] if len(dealer_parts_ees) > 0 else np.nan
            
            parts_rev = round(random.uniform(35, 450), 2)
            parts_cogs = round(parts_rev * random.uniform(0.60, 0.68), 2)
            
            rows.append([journal_id, date_str, dealer_id, 1, sku_id, ee_id, parts_rev, 0.0, f"Parts Sale - {part_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 11, sku_id, ee_id, 0.0, parts_rev, f"Parts Rev - {part_sku_row['Description']}"])
            journal_id += 1
            
            rows.append([journal_id, date_str, dealer_id, 15, sku_id, ee_id, parts_cogs, 0.0, f"Parts COGS - {part_sku_row['Description']}"])
            rows.append([journal_id, date_str, dealer_id, 4, sku_id, ee_id, 0.0, parts_cogs, f"Parts Inv Relief - {part_sku_row['Description']}"])
            journal_id += 1

    # Monthly Expenses (1st of month)
    if curr_date.day == 1:
        for dealer_id in range(1, 5):
            expenses = [
                (18, round(random.uniform(14000, 18000), 2), "Monthly Rent & Occupancy"),
                (19, round(random.uniform(2500, 4200), 2), "Monthly Utilities"),
                (20, round(random.uniform(6000, 12000), 2), "Marketing & Local Advertising"),
                (21, round(random.uniform(3000, 5000), 2), "Property & Liability Insurance"),
                (22, round(random.uniform(1500, 3500), 2), "Facility Maintenance"),
                (23, round(random.uniform(4000, 7000), 2), "Equipment Depreciation"),
                (24, round(random.uniform(2000, 4500), 2), "Office & Admin Supplies"),
                (25, round(random.uniform(1000, 2500), 2), "Sundry Operating Expenses")
            ]
            for acc_id, amt, desc in expenses:
                rows.append([journal_id, date_str, dealer_id, acc_id, np.nan, np.nan, amt, 0.0, desc])
                rows.append([journal_id, date_str, dealer_id, 1, np.nan, np.nan, 0.0, amt, f"Cash Payment - {desc}"])
                journal_id += 1

cols = ["Journal_ID", "Posting_Date", "Dealership_ID", "Account_ID", "SKU", "Employee_ID", "Debit", "Credit", "Description"]
fact_df = pd.DataFrame(rows, columns=cols)
fact_df.to_csv("seeds/F_Journal_Entries.csv", index=False)
print("F_Journal_Entries.csv generated successfully.")