import pandas as pd
import numpy as np
import os

def main():
    os.makedirs("data", exist_ok=True)

    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", end="2024-06-30")
    regions = ["North", "South", "East", "West", "Central"]
    diseases = ["Flu", "Malaria", "COVID"]

    data = []

    for date in dates:
        for region in regions:
            for disease in diseases:
                base = {"Flu": 40, "Malaria": 60, "COVID": 30}[disease]

                cases = np.random.poisson(lam=base)
                vaccinations = np.random.randint(20, 120)

                data.append([date, region, disease, cases, vaccinations])

    df = pd.DataFrame(data, columns=[
        "date", "region", "disease", "cases", "vaccinations"
    ])

    # Inject anomalies
    df.loc[200:220, "cases"] *= 3
    df.loc[150, "cases"] = None
    df.loc[300, "cases"] = 0

    df.to_csv("data/raw_health_data.csv", index=False)

    print("Mock data generated.")


if __name__ == "__main__":
    main()