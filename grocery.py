import duckdb
import os

def load_db(in_file,table_name,db_path):
    # Connect to Database, EPastore 05/15/2026
    con = duckdb.connect(db_path)

    # Load data into database and close connection, EPastore 05/15/2026
    con.sql(
        f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv('{in_file}')
        """
    )

    con.close()

def main():
    # Declare Constants, EPastore 06/12/2026
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(SCRIPT_DIR,'grocery_transactions.csv')
    TABLE_NAME = 'grocery_transactions'
    DB_PATH = os.path.join(SCRIPT_DIR,"my_database.duckdb")

    # Create table in database, EPastore 05/17/2026
    load_db(CSV_FILE,TABLE_NAME,DB_PATH)

    # Connect to the database, EPastore 05/17/2026
    con = duckdb.connect(DB_PATH)

    # Test connection, EPastore 05/17/2026
    print(
    con.sql(
        f"""
            SELECT * FROM {TABLE_NAME} LIMIT 10;
        """))
    
    print(
    con.sql(
        f"""
            SELECT COUNT(upc) FROM {TABLE_NAME};
        """))
    
    # Business Question
    # How many transactions does the top product pairing have?

    print(
        con.sql(
            f"""
                SELECT
                    a.product_name AS product_1,
                    b.product_name AS product_2,
                    COUNT(DISTINCT a.transaction_id) AS transaction_count
                FROM {TABLE_NAME} a
                JOIN {TABLE_NAME} b
                    ON  a.transaction_id = b.transaction_id
                    AND a.upc < b.upc
                GROUP BY a.product_name, b.product_name
                ORDER BY transaction_count DESC
                LIMIT 1;
            """
        )
    )

if __name__ == '__main__':
    main()

