USE product_data;

-- Example: Query to manually calculate metrics from raw table.
-- I used these queries while developing.
-- This runs as a logic inside the n8n python execution pipeline.
INSERT INTO categorical_summary 
	(
		Category, SubCategory, Top_Brand, Top_Manufacturer, Best_Product,
        Product_Count, Average_Rating, Average_Discount, Brand_Count
	) 
SELECT 
    p.Category, p.SubCategory,
    (
		SELECT Brand FROM amazon_products sub 
        WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory 
        AND sub.Brand != 'Not found' AND sub.Brand IS NOT NULL 
        GROUP BY Brand ORDER BY COUNT(*) DESC LIMIT 1
	) AS Top_Brand, 
    (
		SELECT Manufacturer FROM amazon_products sub 
        WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory 
        AND sub.Manufacturer != 'Not found' AND sub.Manufacturer IS NOT NULL 
        GROUP BY Manufacturer ORDER BY COUNT(*) DESC LIMIT 1
	) AS Top_Manufacturer,
    (
		SELECT Product_Name FROM amazon_products sub 
        WHERE sub.Category = p.Category AND sub.SubCategory = p.SubCategory 
        ORDER BY Rating DESC LIMIT 1
	) AS Best_Product,
    COUNT(*) AS Product_Count,
    ROUND(AVG(p.Rating), 2) AS Average_Rating,
    ROUND(AVG(CAST(REPLACE(p.Discount, '%', '') AS DECIMAL)), 2) AS Average_Discount,
    COUNT(DISTINCT p.Brand) AS Brand_Count
FROM amazon_products p
GROUP BY p.Category, p.SubCategory;

-- These are the scripts that I used during developing this project.

select column_name, data_type from INFORMATION_SCHEMA.columns 
where table_name= 'amazon_products';
select * from amazon_products;
select count(*) from amazon_products;

select * from categorical_summary;
select count(*) from categorical_summary;

