import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("avgIQpercountry.csv")


avg_iq_per_continent = df.groupby('Continent')['Average IQ'].mean()


plt.figure(figsize=(10, 6))


avg_iq_per_continent.plot(kind="line", marker="o", color="skyblue")


plt.title("Average IQ by continent")
plt.xlabel("Continent")
plt.ylabel("Average IQ")


plt.grid(axis="both", linestyle="--", alpha=0.7)


plt.show()
