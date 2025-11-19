from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import logging
import os
from config.setup import initilize_environment
from services.extract_data import fetch_paginated_api_velib, data_to_df, get_unique_communes, fetch_paginated_api_cars
from services.load_to_big_query import upload_dataframe_to_bigquery
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    global chunking_service_instance
    logger.info("Starting up The Data Pipeline Module...")
    try:
        initilize_environment()
        logger.info("Google environment initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Google environment or services: {e}")
    yield
    logger.info("Shutting down The Data Pipeline Module...")

app = FastAPI(lifespan=lifespan)


@app.get("/upload_data")
def upload_velib_data():

    velib_base_url = os.environ['VELIB_URL']
    velib_data = fetch_paginated_api_velib(velib_base_url)
    velib_df = data_to_df(velib_data)
    logger.info("Velib data fetched and converted to DataFrame successfully.")

    success = upload_dataframe_to_bigquery(
        df=velib_df,
        table_id='quantic-factory-project.bikes_and_cars.bikes',
        service_account_file=os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    )
    if success:
        logger.info("Bikes Data Uploaded successfully.")
    else:
        raise HTTPException(status_code=500, detail="Failed to upload Velib data to BigQuery.")

    CARS_URL = os.environ['CARS_URL']
    unique_communes_insee_velib = get_unique_communes(data_to_df(velib_data))
    unique_communes_insee_velib = get_unique_communes(data_to_df(velib_data))
    cars_data = fetch_paginated_api_cars(CARS_URL, limit = 100, communes = unique_communes_insee_velib)
    cars_df = data_to_df(cars_data)
    
    cars_df = cars_df.rename (columns = {
    "codgeo": "commune_code",
    "libgeo": "commune_name",
})
    cars_df["date_arrete"] = pd.to_datetime(cars_df["date_arrete"])
    cars_2025 = cars_df[cars_df["date_arrete"].dt.year == 2025]
    cars_2025_recent = cars_2025.sort_values(by="date_arrete", ascending=False).drop_duplicates(subset="commune_code", keep="first")
    

    logger.info("Cars data fetched and converted to DataFrame successfully.")

    success = upload_dataframe_to_bigquery(
        df=cars_2025_recent,
        table_id='quantic-factory-project.bikes_and_cars.cars',
        service_account_file=os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    )
    if success:
        logger.info("Cars Data Uploaded successfully.")
    else:
        raise HTTPException(status_code=500, detail="Failed to upload Cars data to BigQuery.")
    
    return {"message": "Data upload process completed."}

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)