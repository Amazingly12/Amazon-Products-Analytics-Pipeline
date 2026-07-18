import pandas as pd, re, random, os, sys


if len(sys.argv) < 3:
    print("Error: Missing input_file or output_file arguments.")
    sys.exit(1)
    
df1 = sys.argv[1]
output_file = sys.argv[2]
df = pd.read_csv(df1, encoding = 'latin1')

img_col = [col for col in df.columns if col.startswith("url")]

def normalize_url(url):
    if pd.isna(url) or url.strip() == '':
        return ''
    if any(bad in url for bad in ["overlay", "PKdp-play-icon", "BR-", "BG", "sprite", "icon", "360_icon"]):
        return ''
    return re.sub(r'\._[A-Z0-9,]+_\.', '.', url)

df_normalized = df[img_col].map(normalize_url)

def deduplicate_row(row):
    seen = set()
    unique_urls = []
    for url in row:
        if url and url not in seen:
            seen.add(url)
            unique_urls.append(url)
    return pd.Series(unique_urls + [' '] * (len(row) - len(unique_urls)))

df_cleaned = df_normalized.apply(deduplicate_row, axis = 1)
df[img_col] = df_cleaned

df['discount_percent'] = df['discount_percent'].astype(str).str.replace(r'[^\d]', '', regex=True)
df['discount_percent'] = df['discount_percent'].replace('', '0').astype(int)
df['discount_percent'] = df['discount_percent'].astype(object)
df.loc[df['discount_percent']>0, 'discount_percent'] = df['discount_percent'].astype(str) + '%'

desired_order = [
    'Sr.No', 'Scraped_Date', 'uid', 'url', 'title', 'description', 'brand', 'Manufacturer', 'category', 'subcategory', 'price', 'mrp', 'discount_percent',
    'rating', 'review_count', 'seo_url']
other_col = [col for col in df.columns if col not in desired_order]

df = df[desired_order + other_col]

renamed_col = {
    'uid': 'UID', 'url': 'URL', 'title': 'Product_Name', 'description': 'Description', 'brand': 'Brand', 'category': 'Category', 'subcategory': 
    'SubCategory', 'price': 'Price', 'mrp': 'MRP', 'discount_percent': 'Discount', 'rating': 'Rating', 'review_count': 'Review_Count'}
df = df.rename(columns = renamed_col)

df.to_csv(output_file, index=False)