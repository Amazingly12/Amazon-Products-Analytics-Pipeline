USE product_data;

-- Competition Density and Analytics View (For Tableau Dashboard)
CREATE OR REPLACE VIEW competition_density AS
WITH base AS (
    SELECT
        cs.Category, 
        cs.SubCategory, 
        cs.Product_Count,
        cs.Average_Rating, 
        cs.Average_Discount, 
        cs.Brand_Count,
        
        -- Review Velocity: avg reviews per product (safely handles zeros or nulls)
        ROUND(COALESCE(SUM(p.Review_Count), 0) / NULLIF(cs.Product_Count, 0), 2) AS Review_Velocity,

        -- Price Variance: Standard deviation of pricing strategy
        ROUND(COALESCE(STDDEV(p.Price), 0), 2) AS Price_Variance
    FROM categorical_summary cs
    LEFT JOIN amazon_products p 
        ON cs.Category = p.Category AND cs.SubCategory = p.SubCategory
    GROUP BY cs.Category, cs.SubCategory, cs.Product_Count, 
             cs.Average_Rating, cs.Average_Discount, cs.Brand_Count
),

normalized AS (
    SELECT *,
        -- Window function maximums used to score items evenly out of 100
        ROUND((Brand_Count / NULLIF(MAX(Brand_Count) OVER(), 0)) * 100, 2) AS Seller_Concentration,
        ROUND((Review_Velocity / NULLIF(MAX(Review_Velocity) OVER(), 0)) * 100, 2) AS Review_Velocity_Norm,
        ROUND((Price_Variance / NULLIF(MAX(Price_Variance) OVER(), 0)) * 100, 2) AS Price_Variance_Norm
    FROM base
)

SELECT
    Category,
    SubCategory,
    Product_Count,
    Brand_Count,
    Review_Velocity,
    Price_Variance,
    Seller_Concentration,
    Review_Velocity_Norm,
    Price_Variance_Norm,

    -- Weighted Matrix Competition Density Score Formula
    ROUND(
        (COALESCE(Seller_Concentration, 0) * 0.40) +
        (COALESCE(Review_Velocity_Norm, 0) * 0.35) +
        (COALESCE(Price_Variance_Norm, 0) * 0.25), 2
    ) AS Competition_Density_Score
FROM normalized;


-- Price Tag Intelligence Core Summary View
CREATE OR REPLACE VIEW tagintel_summary AS
SELECT 
    Sr_No,
    UID,
    Product_Name,
    Brand,
    Category,
    SubCategory,
    Price,
    MRP,
    Discount,
    Rating,
    Review_Count,
    seo_url
FROM amazon_products;