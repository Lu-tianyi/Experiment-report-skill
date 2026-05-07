import numpy as np
from scipy import stats
import json

# Correct interpretation based on analysis:
# Rows correspond to different If values: [0.600, 0.625, 0.650, 0.675, 0.700] A
# Columns correspond to different Ua values: [0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.00] V
# (The column headers 16, 25, 36, 49, 64, 81, 100 are divided by 100 to get Ua in V)

If_values = np.array([0.600, 0.625, 0.650, 0.675, 0.700])  # A
Ua_values = np.array([0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.00])  # V

# Temperature calculation: T = 900 + 1430 * If
T = 900 + 1430 * If_values

# Ia data (mA) - 5 rows (different If) x 7 columns (different Ua)
Ia_data = np.array([
    [59, 62, 66, 69, 68, 72, 76],        # If = 0.600 A
    [110, 117, 125, 127, 131, 137, 142],  # If = 0.625 A
    [199, 211, 221, 230, 238, 244, 252],  # If = 0.650 A
    [336, 365, 383, 399, 410, 423, 437],  # If = 0.675 A
    [544, 603, 637, 670, 693, 719, 736],  # If = 0.700 A
])

# Constants
k_over_e = 8.617333262e-5  # k/e in eV/K

# Step 1: Calculate temperatures
print("=== Step 1: Temperature Calculation ===")
for i in range(5):
    print(f"If = {If_values[i]:.3f} A -> T = {T[i]:.1f} K")
print()

# Step 2: For each If (each row), perform linear regression of lg(Ia) vs sqrt(Ua)
# to find the intercept lg(I) at Ua = 0 (zero-field current)
sqrt_Ua = np.sqrt(Ua_values)
lg_Ia = np.log10(Ia_data.astype(float))

intercepts = []
slopes = []
r_values = []

print("=== Step 2: lg(Ia) vs sqrt(Ua) Linear Regression ===")
for row in range(5):
    x = sqrt_Ua
    y = lg_Ia[row, :]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    intercepts.append(intercept)
    slopes.append(slope)
    r_values.append(r_value)
    print(f"If = {If_values[row]:.3f} A, T = {T[row]:.1f} K:")
    print(f"  lg(Ia) = {slope:.4f}*sqrt(Ua) + {intercept:.4f}, r = {r_value:.6f}")
print()

# Step 3: Richardson plot - lg(I/T^2) vs 1/T
# From Richardson-Dushman: I = A*S*T^2*exp(-e*phi/(k*T))
# lg(I/T^2) = lg(A*S) - (e*phi/(k*ln(10)))*(1/T)
# slope = -e*phi/(k*ln(10)) => phi = -slope * (k/e) * ln(10)

lg_I = np.array(intercepts)
lg_I_over_T2 = lg_I - 2 * np.log10(T)
inv_T = 1.0 / T

print("=== Step 3: Richardson Plot Data ===")
for i in range(5):
    print(f"T = {T[i]:.1f} K: lg(I) = {lg_I[i]:.4f}, lg(I/T^2) = {lg_I_over_T2[i]:.4f}, 1/T = {inv_T[i]:.6f}")
print()

# Linear regression: lg(I/T^2) = slope*(1/T) + intercept
slope_rich, intercept_rich, r_rich, p_rich, std_err_rich = stats.linregress(inv_T, lg_I_over_T2)

print("=== Step 4: Richardson Plot Regression ===")
print(f"lg(I/T^2) = {slope_rich:.4f}*(1/T) + {intercept_rich:.4f}")
print(f"r = {r_rich:.6f}")
print()

# Calculate work function phi
phi = -slope_rich * k_over_e * np.log(10)

print("=== Step 5: Work Function Calculation ===")
print(f"Work function phi = {phi:.4f} eV")
print(f"Work function W = {phi:.4f} eV")
print()

# Calculate A*S from intercept
AS = 10 ** intercept_rich
print(f"A*S = {AS:.4e} A/K^2")

# Save results
results = {
    "If_values": If_values.tolist(),
    "Ua_values": Ua_values.tolist(),
    "T": T.tolist(),
    "lg_I": lg_I.tolist(),
    "lg_I_over_T2": lg_I_over_T2.tolist(),
    "inv_T": inv_T.tolist(),
    "slope_rich": float(slope_rich),
    "intercept_rich": float(intercept_rich),
    "r_rich": float(r_rich),
    "phi_eV": float(phi),
    "AS": float(AS),
    "Ia_data": Ia_data.tolist(),
    "sqrt_Ua": sqrt_Ua.tolist(),
    "lg_Ia": lg_Ia.tolist(),
    "intercepts": intercepts,
    "slopes": slopes,
    "r_values": r_values,
}

with open("C:/Users/Cgy123456/.agents/skills/大物实验报告skill/scripts/results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nResults saved to results.json")
