-- Startup run
create database if not exists product_data;
use product_data;
SET GLOBAL local_infile = 1;

-- Master Table for all Amazon Products
CREATE TABLE IF NOT EXISTS amazon_products (   
    Sr_No INT,
    Scraped_Date VARCHAR(50),      
    UID VARCHAR(50),               
    URL TEXT,
    Product_Name TEXT,
    Description TEXT,              
    Brand VARCHAR(100),
    Manufacturer TEXT,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Price DECIMAL(10, 2),          
    MRP DECIMAL(10, 2),
    Discount VARCHAR(20),          
    Rating DECIMAL(3, 1),          
    Review_Count INT,              
    seo_url VARCHAR(255),
    url1 VARCHAR(500), url2 VARCHAR(500), url3 VARCHAR(500), url4 VARCHAR(500),
    url5 VARCHAR(500), url6 VARCHAR(500), url7 VARCHAR(500), url8 VARCHAR(500),
    PRIMARY KEY (UID)             -- Optimized for lookup and avoiding scrapers duplicates
);

-- Summary Metrics Table
CREATE TABLE IF NOT EXISTS categorical_summary (
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Top_Brand text,
    Top_Manufacturer text,
    Best_Product text,
    Product_Count INT,
    Average_Rating DECIMAL(10, 2),
    Average_Discount DECIMAL(10, 2),
    Brand_Count INT,
    PRIMARY KEY (Category, SubCategory)
);