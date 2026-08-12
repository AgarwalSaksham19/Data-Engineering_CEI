# Azure Data Engineering Pipeline using Azure Data Factory

## Overview

This project demonstrates a simple end-to-end data engineering pipeline on **Microsoft Azure** using **Azure Blob Storage** and **Azure Data Factory (ADF)**.

The pipeline reads a CSV file from Azure Blob Storage, validates the source file using **Get Metadata**, and copies the data to a destination file within the storage account using **Copy Data**.

This project was completed as part of the **Celebal Technologies Data Engineering Internship – Week 3 Assignment**.

---

## Objectives

* Understand Azure cloud fundamentals.
* Create and configure an Azure Storage Account.
* Store and manage data using Azure Blob Storage.
* Create and configure Azure Data Factory.
* Configure Linked Services and Datasets.
* Build a data pipeline using Copy Data activity.
* Validate source file metadata using Get Metadata activity.
* Execute, monitor, and verify a successful pipeline run.
* Understand Azure role-based access control (RBAC).

---

## Technologies Used

* **Microsoft Azure**
* **Azure Storage Account**
* **Azure Blob Storage**
* **Azure Data Factory (ADF)**
* **Azure RBAC / IAM**
* **CSV / Delimited Text**

---

## Project Architecture

```text
                  Sample Superstore.csv
                           │
                           ▼
                 ┌──────────────────┐
                 │ Azure Blob       │
                 │ Storage          │
                 │ Source Container │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Azure Data       │
                 │ Factory          │
                 └────────┬─────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
          Get Metadata         Copy Data
             Activity           Activity
                 │                 │
                 │                 ▼
                 │        ┌──────────────────┐
                 └───────►│ Azure Blob       │
                          │ Storage          │
                          │ Output.csv      │
                          └──────────────────┘
```

---

# Project Workflow

## Step 1 — Resource Group

Created an **Azure Resource Group** to organize and manage all resources used in the project.

---

## Step 2 — Storage Account

Created an **Azure Storage Account** and configured a Blob Storage container.

Uploaded the source dataset:

```text
Sample Superstore.csv
```

The CSV file serves as the source data for the pipeline.

---

## Step 3 — Azure Data Factory

Created an **Azure Data Factory** instance.

The ADF interface was used to work with:

* **Author** — Create and configure pipelines
* **Monitor** — Track pipeline executions
* **Manage** — Configure connections and services

---

## Step 4 — Linked Service

Created an Azure Data Factory **Linked Service** to establish a connection between ADF and Azure Blob Storage.

The connection was configured using Azure subscription-based authentication.

---

## Step 5 — Datasets

Created two datasets representing the source and destination files.

### Source Dataset

* Storage: Azure Blob Storage
* Format: Delimited Text
* File: `Sample Superstore.csv`

### Destination Dataset

* Storage: Azure Blob Storage
* Format: Delimited Text
* File: `Output.csv`

---

## Step 6 — Get Metadata Activity

Configured the **Get Metadata** activity to validate the source file before the copy operation.

The following metadata properties were selected:

* `Exists`
* `Size`
* `Last Modified`

This provides a basic validation step before transferring the data.

---

## Step 7 — Copy Data Pipeline

Created an ADF pipeline containing the following activities:

```text
Get Metadata
      │
      ▼
Copy Data
```

The Copy Data activity transfers:

```text
Sample Superstore.csv
          ↓
      Output.csv
```

within Azure Blob Storage.

---

## Step 8 — Pipeline Execution

The pipeline was executed using **Debug** in Azure Data Factory.

Pipeline status:

```text
Succeeded
```

The destination file was successfully created in Azure Blob Storage.

---

## Step 9 — IAM / RBAC Configuration

Azure role-based access control was configured to provide the required permissions for accessing Azure resources and Blob Storage.

Roles used during the project included:

* **Reader**
* **Contributor**
* **Storage Blob Data Contributor**

These permissions enabled the required resource management and Blob Storage operations.

> For a production implementation, permissions should follow the principle of least privilege rather than granting broader roles than necessary.

---

# Folder Structure

```text
Azure-ADF-Pipeline/
│
├── README.md
├── Sample Superstore.csv
│
├── Screenshots/
│   ├── ResourceGroup.png
│   ├── StorageAccount.png
│   ├── BlobContainer.png
│   ├── LinkedService.png
│   ├── SourceDataset.png
│   ├── DestinationDataset.png
│   ├── GetMetadata.png
│   ├── PipelineDesign.png
│   ├── PipelineSucceeded.png
│   └── IAMRoles.png
│
└── Output/
    └── Output.csv
```

---

# Results

The pipeline was successfully completed and verified.

* Created an Azure Resource Group.
* Created and configured an Azure Storage Account.
* Created an Azure Blob Storage container.
* Uploaded `Sample Superstore.csv`.
* Created an Azure Data Factory instance.
* Configured a Blob Storage Linked Service.
* Created source and destination datasets.
* Configured Get Metadata activity.
* Configured Copy Data activity.
* Executed the pipeline successfully.
* Generated `Output.csv`.
* Verified the copied data in Azure Blob Storage.
* Configured the required Azure RBAC permissions.

---

# Learning Outcomes

This project provided hands-on experience with:

* Azure Cloud Services
* Azure Resource Management
* Azure Storage Accounts
* Azure Blob Storage
* Azure Data Factory
* Linked Services
* Datasets
* Get Metadata Activity
* Copy Data Activity
* Pipeline Development
* Pipeline Debugging
* Pipeline Monitoring
* Azure RBAC / IAM

---

# Future Enhancements

The pipeline can be extended with:

* **Triggers** for automated execution.
* **ForEach activity** for processing multiple files.
* **Azure SQL Database** or **Azure Synapse Analytics** as a destination.
* **Mapping Data Flows** for data transformations.
* **Parameterized datasets and pipelines** for reusable workflows.
* **Monitoring and alerting** for pipeline failures.
* **Incremental data loading** for larger datasets.

---

# Author

**Saksham Agarwal**

B.Tech CSE (AI & ML)
DIT University

**Data Engineering Intern — Celebal Technologies**
