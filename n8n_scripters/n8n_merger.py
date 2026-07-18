import mysql.connector, pandas as pd, os, sys, glob
from sqlalchemy import create_engine, text

# 1. Grab configuration arguments from n8n
# Usage: python file_merger.py "D:/My_Projects/Project" "amazon_products"
if len(sys.argv) < 3:
    print("Error: Missing directory_path or table_name arguments.")
    sys.exit(1)

target_directory = sys.argv[1]
table_name = sys.argv[2]
merged_output_path = os.path.join(target_directory, "merged_clean_products.csv")

# 2. Dynamic file search: Find all "clean_*.csv" in target directory
search_pattern = os.path.join(target_directory, "clean_*.csv")
clean_files = glob.glob(search_pattern)

if not clean_files:
    print(f"No clean files matching pattern '{search_pattern}' found.")
    sys.exit(0)

print(f"Found {len(clean_files)} files to merge: {clean_files}")

# 3. Read and concatenate whatever files exist
dfs = [pd.read_csv(f, encoding='latin1') for f in clean_files]
merged = pd.concat(dfs, ignore_index=True)

# 4. Filter missing rows, handle duplicates, and re-index
excluded_cols = list(merged.columns[-1:])  
excluded_cols += [col for col in merged.columns if col.startswith('url')]
columns_check = [col for col in merged.columns if col not in excluded_cols]

is_nan = merged[columns_check].isna()
is_blank = merged[columns_check].astype(str).map(lambda x: x.strip() == '')
rows_to_drop = (is_nan | is_blank).any(axis=1)
clean_df = merged[~rows_to_drop].reset_index(drop=True)

clean_df['UID'] = clean_df['UID'].astype(str).str.strip()
clean_df = clean_df.drop_duplicates(subset=['UID'], keep='first').reset_index(drop=True)

clean_df[' '] = ' '
clean_df = clean_df.sort_values(by='SubCategory', key=lambda col: col.str.lower()).reset_index(drop=True)
clean_df['Sr.No'] = range(1, len(clean_df) + 1)

# Save master CSV
clean_df.to_csv(merged_output_path, index=False)

# ── MySQL Engine Setup ──
engine = create_engine('mysql+mysqlconnector://root:AmAzInG%4012@127.0.0.1/product_data')

insert_df = clean_df.drop(columns=[' '], errors='ignore')
insert_df = insert_df.rename(columns={'Sr.No': 'Sr_No'})
insert_df = insert_df.where(pd.notnull(insert_df), None)

# Typecasting
insert_df['Rating'] = pd.to_numeric(insert_df['Rating'], errors='coerce')
insert_df['Review_Count'] = pd.to_numeric(insert_df['Review_Count'], errors='coerce').astype('Int64')
insert_df['MRP'] = pd.to_numeric(insert_df['MRP'], errors='coerce')
insert_df['Price'] = pd.to_numeric(insert_df['Price'], errors='coerce')

# ── SQL Execution ──
with engine.begin() as conn:
    # 1. Truncate master table and write new merged data
    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
    insert_df.to_sql(table_name, con=conn, if_exists='append', index=False)
    print(f"{len(insert_df)} rows inserted into {table_name}!")

    # 2. Refresh dynamic summary table (forced limit 650)
    conn.execute(text(f"""
        INSERT INTO categorical_summary 
            (Category, SubCategory, Top_Brand, Top_Manufacturer, Best_Product, 
             Product_Count, Average_Rating, Average_Discount, Brand_Count)
        SELECT 
            p.Category, p.SubCategory,

            (SELECT Brand FROM {table_name} sub
             WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory
               AND sub.Brand != 'Not Found' AND sub.Brand IS NOT NULL
             GROUP BY Brand ORDER BY COUNT(*) DESC LIMIT 1) AS Top_Brand,

            (SELECT Manufacturer FROM {table_name} sub
             WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory
               AND sub.Manufacturer != 'Not Found' AND sub.Manufacturer IS NOT NULL
             GROUP BY Manufacturer ORDER BY COUNT(*) DESC LIMIT 1) AS Top_Manufacturer,

            (SELECT Product_Name FROM {table_name} sub
             WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory
             ORDER BY Rating DESC LIMIT 1) AS Best_Product,

            COUNT(*) AS Product_Count,
            ROUND(AVG(p.Rating), 2) AS Average_Rating,
            ROUND(AVG(REPLACE(p.Discount, '%', '')), 2) AS Average_Discount,
            COUNT(DISTINCT p.Brand) AS Brand_Count 

        FROM (
            SELECT *, 
                   ROW_NUMBER() OVER (
                       PARTITION BY Category, SubCategory 
                       ORDER BY Rating DESC
                   ) as row_num
            FROM {table_name}
        ) p
        WHERE p.row_num <= 650
        GROUP BY p.Category, p.SubCategory
        
        ON DUPLICATE KEY UPDATE
            Top_Brand        = VALUES(Top_Brand),
            Top_Manufacturer = VALUES(Top_Manufacturer),
            Best_Product     = VALUES(Best_Product),
            Product_Count    = VALUES(Product_Count),
            Average_Rating   = VALUES(Average_Rating),
            Average_Discount = VALUES(Average_Discount),
            Brand_Count      = VALUES(Brand_Count)
    """))
    print("categorical_summary refreshed!")