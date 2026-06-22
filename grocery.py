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

#     print(
#         con.sql(
#             f"""
#             WITH
#             -- Expand each non-canceled booking into one row per night occupied 
#             nights AS (
#                 SELECT
#                     unnest(
#                         range(checkin_date::DATE, checkout_date::DATE, INTERVAL '1 day')
#                     )::DATE AS night_date
#                 FROM {TABLE_NAME}
#                 WHERE is_canceled = 0
#             ),
#             -- Count rooms occupied per night
#             daily_occupancy AS (
#                 SELECT
#                     night_date,
#                     COUNT(*) AS rooms_occupied
#                 FROM nights
#                 GROUP BY night_date
#             ),
#             -- Sum booked room-nights per calendar month
#             monthly_stats AS (
#                 SELECT
#                     DATE_TRUNC('month', night_date)::DATE AS month_start,
#                     SUM(rooms_occupied) AS booked_room_nights
#                 FROM daily_occupancy
#                 GROUP BY DATE_TRUNC('month', night_date)
#             )
#             SELECT
#                 month_start,
#                 booked_room_nights,
#                 200 * DATEDIFF('day', month_start, month_start + INTERVAL '1 month')
#                     AS available_room_nights,
#                 FLOOR(
#                     booked_room_nights * 100.0
#                     / (200 * DATEDIFF('day', month_start, month_start + INTERVAL '1 month'))
#                 )::INTEGER AS occupancy_rate_pct
#             FROM monthly_stats
#             WHERE YEAR(month_start) = 2016
#             ORDER BY month_start;
# """
#         )
#     )

if __name__ == '__main__':
    main()

