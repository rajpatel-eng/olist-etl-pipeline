# Olist E-commerce ETL Pipeline

A batch ETL pipeline in Python that loads the Olist Brazilian e-commerce dataset into MySQL, with incremental loading, data quality checks and logging.

## What it does

1. **Extract**: reads 4 CSV files (customers, products, orders, order_items) with pandas
2. **Transform**: cleans text, converts dates and numbers, removes duplicates and null keys
3. **Quality checks**: stops the load of a table if keys are null or duplicated, data is empty, or prices are negative
4. **Load**: writes to a staging table, then inserts only new rows into the final table (INSERT IGNORE) inside a transaction
5. **Logging**: every step is logged to the console and to logs/etl.log

## Tech stack

Python, pandas, SQLAlchemy, PyMySQL, MySQL 8

## Results (on my machine)

- First run: 245,042 rows loaded in 42.1 s
- Second run: 0 new rows (incremental load works, no duplicates), 29.6 s
- If one table fails, the other tables still load and the pipeline exits with code 1

## Project structure

    src/
      config.py      - paths, DB connection, table list
      logger.py      - file and console logging
      schema.py      - CREATE TABLE statements (primary keys)
      extract.py     - CSV reading
      transform.py   - cleaning per table
      quality.py     - data quality checks
      load.py        - staging and incremental insert
      main.py        - runs the whole pipeline
    queries.sql      - analysis queries

## How to run

1. Download the Olist dataset from Kaggle and place these files in data/raw/:
   olist_customers_dataset.csv, olist_products_dataset.csv, olist_orders_dataset.csv, olist_order_items_dataset.csv
2. Create the database:

        CREATE DATABASE olist_db CHARACTER SET utf8mb4;

3. Create a .env file in the project root:

        DB_USER=root
        DB_PASSWORD=your_password
        DB_HOST=localhost
        DB_PORT=3306
        DB_NAME=olist_db

4. Install and run:

        pip install -r requirements.txt
        python src/main.py

5. Run the analysis queries:

        mysql -u root -p olist_db --table -e "source queries.sql"

## Sample findings

- Sao Paulo (SP) has the highest revenue.
- Alagoas (AL) has the highest share of late deliveries (about 24% of delivered orders).

## Limitations and next steps

- INSERT IGNORE only adds new rows; it does not update rows that changed.
- Scheduling (Airflow), a star schema and cloud storage are not implemented yet.
