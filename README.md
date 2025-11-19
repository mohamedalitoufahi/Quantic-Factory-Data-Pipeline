# Vélib & Private Cars Analysis: Paris Region

A data analysis project examining the relationship between available Vélib bikes and private car ownership in Parisian communes.

**Author:** Mohamed Ali Toufahi - INSAT  

---

## 📊 Project Overview

### Problem Statement

Among the benefits promoted by bike-sharing projects like Vélib is the reduction in the need for private cars. To test this impact and inform public policy, we analyze two Open Data Paris datasets:

- **Vélib: Bikes and Stations - Real-time Availability**  
  Source: https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information

- **Private Cars Registered by Commune and Charging Type**  
  Source: https://opendata.agenceore.fr/explore/dataset/voitures-par-commune-par-energie/information/

---

## 🛠️ Tech Stack

### Data Loading Microservice
- **FastAPI** - REST API framework
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

### Data Warehouse
- **BigQuery** - Cloud data warehouse

### Visualization
- **Looker Studio** (formerly Google Data Studio)

---

## 🏗️ Architecture

### Workflow Schema

```
1. Fetch both datasets + transformation + upload via REST API
2. Data manipulation and joins on BigQuery
3. Visualization and analysis with Looker
```

### Backend Organization
The backend is organized in layers with separation of concerns:
- **Service Layer** - REST entry points
- **Extract Data Service** - Browses APIs by pages and extracts results while filtering irrelevant communes
- **Load Data Service** - Handles Google Cloud authentication

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Google Cloud account with BigQuery enabled
- Service account JSON authentication key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mohamedalitoufahi/Quantic-Factory-Data-Pipeline
cd Quantic-Factory-Data-Pipeline
```

2. Create two tables in BigQuery:
   - `bikes`
   - `cars`

3. Place your Google Cloud service account JSON key in the project directory

4. Launch the microservice:
```bash
docker compose up
```

### Data Transformations

For the private cars dataset, the following transformations were applied:
- Column name standardization
- Filtering for Île-de-France communes only
- Selection of 2025 data

---

## 📈 Data Analysis

### Join Query for Final Analysis Table

```sql
CREATE TABLE bikes_and_cars.analysis_table AS
SELECT 
    i.code_insee_commune,
    i.nom_arrondissement_communes, 
    i.nombre_de_velo_dispo, 
    c.nb_vp
FROM bikes_and_cars.cars AS c
INNER JOIN (
    SELECT 
        code_insee_commune,
        nom_arrondissement_communes, 
        SUM(capacity) AS nombre_de_velo_dispo
    FROM bikes_and_cars.bikes
    GROUP BY code_insee_commune, nom_arrondissement_communes
) AS i
ON c.commune_code = i.code_insee_commune
```

**Note:** 
- `bikes` table contains bike availability data
- `cars` table contains private vehicle data
- Solution uses INNER JOIN to combine datasets

---

## 📊 Results & Conclusions

**Interactive Dashboard:**  
[View Looker Studio Report](https://lookerstudio.google.com/reporting/5a2a1daa-ebec-4b8c-905a-b09a215dff0c)

### Key Findings

**Surprisingly, there is no negative correlation as expected!** Both the number of cars and the number of bikes in service appear to be correlated with population density and demand rather than inversely correlated with each other.

### Limitations

- **Limited Dataset:** Finding comprehensive datasets for 2025 was challenging
- **Small Sample Size:** Reduced number of data points limits statistical confidence

### Important Note

**We cannot conclude that bikes and alternative transportation have no effect.** There may be an attenuation of need that requires more extensive data to detect. A **difference-in-differences analysis** would be most revealing for establishing causal relationships.

---

## 🔗 Resources

- **GitHub Repository:** https://github.com/mohamedalitoufahi/Quantic-Factory-Data-Pipeline
- **Looker Dashboard:** https://lookerstudio.google.com/reporting/5a2a1daa-ebec-4b8c-905a-b09a215dff0c
- **Vélib Data Source:** https://tinyurl.com/cfahhs27
- **Car Registration Data:** https://l1nq.com/RIV2x

---

## 📝 License

This project was completed as part of a Data Analysis and DataOps exercise at INSAT.

---

**Thank you for your interest in this project!**
