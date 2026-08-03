# Week 7 - Delta Lake MERGE Implementation

## Celebal Technologies Data Engineering Internship

### Overview

This assignment demonstrates incremental data processing using Delta Lake. The objective was to load a customer dataset into a Delta table, clean the data, process an incremental dataset, and perform UPSERT operations using the Delta Lake MERGE command.

---

## Assignment Objectives

- Load customer data into a Delta table.
- Handle missing values and remove duplicate records.
- Load an incremental customer dataset.
- Perform MERGE operation to update existing records and insert new records.
- Validate the final dataset.
- Display the final merged dataset and schema.

---

## Project Structure

```
Week-07/
│
├── data/
│   ├── customer_master.csv
│   ├── customer_incremental.csv
│   └── README.md
│
├── notebooks/
│   ├── Delta_Lake_MERGE_Assignment.ipynb
│   └── README.md
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── merge_operation/
│   ├── validation/
│   ├── final_output/
│   └── README.md
│
├── report/
│   └── README.md
│
└── README.md
```

---

## Technologies Used

- Python
- Apache Spark (PySpark)
- Delta Lake
- Google Colab
- Pandas

---

## Assignment Workflow

1. Load Customer Dataset
2. Create Delta Table
3. Data Cleaning
4. Load Incremental Dataset
5. Delta MERGE (UPSERT)
6. Validate Results
7. Display Final Dataset

---

## Output Summary

- Customer dataset loaded successfully.
- Null values removed.
- Duplicate records removed.
- Incremental records processed.
- MERGE operation completed successfully.
- Final dataset validated.
- Duplicate Customer IDs: 0.

---

## Author

**Saksham Agarwal**

Data Engineering Intern

Celebal Technologies Summer Internship 2026
