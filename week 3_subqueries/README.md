# Customer Sales Insights using SQL

## Overview

This project analyzes the **Sample Superstore** dataset using SQL in **MySQL Workbench**. It demonstrates the use of **Subqueries**, **Common Table Expressions (CTEs)**, **Window Functions**, and **JOINs** to generate meaningful customer sales insights.

## Objectives

* Import and organize the Superstore dataset.
* Create normalized tables from the raw data.
* Perform data analysis using SQL.
* Apply advanced SQL concepts including:

  * Subqueries
  * Common Table Expressions (CTEs)
  * Window Functions
  * JOINs
  * Aggregate Functions

## Dataset

* **Dataset:** Sample Superstore
* **Source:** Retail sales dataset commonly used for SQL and data analytics practice.
* **Database:** MySQL
* **Tool:** MySQL Workbench

## Database Tables

* **superstore_raw** – Original imported dataset
* **customers** – Customer information
* **products** – Product information
* **orders** – Order and sales information

## SQL Tasks Performed

### Step 1: Data Setup

* Imported the Superstore dataset into `superstore_raw`
* Created `customers`, `products`, and `orders` tables
* Populated the tables using `SELECT DISTINCT`

### Step 2: SQL Analysis

* Found orders with sales greater than the average sales
* Retrieved the highest sales order for each customer
* Calculated total sales for each customer using a CTE
* Identified customers with above-average sales
* Ranked customers based on total sales
* Assigned row numbers to orders within each customer
* Displayed the top 3 customers by total sales

### Step 3: Final Combined Query

Created a query using:

* JOIN
* Common Table Expression (CTE)
* Window Function

The final output includes:

* Customer Name
* Total Sales
* Customer Rank

### Mini Project: Customer Sales Insights

* Top 5 customers by total sales
* Bottom 5 customers by total sales
* Customers who placed only one order
* Customers with above-average sales
* Highest order value for each customer

## SQL Concepts Used

* SELECT
* DISTINCT
* GROUP BY
* ORDER BY
* Aggregate Functions (`SUM`, `AVG`, `MAX`, `COUNT`)
* Subqueries
* Common Table Expressions (CTEs)
* INNER JOIN
* Window Functions

  * `RANK()`
  * `ROW_NUMBER()`
* `PARTITION BY`

## Learning Outcomes

By completing this project, I learned how to:

* Design simple relational tables from raw data
* Perform business-oriented SQL analysis
* Write efficient SQL queries using CTEs and subqueries
* Apply window functions for ranking and sequencing
* Generate customer sales insights from transactional data

## Project Structure

```text
Customer-Sales-Insights/
│── README.md
│── customer_sales_insights.sql
│── Sample_Superstore.csv
```

## Author

**Saksham Agarwal**
