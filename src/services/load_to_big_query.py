import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path


def upload_dataframe_to_bigquery(
    df: pd.DataFrame,
    table_id: str,
    service_account_file: str,
    write_disposition: str = "WRITE_TRUNCATE"
) -> bool:

    try:
        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        
        # Initialize BigQuery client
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )
        
        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            autodetect=True,
        )
        
        # Upload DataFrame
        job = client.load_table_from_dataframe(
            df, 
            table_id, 
            job_config=job_config
        )
        
        # Wait for the job to complete
        job.result()
        
        print(f"✓ Loaded {len(df)} rows into {table_id}")
        
        # Verify the upload
        table = client.get_table(table_id)
        print(f"✓ Table now has {table.num_rows} rows")
        
        return True
        
    except Exception as e:
        print(f"✗ Error uploading to BigQuery: {e}")
        return False


if __name__ == "__main__":
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    })
    
    # Upload to BigQuery
    success = upload_dataframe_to_bigquery(
        df=df,
        table_id='quantic-factory-project.bikes_and_cars.try'
    )
    
    if success:
        print("Upload completed successfully!")
    else:
        print("Upload failed.")