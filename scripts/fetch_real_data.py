import os
import requests
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_hubeau_data():
    print("Fetching Toulouse (Garonne) measurements from Hub'Eau...")
    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc"
    params = {
        "code_departement": "31",
        "code_parametre": "1301,1302,1303,1340,1350",
        "date_debut_prelevement": "2021-01-01",
        "size": 1000
    }
    r = requests.get(url, params=params, timeout=30)
    print("Status code:", r.status_code)
    if r.status_code in [200, 206]:
        data = r.json().get("data", [])
        if data:
            df = pd.DataFrame(data)
            cols = [
                "code_station", "libelle_station", "date_prelevement",
                "code_parametre", "libelle_parametre", "resultat",
                "symbole_unite", "longitude", "latitude"
            ]
            valid_cols = [c for c in cols if c in df.columns]
            df = df[valid_cols]
            out = os.path.join(DATA_DIR, "toulouse_hubeau_real.csv")
            df.to_csv(out, index=False)
            print(f"SUCCESS: Saved {len(df)} rows to {out}")
            return df
    print("Failed to save data.")
    return None

if __name__ == "__main__":
    fetch_hubeau_data()
