# Python Data Exploration and Cleaning using Pandas

## Overview

This project demonstrates the fundamentals of **Python-based data analysis and data cleaning using Pandas**.

The project loads a CSV dataset into a Pandas DataFrame, explores its structure, identifies and handles missing values, performs basic filtering and column selection, removes duplicate records, creates a derived `total_amount` column, and exports the cleaned dataset as a new CSV file.

---

## Objective

Learn Python basics and perform basic **data exploration and cleaning using Pandas**.

---

## Tasks Performed

1. Load a CSV dataset into a Pandas DataFrame.
2. Explore the dataset using:

   * `head()`
   * `tail()`
   * `shape`
   * `columns`
   * `dtypes`
3. Identify and handle missing values.
4. Perform basic data operations:

   * Filter rows
   * Select columns
5. Remove duplicate records.
6. Create a derived column:

   ```text
   total_amount = price × quantity
   ```
7. Save the cleaned dataset as a new CSV file.
8. Summarize the data-cleaning process and results.

---

## Technologies Used

* **Python**
* **Pandas**
* **Jupyter Notebook**

---

## Dataset

The project uses a CSV dataset containing basic product/order information.

The important columns include:

| Column         | Description                 |
| -------------- | --------------------------- |
| `product`      | Name of the product         |
| `price`        | Price of the product        |
| `quantity`     | Quantity purchased          |
| `total_amount` | Calculated price × quantity |

The dataset is intentionally explored and cleaned during the notebook workflow.

---

## Project Workflow

```text
CSV Dataset
     │
     ▼
Load using Pandas
     │
     ▼
Explore Dataset
     │
     ├── Head / Tail
     ├── Shape
     ├── Columns
     └── Data Types
     │
     ▼
Identify Missing Values
     │
     ▼
Handle Missing Values
     │
     ▼
Filter & Select Data
     │
     ▼
Remove Duplicates
     │
     ▼
Create total_amount
     │
     ▼
Export Cleaned CSV
```

---

# Data Exploration

The notebook examines the dataset using basic Pandas operations.

### View first records

```python
df.head()
```

### View last records

```python
df.tail()
```

### Check dataset dimensions

```python
df.shape
```

### View column names

```python
df.columns
```

### Check data types

```python
df.dtypes
```

These operations provide an initial understanding of the dataset before cleaning.

---

# Handling Missing Values

Missing values are identified using:

```python
df.isnull().sum()
```

Depending on the column and its purpose, missing values are handled by either:

* Filling them with an appropriate value
* Dropping rows where necessary

The notebook documents the approach used for each relevant column.

---

# Basic Data Operations

### Selecting columns

```python
df[["product", "price", "quantity"]]
```

### Filtering rows

Rows can be filtered based on conditions such as price or quantity.

Example:

```python
df[df["price"] > 500]
```

These operations demonstrate basic DataFrame manipulation using Pandas.

---

# Removing Duplicates

Duplicate records are identified and removed using:

```python
df.drop_duplicates()
```

This helps ensure that the cleaned dataset does not contain repeated records.

---

# Creating a Derived Column

A new `total_amount` column is created using:

```python
df["total_amount"] = df["price"] * df["quantity"]
```

This calculates the total value of each order.

Example:

| price | quantity | total_amount |
| ----: | -------: | -----------: |
|   500 |        2 |         1000 |
|   250 |        4 |         1000 |
|   750 |        1 |          750 |

---

# Output

The project produces the following outputs:

```text
Python-Pandas-Data-Cleaning/
│
├── README.md
├── data/
│   ├── input.csv
│   └── cleaned_data.csv
│
└── notebook/
    └── data_exploration_cleaning.ipynb
```

### Generated Files

**Jupyter Notebook**

```text
data_exploration_cleaning.ipynb
```

Contains the complete exploration and cleaning workflow.

**Cleaned CSV**

```text
cleaned_data.csv
```

Contains the final cleaned dataset with the derived `total_amount` column.

---

# Brief Summary

The dataset was successfully loaded into Pandas and explored using basic DataFrame operations. Missing values were identified and handled, required columns were selected, records were filtered, and duplicate rows were removed.

A new `total_amount` column was created using:

```text
price × quantity
```

The cleaned dataset was then exported as a new CSV file for further analysis or use in downstream applications.

---

# Learning Outcomes

Through this project, I gained practical experience with:

* Python fundamentals
* Pandas DataFrames
* Loading CSV files
* Data exploration
* Missing-value handling
* Data filtering
* Column selection
* Duplicate removal
* Creating derived columns
* Exporting cleaned datasets
* Jupyter Notebook

---

# Author

**Saksham Agarwal**

B.Tech CSE (AI & ML)
DIT University
