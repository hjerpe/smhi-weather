import sqlite3

import pandas as pd
import requests


class DataUpdater:
    def __init__(self, db_path: str) -> None:
        """
        Initialize the data updater with the database path and the API URL.

        :param db_path: A string specifying the path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)

    def create_table(self) -> None:
        """
        Create the data table if it does not exist already.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS data (
            station_id TEXT,
            station_active TEXT,
            station_municipality TEXT,
            Datum TEXT,
            Tid_UTC TEXT,
            Lufttemperatur REAL,
            Kvalitet TEXT,
            Tidsutsnitt TEXT
        )
        """
        )
        self.conn.commit()

    def fetch_and_update_db(self, df_new: pd.DataFrame) -> None:
        """
        Fetch new data from the API and update the database with only the newer entries.
        """
        self.create_table()
        # Get the latest date in the database for each group
        # TODO: Must combine the time and date columns to get the latest date
        query = """
        SELECT station_id, MAX(Datum) as max_date
        FROM data
        GROUP BY station_id
        """
        df_max_dates = pd.read_sql(query, self.conn)

        # Merge new data with max dates to identify newer records
        df_new.rename(columns={"Tid (UTC)": "Tid_UTC"}, inplace=True)
        df_combined = pd.merge(df_new, df_max_dates, on=["station_id"], how="left")
        print(df_combined)
        print(df_combined.columns)

        # Filter out records from the new data where the date is not greater than the max date in the corresponding group
        # TODO: Must combine the time and date columns to get the latest date
        df_to_insert = df_combined[
            (df_combined["Datum"] > df_combined["max_date"])
            | df_combined["max_date"].isnull()
        ]

        # Insert the filtered new data into the database
        cols = [
            "station_id",
            "station_active",
            "station_municipality",
            "Datum",
            "Tid_UTC",
            "Lufttemperatur",
            "Kvalitet",
            "Tidsutsnitt",
        ]
        if not df_to_insert.empty:
            df_to_insert[cols].to_sql(
                "data", self.conn, if_exists="append", index=False
            )
        print("Database updated with new data!")
