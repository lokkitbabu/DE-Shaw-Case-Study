# Simulation for optimizing packaging strategies under waste-based taxation
# Author: Lokkit Sanjay Babu Narayanan
# Date: April 2025
# Made for D. E. Shaw Case Study

import numpy as np
import pandas as pd

# price (P), value (V), and lambda (sensitivity)
products = [
    {"Product": "Smartphone", "P": 650, "V": 600, "lambda": 0.01},
    {"Product": "Headphones", "P": 100, "V": 80, "lambda": 0.03},
    {"Product": "T-Shirt", "P": 30, "V": 20, "lambda": 0.05},
    {"Product": "Paper Towels", "P": 4, "V": 3, "lambda": 0.07},
]

# environmental multiplier (M), base survivability (S0), max survivability (Smax), and log gain coefficient (k)
materials = [
    {"Material": "Styrofoam", "M": 2.0, "S0": 0.95, "Smax": 0.995, "k": 5.0},
    {"Material": "Plastic Film", "M": 1.5, "S0": 0.90, "Smax": 0.97, "k": 4.5},
    {"Material": "Recycled PET", "M": 1.0, "S0": 0.85, "Smax": 0.95, "k": 4.5},
    {"Material": "Cardboard", "M": 0.5, "S0": 0.80, "Smax": 0.93, "k": 4.0},
    {"Material": "Compostable Fiber", "M": 0.2, "S0": 0.75, "Smax": 0.91, "k": 3.5},
]

weights = np.arange(0.05, 0.30, 0.05)
waste_tax_base = 0.50
epsilon = 1.0

rows = []
for product in products:
    for material in materials:
        for weight in weights:
            S = min(material["Smax"], material["S0"] + material["k"] * np.log(weight + epsilon))
            expected_loss = (1 - S) * product["V"]
            waste_tax = weight * material["M"] * waste_tax_base
            TEC = product["P"] + waste_tax
            CR = max(0, 1 - product["lambda"] * (TEC - product["P"]))
            revenue = CR * (product["P"] - expected_loss)
            rows.append({
                "Product": product["Product"],
                "Material": material["Material"],
                "Weight (kg)": round(weight, 2),
                "Survivability": round(S, 4),
                "Waste Tax ($)": round(waste_tax, 4),
                "Expected Loss ($)": round(expected_loss, 2),
                "TEC ($)": round(TEC, 2),
                "Conversion Rate": round(CR, 4),
                "Expected Revenue ($)": round(revenue, 2)
            })

df_simulation = pd.DataFrame(rows)

best_configurations = (
    df_simulation.loc[df_simulation.groupby("Product")["Expected Revenue ($)"].idxmax()]
    .sort_values(by=["Product", "Expected Revenue ($)"], ascending=[True, False])
    .reset_index(drop=True)
)

columns_order = [
    "Product", "Material", "Weight (kg)", "Survivability",
    "Waste Tax ($)", "Expected Loss ($)", "TEC ($)",
    "Conversion Rate", "Expected Revenue ($)"
]
best_configurations = best_configurations[columns_order]

print(best_configurations.to_string(index=False))