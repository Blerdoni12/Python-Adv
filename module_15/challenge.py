import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "weather_tokyo_data.csv")

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower()

df = df.replace(r"[\(\)]", "", regex=True)

num_cols = ["temperature", "humidity", "atmospheric pressure"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["date"] = pd.to_datetime(df["year"].astype(str) + "/" + df["day"], errors="coerce")

df.set_index("date", inplace=True)
df = df.sort_index()

df = df.dropna(subset=["temperature"])

avg_temp = round(df["temperature"].mean(), 2)
print("1. Temperatura mesatare totale:", avg_temp)


monthly_avg = df["temperature"].resample("ME").mean()

print("\n2. Mesatarja mujore:")
print(monthly_avg.round(2))

plt.figure()
monthly_avg.plot(kind="bar")
plt.title("Mesatarja Mujore e Temperatures - Tokyo")
plt.xlabel("Muaji")
plt.ylabel("Temperatura (°C)")
plt.tight_layout()
plt.show()

hot_day = df["temperature"].idxmax()
cold_day = df["temperature"].idxmin()

hot_temp = df.loc[hot_day, "temperature"]
cold_temp = df.loc[cold_day, "temperature"]

print("\n3. Dita më e nxehtë:")
print("   Data:", hot_day.strftime("%d-%m-%Y"), "| Temperatura:", hot_temp)

print("\n   Dita më e ftohtë:")
print("   Data:", cold_day.strftime("%d-%m-%Y"), "| Temperatura:", cold_temp)

plt.figure()
df["temperature"].plot()
plt.title("Temperatura ditore në kohë - Tokyo")
plt.xlabel("Data")
plt.ylabel("Temperatura (°C)")
plt.tight_layout()
plt.show()


df["month"] = df.index.month

seasons = {
    "Dimër": [12, 1, 2],
    "Pranverë": [3, 4, 5],
    "Verë": [6, 7, 8],
    "Vjeshtë": [9, 10, 11]
}

seasonal_avg = {
    season: df[df["month"].isin(months)]["temperature"].mean()
    for season, months in seasons.items()
}

seasonal_avg_df = pd.DataFrame.from_dict(seasonal_avg, orient="index", columns=["Mesatarja (°C)"])
print("\n5. Mesataret sezonale:")
print(seasonal_avg_df.round(2))

