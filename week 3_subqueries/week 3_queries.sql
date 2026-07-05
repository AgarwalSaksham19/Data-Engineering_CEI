USE student_db;
ALTER TABLE superstore RENAME TO superstore_raw;   
show tables;
DROP TABLE customers;
CREATE TABLE customers (customer_id VARCHAR(20), customer_name VARCHAR(100), 
segment VARCHAR(50), country VARCHAR(50), city VARCHAR(100), state VARCHAR(100), postal_code INT, region VARCHAR(50));
INSERT INTO customers (customer_id, customer_name, segment, country, city, state, postal_code, region) 
SELECT DISTINCT `Customer ID`, `Customer Name`, Segment, Country, City, State, `Postal Code`, Region FROM superstore_raw;
SELECT * FROM customers LIMIT 10;
CREATE TABLE products (product_id VARCHAR(30), category VARCHAR(50), sub_category VARCHAR(50), product_name VARCHAR(255));
INSERT INTO products (product_id, category, sub_category, product_name) SELECT DISTINCT `Product ID`, Category, `Sub-Category`, `Product Name` FROM superstore_raw;
SELECT * FROM products LIMIT 10;
CREATE TABLE orders (row_id INT, order_id VARCHAR(30), order_date DATE, ship_date DATE, ship_mode VARCHAR(50), 
customer_id VARCHAR(20), product_id VARCHAR(30), sales DECIMAL(10,2), quantity INT, discount DECIMAL(5,2), profit DECIMAL(10,2));
INSERT INTO orders (row_id, order_id, order_date, ship_date, ship_mode, customer_id, product_id, sales, quantity, discount, profit)  
SELECT DISTINCT 
    `Row ID`, 
    `Order ID`, 
    STR_TO_DATE(`Order Date`, '%m/%d/%Y'), 
    STR_TO_DATE(`Ship Date`, '%m/%d/%Y'), 
    `Ship Mode`, 
    `Customer ID`, 
    `Product ID`, 
    CAST(REPLACE(REPLACE(Sales, '$', ''), ',', '') AS DECIMAL(15,2)), 
    Quantity, 
    Discount, 
    CAST(REPLACE(REPLACE(Profit, '$', ''), ',', '') AS DECIMAL(15,2)) 
FROM superstore_raw;
ALTER TABLE orders 
MODIFY COLUMN sales DECIMAL(15,2),
MODIFY COLUMN profit DECIMAL(15,2);
SELECT * FROM orders LIMIT 10;
SHOW TABLES;

#1. Find all orders where sales are greater than the average sales (Subquery)
SELECT * FROM orders WHERE sales > (SELECT AVG(sales) FROM orders);

#2. Find the highest sales order for each customer (Subquery)
SELECT o.*
FROM orders o
INNER JOIN (
    -- This subquery finds the highest sales amount for each customer first
    SELECT customer_id, MAX(sales) AS max_sales
    FROM orders
    GROUP BY customer_id
) sub 
ON o.customer_id = sub.customer_id AND o.sales = sub.max_sales;

#3. Calculate total sales for each customer (CTE)
WITH customer_sales AS (SELECT customer_id, SUM(sales) AS total_sales FROM orders GROUP BY customer_id) 
SELECT * FROM customer_sales;

#4. Find customers whose total sales are above average (CTE + Subquery)
WITH customer_sales AS (SELECT customer_id, SUM(sales) AS total_sales FROM orders GROUP BY customer_id) 
SELECT * FROM customer_sales WHERE total_sales > (SELECT AVG(total_sales) FROM customer_sales);

#5. Rank all customers based on total sales (Window Function)
SELECT customer_id, SUM(sales) AS total_sales, RANK() OVER (ORDER BY SUM(sales) DESC) AS customer_rank FROM orders GROUP BY customer_id;

#6. Assign row numbers to each order within a customer (Window Function + PARTITION BY)
SELECT customer_id, order_id, order_date, sales, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_number FROM orders;

#7. Display top 3 customers based on total sales (Window Function)
WITH ranked_customers AS (SELECT customer_id, SUM(sales) AS total_sales, RANK() OVER (ORDER BY SUM(sales) DESC) AS customer_rank FROM orders GROUP BY customer_id) 
SELECT * FROM ranked_customers WHERE customer_rank <= 3;

#(Use JOIN + CTE + Window Function together) 
WITH customer_sales AS (SELECT o.customer_id, c.customer_name, SUM(o.sales) AS total_sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
GROUP BY o.customer_id, c.customer_name) SELECT customer_name, total_sales, RANK() OVER (ORDER BY total_sales DESC) AS customer_rank FROM customer_sales;


#Mini Project: Customer Sales Insights.

#1. Who are the Top 5 Customers?
SELECT c.customer_name, SUM(o.sales) AS total_sales FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name ORDER BY total_sales DESC LIMIT 5;

#2. Who are the Bottom 5 Customers?
SELECT c.customer_name, SUM(o.sales) AS total_sales FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name ORDER BY total_sales ASC LIMIT 5;

#3. Which Customers Made Only One Order?
SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS total_orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name HAVING COUNT(DISTINCT o.order_id) = 1;

#4. Which Customers Have Above-Average Sales?
WITH customer_sales AS (SELECT c.customer_id, c.customer_name, SUM(o.sales) AS total_sales FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name)SELECT customer_name, total_sales FROM customer_sales WHERE total_sales > (SELECT AVG(total_sales) FROM customer_sales);

#5. What Is the Highest Order Value per Customer?
SELECT c.customer_name, MAX(o.sales) AS highest_order_value FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name ORDER BY highest_order_value DESC;