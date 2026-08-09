# E-Commerce Order Analytics System

### Celebal Technologies Summer Internship 2026

---

## 📖 Overview

This project implements an end-to-end **E-Commerce Order Analytics System** using **Python, SQL, and SQLite**.

The system works with realistic but intentionally inconsistent e-commerce data and follows a complete data engineering workflow, from data generation and validation to cleaning, database loading, SQL analysis, reporting, and edge-case testing.

```text
Data Generation
      ↓
Data Verification
      ↓
Data Cleaning
      ↓
SQLite Database
      ↓
SQL Analysis
      ↓
CLI Reporting
      ↓
Edge Case Testing
```

---

## 🎯 Objectives

The main objectives of this project are to:

* Generate realistic e-commerce datasets
* Introduce intentional data-quality issues
* Validate raw datasets
* Clean and transform data using Python
* Maintain referential integrity
* Store cleaned data in a relational SQLite database
* Perform business analytics using SQL
* Use CTEs and window functions for advanced analysis
* Perform customer segmentation
* Perform cohort and retention analysis
* Generate automated CLI reports
* Test and handle important edge cases

---

## 📂 Project Structure

```text
Week-08/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── scripts/
│   ├── generate_data.py
│   ├── verify_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── run_sql.py
│   ├── report_cli.py
│   └── test_edge_cases.py
│
├── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── output/
│   └── data_quality_report.txt
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── sql_analysis/
│   ├── phase5_cli/
│   └── phase6_edge_cases/
│
├── report/
│   ├── README.md
│   └── Celebal_Week_08_ECommerce_Order_Analytics_Report.docx
│
├── ecommerce.db
└── README.md
```

---

## 📊 Dataset

The project uses four main datasets.

### Customers

Contains:

* `customer_id`
* `customer_name`
* `email`
* `registration_date`
* `customer_type`

### Products

Contains:

* `product_id`
* `product_name`
* `category`
* `subcategory`
* `cost_price`

### Orders

Contains:

* `order_id`
* `customer_id`
* `order_date`
* `status`
* `region_code`

### Order Items

Contains:

* `item_id`
* `order_id`
* `product_id`
* `quantity`
* `unit_price`
* `discount_percent`

---

## 📈 Dataset Statistics

### Raw Data

```text
Customers    : 500
Products     : 500
Orders       : 1000
Order Items  : 2000
```

### Cleaned Data

```text
Customers    : 500
Products     : 500
Orders       : 950
Order Items  : 1905
```

---

# 🔹 Project Phases

## Phase 1 — Data Generation

Python was used to generate realistic e-commerce datasets with intentionally introduced data-quality issues.

Examples include:

* Missing customer IDs
* Invalid email addresses
* Negative quantities
* Product name formatting inconsistencies
* Incorrect date formats
* Invalid discount values

The generated datasets were verified before proceeding to the cleaning stage.

---

## Phase 2 — Data Cleaning

The raw datasets were cleaned and transformed using Python and Pandas.

Major operations included:

* Duplicate detection and removal
* Email validation
* Product name normalization
* Date conversion
* Missing customer ID handling
* Referential integrity checks
* Discount validation
* Invalid record handling

---

## Phase 3 — SQLite Database

The cleaned datasets were loaded into a SQLite database:

```text
ecommerce.db
```

The database contains the following tables:

```text
customers
products
orders
order_items
```

Foreign-key relationships were established between the tables, and referential integrity was validated successfully.

---

## Phase 4 — SQL Analysis

The project contains **16 SQL analytical questions** covering different business and analytical scenarios.

### Analysis Areas

* Revenue analysis
* Customer analysis
* Monthly order analysis
* Return analysis
* Running totals
* Ranking
* Previous-period comparison
* Customer segmentation
* Customer lifetime value
* Year-over-year comparison
* First and last category analysis
* Cumulative revenue
* Cohort retention analysis
* Self-join analysis

### SQL Concepts Used

* JOINs
* Aggregations
* CTEs
* Subqueries
* Window Functions
* `RANK()`
* `DENSE_RANK()`
* `LAG()`
* `NTILE()`
* `SUM() OVER()`
* Cohort Analysis

---

## Phase 5 — CLI Reporting

A Python-based CLI reporting tool was developed to generate periodic e-commerce analytics reports.

The tool supports:

* Daily reports
* Weekly reports
* Monthly reports

### Reports Include

* Total orders
* Total revenue
* Unique customers
* Top 3 products
* Previous-period comparison
* Percentage changes

This provides a simple way to analyze business performance directly from the command line.

---

## Phase 6 — Edge Case Testing

The system was tested against several invalid and boundary conditions.

| Test              |  Result  |
| ----------------- | :------: |
| Invalid Order ID  | ✅ Passed |
| Discount > 100%   | ✅ Passed |
| Zero Quantity     | ✅ Passed |
| Future Order Date | ✅ Passed |

These tests help ensure that the system handles invalid input and unusual scenarios correctly.

---

# 🛠️ Technologies Used

* **Python**
* **SQL**
* **SQLite**
* **Pandas**
* **Faker**
* **Git**
* **GitHub**
* **Visual Studio Code**

---

# ▶️ How to Run

Run all commands from the `Week-08` project directory.

### 1. Generate Data

```bash
python scripts/generate_data.py
```

### 2. Verify Data

```bash
python scripts/verify_data.py
```

### 3. Clean Data

```bash
python scripts/clean_data.py
```

### 4. Create Database

```bash
python scripts/load_database.py
```

### 5. Run SQL Analysis

```bash
python scripts/run_sql.py
```

### 6. Run CLI Reports

```bash
python scripts/report_cli.py
```

### 7. Run Edge Case Tests

```bash
python scripts/test_edge_cases.py
```

---

# 📸 Screenshots

Execution screenshots are available in the:

```text
screenshots/
```

directory.

The screenshots demonstrate:

* Data generation
* Data verification
* Data cleaning
* Database creation
* SQL analysis
* CLI reporting
* Edge-case testing

---

# 🎯 Key Outcomes

This project demonstrates practical experience in:

* Data generation
* Data quality management
* Data cleaning and transformation
* Data validation
* Relational database design
* SQL analytics
* Advanced SQL
* Window functions
* Common Table Expressions (CTEs)
* Cohort analysis
* Customer segmentation
* Python automation
* CLI-based reporting
* Edge-case testing

---

# 👨‍💻 Author

**Saksham Agarwal**

Computer Science Engineering Student

### Areas of Interest

* Data Engineering
* Software Development
* Cloud Technologies
* Artificial Intelligence

---

## ⭐ Acknowledgement

Developed as part of the **Celebal Technologies Summer Internship 2026**.
