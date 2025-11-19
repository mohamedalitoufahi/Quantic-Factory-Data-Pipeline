import os
from pathlib import Path


def initilize_environment():
    credentials_path = Path(__file__).parent / "quantic-factory-project-1ab4a3a0c753.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(credentials_path)
    PROJECT_ID = "quantic-factory-project"
    #REGION = ?????
    os.environ['PROJECT_ID'] = "quantic-factory-project"
    #os.environ['REGION'] = "us-central1"

    credentials_path = Path(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    if not credentials_path.exists():
        raise FileNotFoundError(f"Google credentials file not found: {credentials_path}")
    print("Google environment initialized successfully.")
    os.environ['VELIB_URL'] = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?"
    os.environ['CARS_URL'] = "https://opendata.agenceore.fr/api/explore/v2.1/catalog/datasets/voitures-par-commune-par-energie/records?"