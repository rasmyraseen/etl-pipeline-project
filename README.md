
# 🚀 Advanced ETL Pipeline - PySpark + Docker

This project implements an advanced ETL pipeline using PySpark. It includes:

- Data ingestion from CSV
- External API currency conversion
- Data validation, enrichment, and transformation
- Loading into Microsoft SQL Server
- Logging and error handling

---

## 📁 Project Structure

```
etl_pipeline_project/
│
├── data/
│   ├── sales_data.csv
│   └── product_reference.csv
│
├── jars/
│   └── mssql-jdbc-12.10.1.jre11.jar
│
├── logs/
│   └── conversion_log.csv
│
├── rejected/
│   └── rejected_records.csv
│
├── notebooks/
│   └── AdvancedETL.ipynb      # Jupyter notebook version
│
├── scripts/
│   └── advanced_etl.py        # PySpark script version (if any)
│
├── docker-compose.yml
├── Dockerfile (optional)
├── create_tables.sql
└── README.md
```

---

## 🧰 Setup Instructions

### ✅ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Optional: Microsoft SQL Server running locally or remotely (port `1433`)

### ✅ Clone the Project

```bash
git clone https://github.com/yourusername/etl_pipeline_project.git
cd etl_pipeline_project
```

### ✅ Start the Jupyter + PySpark Environment

```bash
docker-compose up
```

Once started, find the Jupyter Notebook URL (with token) in the logs:

```bash
docker logs etl-pipeline
```

🔗 Example: `http://localhost:8888/?token=abc123...`

---

## ▶️ How to Run the ETL

1. Open the Jupyter Notebook in browser using the token URL.
2. Navigate to:  
   `notebooks/AdvancedETL.ipynb`
3. Run all cells from top to bottom.

✅ It will:
- Load source data
- Fetch exchange rates from API
- Convert currencies
- Validate and enrich data
- Log conversions and errors
- Load data to SQL Server (`SalesEnriched` table)

---

## 🗄️ SQL Server Setup

Before running the ETL, run the schema creation script:

```bash
# Inside your SQL Server client
USE SalesDB;
GO

-- Execute this
CREATE TABLE SalesEnriched (
    ...
);
```

The script is provided in:  
`create_tables.sql`

---

## 💡 Tips

- To stop/start the environment:
  ```bash
  docker-compose stop
  docker-compose start
  ```
- To rebuild from scratch:
  ```bash
  docker-compose down
  docker-compose up --build
  ```
- To view logs:
  ```bash
  docker logs etl-pipeline
  ```
