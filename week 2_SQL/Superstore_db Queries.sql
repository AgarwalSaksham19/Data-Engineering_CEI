CREATE DATABASE superstore_db;
USE superstore_db;
#1. Load dataset into a SQL database.
SHOW TABLES;
SELECT * FROM `sample - superstore` LIMIT 10;
RENAME TABLE `sample - superstore` TO superstore;
#2.Explore table (schema, sample data):
SELECT * FROM superstore LIMIT 10;
SELECT COUNT(*) AS Total_Rows FROM superstore;
#3.Apply WHERE filters (region, category, date, sales).
SELECT * FROM superstore WHERE Region='West';
SELECT * FROM superstore WHERE Category='Furniture';
SELECT * FROM superstore WHERE Sales>500;
SELECT * FROM superstore WHERE `Order Date` BETWEEN '2016-01-01' AND '2016-12-31';
#4.Use GROUP BY for aggregations (sales, quantity, averages).
SELECT Region,SUM(Sales) AS TotalSales FROM superstore GROUP BY Region;
SELECT Category,AVG(Sales) AS AvgSales FROM superstore GROUP BY Category;
SELECT Category,SUM(Quantity) AS TotalQuantity FROM superstore GROUP BY Category;
SELECT Segment,SUM(Profit) AS TotalProfit FROM superstore GROUP BY Segment;

# 5.Sort and limit results (top products, top categories).
SELECT `Product Name`,SUM(Sales) AS TotalSales FROM superstore GROUP BY `Product Name` ORDER BY TotalSales DESC LIMIT 10;
SELECT Category,SUM(Sales) AS TotalSales FROM superstore GROUP BY Category ORDER BY TotalSales DESC;
SELECT * FROM superstore ORDER BY Profit DESC LIMIT 10;

#6.Solve use cases (monthly trends, top customers, duplicates).
SELECT YEAR(STR_TO_DATE(`Order Date`,'%m/%d/%Y')) AS Year,MONTH(STR_TO_DATE(`Order Date`,'%m/%d/%Y')) AS Month,SUM(Sales) AS TotalSales FROM superstore GROUP BY Year,Month ORDER BY Year,Month;
SELECT `Customer Name`,SUM(Sales) AS TotalSales FROM superstore GROUP BY `Customer Name` ORDER BY TotalSales DESC LIMIT 10;
SELECT `Product Name`,SUM(Quantity) AS TotalQuantity FROM superstore GROUP BY `Product Name` ORDER BY TotalQuantity DESC LIMIT 10;
SELECT State,SUM(Profit) AS TotalProfit FROM superstore GROUP BY State ORDER BY TotalProfit DESC;

# 7.Validate results (row counts, data quality)
SELECT COUNT(*) FROM superstore;
SELECT COUNT(DISTINCT `Customer ID`) FROM superstore;
SELECT COUNT(DISTINCT `Product Name`) FROM superstore;
SELECT MIN(Sales),MAX(Sales) FROM superstore;

/* Data quality is good */

#T he Superstore dataset was successfully explored using SQL queries to understand its structure and contents.
# WHERE filters were applied to analyze records based on region, category, sales amount, and order dates.
# GROUP BY operations were used to calculate total sales, profit, and quantity across different categories and regions.
# Sorting and limiting techniques helped identify the top-performing products and categories based on sales.
# Customer analysis revealed the customers contributing the highest sales revenue.
# Duplicate checks showed that some Order IDs appear multiple times because a single order may contain multiple products.
# Data validation queries were performed to verify row counts and check for data quality issues.
