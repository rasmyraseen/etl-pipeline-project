# PySpark Notebook: Advanced ETL Pipeline Implementation

# --- 1. Imports and Spark Initialization ---
import logging
import requests
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, lit, current_timestamp
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import to_date
import shutil
import os


spark = SparkSession.builder \
    .appName("AdvancedETL") \
    .config("spark.jars", "/app/jars/mssql-jdbc-12.10.1.jre11.jar") \
    .getOrCreate()


# spark.sparkContext.addJar("/opt/spark/jars/mssql-jdbc-12.10.1.jre11.jar")



# ✅ JDBC driver check
print("[INFO] JDBC driver is available:", spark._jvm.com.microsoft.sqlserver.jdbc.SQLServerDriver)

# breakpoint()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/home/jovyan/etl_pipeline_error_log.log"),
        logging.StreamHandler()
    ]
)


# --- 2. Load Data ---

sales_df = spark.read.option("header", True).csv("data/sales_data_2.csv")
print(f"[INFO] sales_df row count: {sales_df.count()}")
sales_df.show(5)  # To inspect the first 5 rows
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
sales_df.show(10)



sales_df.filter(col("SaleAmount").isNull()).show()  # Check rows where SaleAmount is null

sales_df.filter(col("OrderDate").isNull()).show()   # Check rows where OrderDate is null

sales_df.filter((col("SaleAmount").isNotNull()) & (col("OrderDate").isNotNull())).show(5)



# --- 3. Data Cleaning ---
# sales_df_clean = sales_df.dropna(subset=["SaleAmount", "OrderDate"])
# sales_df_clean = sales_df.dropDuplicates(["OrderID"])
# sales_df_clean = sales_df_clean.filter(
#     (col("SaleAmount").cast("double").isNotNull()) &
#     (col("OrderDate").cast("date").isNotNull())
# )
# print(f"[INFO] sales_df_clean row count: {sales_df_clean.count()}")
# sales_df_clean.show(5)  # To inspect the first 5 rows



sales_df_clean = (
    sales_df
    .dropna(subset=["SaleAmount", "OrderDate"])
    .dropDuplicates(["OrderID"])
    .withColumn("OrderDateParsed", to_date("OrderDate", "MM/dd/yyyy"))  # Adjust format as needed
    .filter(
        (col("SaleAmount").cast("double").isNotNull()) &
        (col("OrderDateParsed").isNotNull())
    )
)

sales_df_clean.show(5) 

# breakpoint()

product_df = spark.read.option("header", True).csv("data/product_reference_2.csv")


# --- 4. Lookup: Join with Product Reference ---
enriched_df = sales_df_clean.join(product_df, on="ProductID", how="left")
print(f"[INFO] enriched_df row count: {enriched_df.count()}")
enriched_df.show(5)  # To inspect the first 5 rows


# --- 5. Currency Conversion via API ---
def get_exchange_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        return response.json().get("rates", {})
    except Exception as e:
        logging.error(f"Exchange rate API failed: {e}")
        return {"EUR": 1.0, "GBP": 1.0}

exchange_rates = get_exchange_rates()
broadcast_rates = spark.sparkContext.broadcast(exchange_rates)


@udf(DoubleType())
def convert_to_usd(amount, currency):
    try:
        rate = broadcast_rates.value.get(currency, 1.0)
        return float(amount) / float(rate)
    except Exception as e:
        logging.error(f"Conversion error: amount={amount}, currency={currency}, error={e}")
        return None

converted_df = enriched_df.withColumn("SaleAmountUSD", convert_to_usd(col("SaleAmount"), col("Currency")))
print(f"[INFO] converted_df row count: {converted_df.count()}")
converted_df.show(5)  # To inspect the first 5 rows



# --- 6. Logging Conversion Info ---
conversion_log_df = converted_df.withColumn("ConversionTime", current_timestamp()) \
    .select("OrderID", "Currency", "SaleAmount", "SaleAmountUSD", "ConversionTime")



log_path = "/app/logs/conversion_log"

# Clean entire log directory if it exists
if os.path.exists(log_path):
    try:
        shutil.rmtree(log_path)  # deletes folder and contents
        print(f"Deleted old log directory at {log_path}")
    except Exception as e:
        print(f"[WARN] Failed to delete log directory: {e}")

# Spark will create this folder fresh
conversion_log_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(log_path)

# --- 7. Error Handling ---
error_df = converted_df.filter(col("SaleAmountUSD").isNull())
error_df = error_df.withColumn("ErrorReason", lit("Invalid currency or amount")) \
                   .withColumn("RejectedAt", current_timestamp())
error_df.write.mode("overwrite").option("header", True).csv("rejected/rejected_records.csv")

error_rate = error_df.count() / converted_df.count()
if error_rate > 0.05:
    raise Exception(f"[ERROR] Rejected records exceed 5% threshold ({error_rate*100:.2f}%)")

# --- 8. Final Clean Data ---
final_df = converted_df.filter(col("SaleAmountUSD").isNotNull())

# --- 9. Write to SQL Database ---
jdbc_url = "jdbc:sqlserver://host.docker.internal:1433;databaseName=SalesDB;encrypt=true;trustServerCertificate=true"

db_props = {
    "user": "sa",
    "password": "qwe123!@#",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

final_df.write.jdbc(url=jdbc_url, table="SalesEnriched", mode="append", properties=db_props)

# Write rejected records to SQL for tracking
error_df.write.jdbc(url=jdbc_url, table="RejectedRecords", mode="append", properties=db_props)

import time
print("[INFO] ETL finished. Sleeping to keep container alive for debugging...")
time.sleep(300)  # Keep container alive for 5 minutes
