# Week 5 – Apache Spark and PySpark

## 📌 Overview

This assignment focuses on Apache Spark and PySpark DataFrame operations. It covers the limitations of traditional MapReduce, Spark's in-memory computing capabilities, data cleaning, handling null values, filtering, grouping, aggregation, data type casting, and shuffle operations.

---

## 🎯 Objectives

The main objectives of this assignment are:

* Understand the limitations of traditional MapReduce.
* Learn how Spark uses in-memory computing.
* Perform data cleaning using PySpark DataFrames.
* Remove duplicate records.
* Handle null values.
* Filter and group data.
* Perform aggregations using functions such as `sum()`, `avg()`, `min()`, and `max()`.
* Understand DataFrame immutability.
* Understand Spark Shuffle and wide transformations.
* Cast and rename columns.

---

## 🛠️ Technologies Used

* **Python 3.11.9**
* **Apache Spark**
* **PySpark**
* **Jupyter Notebook**
* **Visual Studio Code**

---

## 📂 Project Structure

```text
Week5_Spark_Questions/
│
├── Week5_Spark.ipynb
├── README.md
└── .venv/
```

> **Note:** The `.venv` folder is a local virtual environment and should generally not be uploaded to GitHub. Add it to `.gitignore` if required.

---

## ⚙️ Setup and Installation

### 1. Create a Virtual Environment

```bash
py -3.11 -m venv .venv
```

### 2. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Required Packages

```bash
python -m pip install pyspark ipykernel
```

### 4. Select the Jupyter Kernel

Open the `.ipynb` file in VS Code and select the Python kernel associated with the project's virtual environment.

---

## 🚀 Running the Project

1. Open the project folder in VS Code.
2. Open `Week5_Spark.ipynb`.
3. Select the correct Python 3.11 kernel.
4. Run the SparkSession initialization cell.
5. Execute the assignment cells sequentially from Q1 to Q15.

---

## 🧪 Topics Covered

### Q1–Q2: Spark Fundamentals

* Limitations of traditional MapReduce.
* In-memory computing in Apache Spark.

### Q3–Q8: DataFrame Operations

* Removing duplicate rows.
* Filtering records.
* Grouping data.
* Counting records.
* Handling DataFrame immutability.
* Applying multiple filter conditions.

### Q9–Q15: Data Cleaning and Aggregation

* Handling null values.
* Casting and renaming columns.
* Understanding Shuffle operations.
* Removing invalid records.
* Multiple aggregations using `.agg()`.
* Schema inference risks.
* Building a complete data processing pipeline.

---

## 📊 Main PySpark Operations Used

The assignment demonstrates the following PySpark operations:

```python
dropDuplicates()
```

```python
filter()
```

```python
groupBy()
```

```python
agg()
```

```python
na.drop()
```

```python
na.fill()
```

```python
withColumn()
```

```python
withColumnRenamed()
```

```python
cast()
```

---

## 📈 Final Processing Pipeline

The final pipeline demonstrates a complete data processing workflow:

```text
Raw Data
   ↓
Remove Duplicate Records
   ↓
Fill Null Prices with 0
   ↓
Group Data by Store
   ↓
Calculate Total Revenue
```

Example:

```python
result = (
    df_store
    .dropDuplicates()
    .na.fill({"price": 0})
    .groupBy("store_id")
    .agg(
        sum("price").alias("total_revenue")
    )
)
```

---

## ✅ Conclusion

This assignment provides practical experience with Apache Spark and PySpark DataFrames. It demonstrates how Spark can efficiently process large datasets while providing powerful tools for data cleaning, transformation, filtering, grouping, and aggregation.

The assignment also highlights important Spark concepts such as **immutability**, **in-memory computing**, **wide transformations**, and **Shuffle operations**.

---

## 👨‍💻 Author

**Saksham Agarwal**

B.Tech Computer Science and Engineering
DIT University
