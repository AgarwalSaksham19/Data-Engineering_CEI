# Week 6 – Spark Architecture and Efficient Data Processing

## 📌 Overview

This assignment focuses on Spark architecture and efficient data processing using PySpark. It covers Spark components, execution modes, lazy evaluation, DAG-based execution, transformations, actions, schema handling, filtering, DataFrame modifications, file formats, performance optimization, and data processing pipelines.

---

## 🎯 Objective

The objective of this assignment is to understand Spark architecture and perform efficient data processing using transformations, filtering, schema handling, and optimized file formats.

The assignment demonstrates:

* Spark architecture and its core components.
* Lazy Evaluation and DAG-based execution.
* Reading data from CSV and Parquet files.
* Filtering and selecting required columns.
* Renaming columns and casting data types.
* Adding calculated columns.
* Understanding transformations and actions.
* Understanding Shuffle and wide transformations.
* Understanding Predicate Pushdown.
* Handling null values efficiently.
* Building read → transform → filter → write pipelines.
* Applying best practices for large datasets.

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
├── Week6_Spark_Questions.ipynb
├── README.md
└── .venv/
```

> **Note:** The `.venv` folder is a local virtual environment and should not be uploaded to GitHub or included in the final submission unless specifically required.

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

Open the notebook in VS Code and select the Python 3.11.9 environment associated with the project virtual environment.

---

## 🚀 Running the Notebook

1. Open the project folder in Visual Studio Code.
2. Open `Week6_Spark_Questions.ipynb`.
3. Select the correct Python 3.11.9 kernel.
4. Start a SparkSession.
5. Execute the notebook cells sequentially.
6. Review the execution results displayed below the code cells.

---

## 🧠 Topics Covered

### Q1: Spark Architecture

Explains the roles of:

* Driver
* Cluster Manager
* Executors

### Q2: Lazy Evaluation

Explains how Spark delays execution until an action is called and optimizes the complete chain of transformations.

### Q3: Reading CSV Files

Demonstrates reading a CSV file with:

* Header support
* Automatic schema inference

### Q4: CSV vs Parquet

Compares row-based CSV storage with columnar Parquet storage and explains the performance benefits of Parquet.

### Q5–Q6: DataFrame Operations

Demonstrates:

* Filtering data.
* Selecting required columns.
* Renaming columns.
* Casting data types.

### Q7: DAG and Fault Tolerance

Explains how Spark uses lineage information to recompute lost partitions when a worker node fails.

### Q8–Q10: Filtering and Data Transformation

Demonstrates:

* Filtering completed orders.
* Applying multiple conditions.
* Adding calculated columns.

### Q11: Transformations and Actions

Explains the difference between lazy transformations and actions that trigger execution.

### Q12: Data Processing Pipeline

Demonstrates the following workflow:

```text
Read Parquet
     ↓
Filter Null Values
     ↓
Write as CSV
```

### Q13: Client Mode vs Cluster Mode

Explains where the Driver runs in different Spark execution modes.

### Q14: Filtering with OR Conditions

Demonstrates filtering records based on multiple alternative conditions.

### Q15: Large Dataset Best Practices

Explains why `show(5)` is safer than `collect()` when working with very large datasets.

---

## 💻 Important PySpark Operations Used

```python
spark.read.csv()
```

```python
spark.read.parquet()
```

```python
filter()
```

```python
select()
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

```python
isNotNull()
```

```python
show()
```

```python
write.csv()
```

---

## ⚡ Performance Concepts

### Lazy Evaluation

Spark delays execution of transformations until an action is called. This allows Spark to optimize the complete execution plan.

### DAG Optimization

Spark creates a Directed Acyclic Graph of transformations and optimizes the execution before running the job.

### Predicate Pushdown

Filters can be pushed closer to the data source, reducing the amount of data read and processed.

### Parquet

Parquet uses columnar storage, which allows Spark to read only the required columns and improves analytical query performance.

### Avoiding `collect()`

The `collect()` function brings all records to the Driver. For very large datasets, this can cause excessive memory usage or an OutOfMemoryError.

Instead, use:

```python
df.show(5)
```

or:

```python
df.limit(5).show()
```

---

## 🔄 Complete Data Processing Workflow

The assignment demonstrates the following general Spark pipeline:

```text
Read Data
    ↓
Apply Transformations
    ↓
Filter Data
    ↓
Select Required Columns
    ↓
Handle Null Values
    ↓
Optimize Processing
    ↓
Write Processed Data
```

---

## 📊 Execution Results

The PySpark code examples are executed in the Jupyter Notebook. The execution results are displayed directly below the corresponding code cells.

These results demonstrate the practical application of Spark transformations, filtering, DataFrame modification, file reading, and data writing operations.

---

## 💡 Final Insights

### Architecture

The Driver coordinates the Spark application, the Cluster Manager allocates resources, and Executors perform the actual data processing on worker nodes.

### Performance

Spark improves performance through Lazy Evaluation, DAG optimization, in-memory processing, Predicate Pushdown, and efficient columnar formats such as Parquet.

### Data Processing

Spark provides a powerful DataFrame API for reading, transforming, filtering, cleaning, and writing large datasets efficiently.

### Best Practices

For large datasets:

* Avoid using `collect()` unnecessarily.
* Use `show()` or `limit()` to inspect data.
* Use Parquet for analytical workloads.
* Filter data as early as possible.
* Use appropriate schemas instead of relying entirely on schema inference.
* Take advantage of Spark's lazy execution and query optimization.

---

## ✅ Conclusion

This assignment provides practical and theoretical knowledge of Apache Spark and PySpark. It demonstrates how Spark's architecture, DAG execution, lazy evaluation, transformations, actions, optimized file formats, and query optimizations enable efficient processing of large datasets.

The assignment also demonstrates a complete data processing workflow from reading data to transforming, filtering, and writing the processed output.

---

## 👨‍💻 Author

**Saksham Agarwal**

B.Tech Computer Science and Engineering
DIT University
