# Azure Data Engineering Pipeline using Azure Data Factory

## Overview

This project demonstrates the creation of a simple end-to-end data pipeline on Microsoft Azure using **Azure Blob Storage** and **Azure Data Factory (ADF)**. The pipeline reads a CSV file from Azure Blob Storage, validates its metadata, and copies it to a new destination file within the storage account.

This project was completed as part of the **Celebal Technologies Data Engineering Internship – Week 3 Assignment**.

---

## Objectives

- Understand Azure cloud fundamentals.
- Create and configure Azure Storage Account.
- Store data in Azure Blob Storage.
- Create and configure Azure Data Factory.
- Build a data pipeline using Copy Data activity.
- Validate source file using Get Metadata activity.
- Execute and monitor the pipeline successfully.

---

## Technologies Used

- Microsoft Azure
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Azure IAM (Identity and Access Management)

---

## Project Architecture

```text
                Sample Superstore.csv
                        │
                        ▼
              Azure Blob Storage
                        │
                        ▼
               Azure Data Factory
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
   Get Metadata Activity         Copy Data Activity
         │                             │
         └──────────────┬──────────────┘
                        ▼
                Output.csv (Destination)
```

---

## Project Workflow

### Step 1: Resource Group

Created an Azure Resource Group to organize all project resources.

---

### Step 2: Storage Account

Created an Azure Storage Account and Blob Container.

Uploaded:

- `Sample Superstore.csv`

---

### Step 3: Azure Data Factory

Created an Azure Data Factory instance and explored:

- Author
- Monitor
- Manage

---

### Step 4: Linked Service

Created a Linked Service connecting Azure Data Factory to Azure Blob Storage using Azure Subscription authentication.

---

### Step 5: Datasets

Created two datasets:

#### Source Dataset

- Azure Blob Storage
- Delimited Text
- File:
  - `Sample Superstore.csv`

#### Destination Dataset

- Azure Blob Storage
- Delimited Text
- File:
  - `Output.csv`

---

### Step 6: Get Metadata Activity

Configured the Get Metadata activity to validate the source file before copying.

Metadata fields selected:

- Exists
- Size
- Last Modified

---

### Step 7: Copy Data Pipeline

Created a pipeline consisting of:

```
Get Metadata
      │
      ▼
   Copy Data
```

The pipeline copies data from:

```
Sample Superstore.csv
```

to

```
Output.csv
```

---

### Step 8: Pipeline Execution

Executed the pipeline using **Debug**.

Pipeline Status:

```
Succeeded
```

The destination file was successfully created inside Azure Blob Storage.

---

### Step 9: IAM Configuration

Assigned the following roles:

- Reader
- Contributor
- Storage Blob Data Contributor

to allow Azure Data Factory to access Azure Blob Storage.

---

## Folder Structure

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

## Results

- Successfully created Azure Resource Group.
- Successfully configured Azure Storage Account.
- Uploaded dataset to Azure Blob Storage.
- Connected Azure Data Factory with Blob Storage.
- Created Source and Destination datasets.
- Validated metadata using Get Metadata activity.
- Copied data using Copy Data activity.
- Executed the pipeline successfully.
- Verified the copied output file.
- Configured IAM roles for secure access.

---

## Learning Outcomes

Through this project, I gained practical experience with:

- Azure Cloud Services
- Azure Resource Management
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory
- Linked Services
- Datasets
- Get Metadata Activity
- Copy Data Activity
- Pipeline Development
- Pipeline Monitoring
- Azure IAM Role Assignments

---

## Future Enhancements

- Automate pipeline execution using Triggers.
- Process multiple files using ForEach activity.
- Load data into Azure SQL Database or Azure Synapse Analytics.
- Integrate Data Flow transformations.
- Implement monitoring and alerting for pipeline failures.

---

## Author

**Saksham Agarwal**

**B.Tech CSE (AI & ML)**  
DIT University

**Celebal Technologies – Data Engineering Internship**
