import requests
import pandas as pd
#from google.cloud import bigquery
from time import sleep
import os

#client = bigquery.Client(project=os.environ['PROJECT_ID'])

def fetch_paginated_api_velib(base_url, limit=100):
    offset = 0
    results = []
    while True:
        url = f"{base_url}&limit={limit}&offset={offset}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        batch = data["results"]
        if len(batch) == 0:
            break
        results.extend(batch)
        offset += limit
        if offset >= data["total_count"]:
            break
        sleep(0.1)
    return results

def data_to_df(data):
    df = pd.DataFrame(data)
    return df

def get_unique_communes(velib_df):
    unique_communes = velib_df["code_insee_commune"].unique()
    return unique_communes

def fetch_paginated_api_cars(base_url, limit=100, communes=[]):
    offset = 0
    results = []
    if len(communes) > 0:
        communes_list_str = ",".join([f'"{c}"' for c in communes])
        where_clause = f"where=codgeo in ({communes_list_str})"
    else:
        where_clause = ""
    while True:
        if offset == 9900:
          limit = 99
        url = f"{base_url}?limit={limit}&offset={offset}"
        if where_clause:
            url += f"&{where_clause}"

        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("results", [])
        if not batch:
            break
        results.extend(batch)
        if offset == 9900:
          break
        offset += limit
        if offset >= data.get("total_count", 0):
            break
        sleep(0.1)
    return results


if __name__ == "__main__":
    velib_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?"
    velib_data = fetch_paginated_api_velib(velib_url)
    print(f"Fetched {len(velib_data)} Velib records.")
    cars_url = "https://opendata.agenceore.fr/api/explore/v2.1/catalog/datasets/voitures-par-commune-par-energie/records?"
    unique_communes_insee_velib = get_unique_communes(data_to_df(velib_data))
    cars_data = fetch_paginated_api_cars(cars_url, limit = 100, communes = unique_communes_insee_velib)
    print(cars_data)