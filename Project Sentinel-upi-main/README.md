# Project Sentinel — Real-Time UPI Transaction & Fraud Detection Pipeline

An end-to-end **UPI transaction analytics and fraud-detection pipeline** built using **PySpark, Delta Lake, Structured Streaming, and Medallion Architecture**.

Project Sentinel processes intentionally messy payment telemetry, preserves raw events, repairs structural defects, quarantines invalid records, detects behavioral anomalies, and produces explainable fraud alerts and business KPIs.

**Stack** — PySpark 3.5 · Delta Lake 3.2 · Structured Streaming · Databricks Runtime 15.4 LTS / Unity Catalog

Runs end to end on a laptop with no cloud account. The same code can be deployed to Databricks by changing one configuration file.

---

## The Problem

Payment telemetry arrives broken in two different ways, and they need two different answers.

### Structurally

Amounts arrive as `842.50` from one client version and `"842.50"` from another. Timestamps come as ISO-8601, epoch milliseconds, and `09-08-2026 19:47:09` with no timezone at all.

Fields can be null, padded with whitespace, or inconsistently cased. Some lines are truncated mid-JSON. A retry storm can resend the same transaction under the same ID.

These are defects of **form**.

The answer is to repair what can be repaired and quarantine the rest with an explicit reason.

### Logically

Every field can be well-formed and the transaction can still be suspicious:

* An account draining itself within five minutes
* One IP serving dozens of unrelated payers
* A large transaction occurring at 3 AM
* One payer sending transactions to many different payees within a short window

These are defects of **behaviour**.

The answer is to score them using transparent, explainable fraud rules.

Project Sentinel handles both categories and measures whether the pipeline worked.

---

# Results

One configured demonstration run completed end-to-end on a laptop in approximately **31 seconds**.

> The exact figures can vary slightly because the simulation window is anchored to the current time. Use a fixed `--seed` and `--end` when reproducible results are required.

| Metric                             |  Result |
| ---------------------------------- | ------: |
| Raw JSON lines generated           | 207,464 |
| Landed and structured without loss | 207,464 |
| Cleansed into Silver               | 199,629 |
| Quarantined with a reason          |   4,924 |
| Deduplicated retry storms          |   2,911 |
| Transactions scored                | 199,629 |
| Fraud alerts raised (HIGH)         |   3,108 |

### Detection Performance

Detection is measured against anomalies intentionally planted by the generator. **The labels are never provided to the pipeline during processing.**

| Injected anomaly | Planted | Never scored | Alerted (HIGH) | Flagged (HIGH+MEDIUM) |  Recall* |
| ---------------- | ------: | -----------: | -------------: | --------------------: | -------: |
| `high_amount`    |     800 |           20 |            780 |                   780 | **1.00** |
| `velocity`       |   1,255 |           25 |            632 |                 1,230 | **1.00** |
| `fanout`         |   1,744 |           43 |          1,107 |                 1,701 | **1.00** |
| `odd_hour`       |     600 |           11 |            589 |                   589 | **1.00** |

*Recall is measured over anomalies that reached Gold: `Planted - Never scored`.

**HIGH-band alert precision:** 3,108 / 3,108 = **100%** against the injected anomaly labels.

Two important caveats:

* Recall is measured only over rows that reached Gold. Anomalies quarantined for structural defects or removed as duplicates are reported separately as **Never scored**.
* Every injected anomaly comes from the suspicious-IP pool, so `shared_ip` contributes to all four anomaly types. This makes flagged recall less demanding than HIGH-band alerting.

### Business Results

Across the same run:

* **₹30.84 crore** successful transaction volume across 7 days
* **199,629** transactions
* **88.2%** success rate
* **₹1,751** average transaction value
* Approximately **10,100** daily active payers
* KPIs available by bank, application, and city
* `IDFC` leads transaction volume at approximately **₹3.99 Cr**

```text
119 tests passing · ruff clean · mypy clean · TypeScript clean
```

---

# Architecture

```text
                  Simulated UPI Telemetry
                           │
                           ▼
                    ┌─────────────┐
                    │   Landing   │
                    │ Raw JSON    │
                    │ No parsing  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Bronze    │
                    │ Structured  │
                    │ All strings │
                    └──────┬──────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
           ┌───────────┐      ┌─────────────┐
           │  Silver   │      │ Quarantine  │
           │ Clean     │      │ Bad records │
           │ Mask      │      │ + reasons   │
           │ Dedup     │      └─────────────┘
           └─────┬─────┘
                 │
                 ▼
           ┌─────────────┐
           │    Gold     │
           │ KPIs + Risk │
           │   Scoring   │
           └──────┬──────┘
                  │
                  ▼
          ┌───────────────┐
          │ Web Export    │
          │ Aggregated    │
          │ JSON          │
          └───────┬───────┘
                  │
                  ▼
          React + Vite Dashboard
```

---

# Step 1 — Landing: Bytes, and Nothing Else

The specification requires raw data to be landed **without applying transformations**.

The reader therefore uses `text`, allowing each JSON line to arrive as one opaque string.

Parsing a line into columns is itself a transformation. Doing this before durable storage could allow malformed records to fail or disappear before they are ever recorded.

Landing stores only:

* Raw payload
* Source file
* Arrival timestamp

Nothing else.

---

# Step 2 — Bronze: Structure Without Cleaning

Every payload field becomes its own column, but **every field remains a string**.

For example:

```text
"842.50"
842.50
"-91.2"
```

all survive exactly as received.

This prevents schema inference from silently deciding which representation is correct.

Typing happens once in Silver, where failed casts become explicit quarantine reasons instead of unnoticed nulls.

Malformed JSON is preserved through `_corrupt_record`, allowing the pipeline to distinguish:

* Invalid JSON
* Valid JSON with missing fields
* Valid JSON with invalid values

---

# Step 3 — Silver: Repair, Mask, Quarantine

Silver performs the main data-quality operations.

### Standardisation

```text
" Success " → SUCCESS
" completed " → COMPLETED
"  user@upi " → user@upi
```

Whitespace is removed and categorical fields are normalised.

### Type Resolution

Amounts and timestamps are converted to their expected types.

Timestamps are routed **by shape** before parsing:

* ISO-8601
* Epoch seconds
* Epoch milliseconds
* `dd-MM-yyyy HH:mm:ss`

This prevents non-ISO dates from being incorrectly interpreted.

### Privacy Masking

VPAs are partially masked while retaining the bank handle for analytics:

```text
us1234567890@oksbi
        ↓
us***@oksbi
```

Phone numbers retain only four digits.

Device IDs and IP addresses are converted into **salted SHA-256 digests**.

The hashes remain stable, allowing Gold to perform behavioural analysis without exposing the original identifiers.

### Quarantine

Invalid rows are written to:

```text
quarantine.upi_rejects
```

with the **reason and original payload attached**.

Example reasons:

| Reason                   | Count |
| ------------------------ | ----: |
| `non_positive_amount`    | 2,853 |
| `missing_transaction_id` |   522 |
| `missing_event_time`     |   574 |
| `malformed_json`         |   413 |
| `missing_amount`         |   562 |

"Filter out" and "throw away" are different instructions. A pipeline that cannot explain what it discarded cannot be trusted about what it kept.

### Deduplication

Retry storms are collapsed using:

```text
dropDuplicatesWithinWatermark
```

on `transaction_id`, bounded by a **2-hour watermark** so streaming state remains finite.

---

# Step 4 — Gold: KPIs and Explainable Fraud Scoring

Gold deliberately runs as a **batch recomputation** over Silver.

Everything here is either a full aggregation or a windowed comparison against neighbouring transactions. Keeping Gold batch-based avoids unnecessary streaming-state complexity while remaining exact and fast at this scale.

---

## Fraud Scoring

Scoring is additive.

Every rule that fires adds its weight and appends its name to the `reasons` field.

| Rule          | Fires when                                   | Weight |
| ------------- | -------------------------------------------- | -----: |
| `high_amount` | Above a robust amount threshold              |     30 |
| `shared_ip`   | ≥5 distinct payers behind one IP             |     25 |
| `velocity`    | >10 transactions from one payer in 5 min     |     25 |
| `fanout`      | >15 distinct payees from one payer in 60 min |     25 |
| `odd_hour`    | 00:00–05:00 IST                              |     10 |

### Design Constraint

**No single rule can reach the HIGH band (50).**

A large payment alone is not fraud. A payment at 3 AM alone is not fraud. A shared IP alone may simply be a public network.

Multiple independent signals create a stronger alert.

Example:

```text
TXN000000201164  2026-08-05 01:48  ₹8,453  us***@okidfc

Score: 85

Reasons:
[shared_ip, velocity, fanout, odd_hour]
```

---

# The Threshold Bug Worth Knowing About

`high_amount` originally used the **99.5th percentile** of successful transaction amounts.

This looked reasonable but failed because the injected anomalies themselves represented approximately 0.7% of traffic.

The 99.5th percentile therefore landed inside the anomaly population:

```text
Measured threshold: ₹103,899
Injected anomalies: starting around ₹60,000
```

The detector was consequently excluding many of the transactions it was intended to detect.

### The Fix

The threshold was changed to a robust Tukey fence:

```text
Q3 + 3 × IQR
```

with a domain-aware floor of:

```text
₹50,000
```

The quartiles are calculated from the dense middle of the distribution, making the threshold less sensitive to a small population of extreme values.

This change:

```text
27 alerts → 80 alerts
```

and improved:

```text
high_amount recall: 0.87 → 1.00
```

The important result is not just the improved metric — the pipeline **exposed a weakness in its own detection methodology and the threshold was redesigned accordingly**.

---

# Why "Real-Time"?

Every ingestion stage is a Structured Streaming query with a checkpoint and:

```text
Trigger.AvailableNow
```

This provides incremental processing while still allowing the pipeline to terminate after processing the currently available data.

The behaviour is:

```text
New files
   ↓
Streaming query
   ↓
Checkpoint
   ↓
Process available data
   ↓
Stop
```

Re-running with no new data is a verified no-op.

Adding another batch causes only the new data to flow through the pipeline.

This provides a practical **incremental streaming architecture** for local execution and testing while allowing the same ingestion design to be moved to a continuously running deployment.

---

# Data Generation

No external dataset is supplied because the specification explicitly requires generated data.

The generator plants known quantities of structural defects and behavioural anomalies.

Example planted defects:

| Defect             |  Count |
| ------------------ | -----: |
| `amount_as_string` | 14,417 |
| `whitespace`       | 10,428 |
| `duplicate`        |  3,065 |
| `case_noise`       | 16,672 |
| `null_optional`    |  8,287 |
| `negative_amount`  |  2,039 |
| Timestamp variants | 12,627 |
| `null_required`    |  1,660 |
| `malformed_json`   |    413 |

The generator's tests assert these quantities so downstream layers are never accidentally tested against zero defects.

### Ground-Truth Labels

Anomaly labels are written to a **separate truth file beside the generated data**.

They are never included in the transaction payload.

This prevents data leakage and keeps the detection evaluation meaningful.

---

# Running It

### Linux / macOS

```bash
./run.sh
```

### Windows

```powershell
.\run.ps1
```

The complete workflow is:

```text
Setup
  ↓
Generate
  ↓
Landing
  ↓
Bronze
  ↓
Silver
  ↓
Gold
  ↓
Report
  ↓
Web Export
  ↓
Dashboard
```

### Options

```bash
./run.sh --fresh
```

Wipe and regenerate first.

```bash
./run.sh --serve-only
```

Skip the pipeline and serve the existing export.

```bash
./run.sh --scale 0.1
```

Run a smaller dataset.

```bash
./run.sh --build
```

Build the production dashboard instead of using the development server.

```bash
./run.sh --no-serve
```

Run the pipeline and export without starting the dashboard.

On Windows, the equivalent PowerShell switches are:

```powershell
-Fresh
-ServeOnly
-Scale 0.1
-Build
-NoServe
```

---

# Individual Commands

```bash
make setup
```

Creates the Python environment and project-local JDK 17.

```bash
make doctor
```

Verifies that Spark and Delta can start correctly.

```bash
make demo
```

Runs:

```text
generate → landing → bronze → silver → gold → report
```

Smaller dataset:

```bash
make gen SCALE=0.05
```

Individual stages:

```bash
make run-landing
make run-bronze
make run-silver
make run-gold
```

Run the complete local pipeline:

```bash
make run-local
```

Generate the report:

```bash
make report
```

Run the full quality suite:

```bash
make check
```

---

# Dashboard

`./run.sh` starts the dashboard.

The dashboard is a single scrolling interface containing:

### Overview

* Transaction volume
* Throughput
* Risk bands
* Fraud alerts

### Medallion Funnel

Shows rows moving through each layer, with quarantine and deduplication represented as separate branches.

### Business

Daily transaction volume and flagged share, with KPIs by:

* Bank
* Application
* City

### Scoring

Shows:

* Score distribution
* Risk-band cutoffs
* Rule frequency
* Rule combinations
* Risk-band composition

### Threshold Finding

Compares:

* 99.5th percentile
* Tukey fence

using the same data that produced the pipeline results.

### Detection

Shows:

* Injected anomalies
* Never-scored anomalies
* HIGH alerts
* HIGH + MEDIUM flags
* Recall

### Alert Console

Every HIGH-band transaction is:

* Filterable by rule
* Filterable by bank
* Searchable
* Sortable
* Expandable to show score arithmetic

---

# How the Dashboard Is Fed

There is deliberately **no API service**.

```text
Gold Tables
     ↓
sentinel-web-export
     ↓
Aggregated JSON
     ↓
public/data
     ↓
React + Vite
```

The browser receives only aggregated and masked data.

There are no:

* Database credentials in the browser
* API services
* Backend servers
* Raw identifiers exposed to the frontend

The dashboard can therefore be hosted as a static site.

---

# Keeping the Dashboard Honest

`tests/spark/test_web_export.py` validates dashboard output against the Gold tables.

Tests verify that:

* The funnel accounts for every row that leaves each layer
* Daily KPIs reconcile with headline metrics
* Detection results match the report
* Exported values match Gold
* Masking is preserved

The generated frontend output is also checked for:

* Unmasked VPAs
* Phone numbers
* Dotted IP addresses
* Device IDs

This prevents a masking regression from publishing sensitive identifiers to the static dashboard.

---

# Project Structure

```text
run.sh
run.ps1

conf/
├── base.yaml
└── databricks.yaml

src/sentinel/
├── config.py
├── tables.py
├── spark.py
├── schemas.py
├── landing.py
├── bronze.py
├── silver.py
├── gold.py
├── report.py
│
├── generate/
│
└── web/
    └── export.py

notebooks/
├── landing
├── bronze
├── silver
└── gold

databricks/
├── job definitions
├── deployment scripts
└── deployment guide

dashboards/web/
├── React
├── TypeScript
├── Vite
└── SVG visualisations

tests/
├── unit/
└── spark/
```

Transformation logic lives in the package rather than the notebooks.

The notebooks are thin Databricks shims that call the same functions covered by the local test suite.

This prevents notebook implementations from drifting away from the tested pipeline.

---

# Databricks

`conf/databricks.yaml` maps the same logical zones onto Unity Catalog:

```text
sentinel.landing.*
sentinel.bronze.*
sentinel.silver.*
sentinel.gold.*
```

The raw drop zone becomes:

```text
/Volumes/sentinel/raw/upi_drop
```

The local landing reader:

```text
text
```

can be switched to:

```text
cloudFiles
```

for Databricks Auto Loader.

No module under `src/sentinel` directly depends on the deployment environment.

---

## Deployment

Authenticate:

```bash
databricks auth login --host https://<workspace-host>
```

Validate without modifying the workspace:

```bash
make deploy-dry
```

Deploy:

```bash
make deploy
```

Deploy and trigger:

```bash
make deploy-run
```

Windows:

```powershell
.\databricks\deploy.ps1 -DryRun
```

then:

```powershell
.\databricks\deploy.ps1
```

Deployment is designed to be idempotent, so an existing job is updated instead of creating duplicate jobs.

### Current Deployment Status

The Databricks deployment has **not yet been executed against a live workspace** because workspace credentials were not available during development.

Before a real deployment, `silver.pii_salt` must be moved from `conf/base.yaml` into a Databricks secret scope.

---

# Testing & Quality

The test suite covers:

* Data generation
* Schema validation
* Timestamp parsing
* Data-quality rules
* Quarantine reasons
* Deduplication
* Fraud scoring
* Threshold behaviour
* Detection metrics
* End-to-end execution
* Dashboard export
* Data masking
* Deployment configuration

Quality tooling:

```text
Pytest
Ruff
Mypy
TypeScript
```

Current validation:

```text
119 tests passing
Ruff clean
Mypy clean
TypeScript clean
```

---

# What This Does Not Do

### The fraud detector is rule-based

This is not a machine-learning model.

The rules are intentionally:

* Transparent
* Explainable
* Tunable through YAML
* Easy to test

They will not detect behavioural patterns that have not been explicitly defined.

### Gold is a full recompute

This is appropriate for the current project scale.

At much larger scale, incremental Gold processing and stateful merges would be the natural next step.

### Detection metrics use injected labels

Precision and recall are measured against the generator's definition of fraud.

Therefore:

> **100% precision against generated labels does not mean 100% real-world fraud precision.**

It means the pipeline agrees with the controlled anomaly population used for evaluation.

---

# Key Engineering Decisions

| Decision                  | Reason                                                   |
| ------------------------- | -------------------------------------------------------- |
| Raw text landing          | Preserve source data exactly                             |
| String-based Bronze       | Prevent schema inference from destroying variants        |
| Explicit Silver typing    | Make data-quality failures observable                    |
| Quarantine table          | Preserve invalid records and reasons                     |
| Salted hashes             | Enable behavioural analysis without exposing identifiers |
| Watermarked deduplication | Keep streaming state bounded                             |
| Batch Gold                | Simplify complex aggregations and window comparisons     |
| Additive scoring          | Provide explainable fraud decisions                      |
| Tukey threshold           | Reduce sensitivity to injected outliers                  |
| Separate truth file       | Prevent data leakage                                     |
| Static dashboard          | Avoid API credentials and backend infrastructure         |
| Shared pipeline functions | Keep local and Databricks implementations consistent     |

---

# Tech Stack

### Data Engineering

* Python 3.11
* PySpark 3.5
* Delta Lake 3.2
* Structured Streaming
* Databricks Runtime 15.4 LTS
* Unity Catalog
* Auto Loader

### Frontend

* React
* TypeScript
* Vite
* Hand-rolled SVG visualisations

### Testing & Quality

* Pytest
* Ruff
* Mypy
* TypeScript

---

# Future Improvements

* Kafka-based continuous ingestion
* Incremental Gold processing
* ML-based anomaly detection
* Feature-store integration
* Model monitoring
* Real-time alert delivery
* Databricks Workflows orchestration
* Secret-scope integration
* Historical fraud feedback loops
* Graph-based shared-account detection

---

# Conclusion

Project Sentinel demonstrates an end-to-end data engineering workflow for messy UPI payment telemetry:

```text
Generate
   ↓
Land raw data
   ↓
Structure safely
   ↓
Clean + validate
   ↓
Quarantine defects
   ↓
Mask identifiers
   ↓
Deduplicate retries
   ↓
Score behavioural anomalies
   ↓
Aggregate business KPIs
   ↓
Export analytics
   ↓
Visualise results
```

The project is built around one principle:

> **Structural problems should be repaired or quarantined; behavioural problems should be detected and explained.**

The same tested pipeline can run locally for development and be configured for Databricks and Unity Catalog for production deployment.

**Author:** Saksham Agarwal
