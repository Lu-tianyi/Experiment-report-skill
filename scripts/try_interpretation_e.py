import numpy as np
from scipy import stats

# Let me try transposing the interpretation:
# Maybe the 5 row values (0.600, 0.625, 0.650, 0.675, 0.700) are If values
# And the 7 column values (16, 25, 36, 49, 64, 81, 100) represent Ua in some unit

# Original data (5 rows x 7 columns)
data_original = np.array([
    [59, 62, 66, 69, 68, 72, 76],
    [110, 117, 125, 127, 131, 137, 142],
    [199, 211, 221, 230, 238, 244, 252],
    [336, 365, 383, 399, 410, 423, 437],
    [544, 603, 637, 670, 693, 719, 736],
])

k_over_e = 8.617333262e-5

# Interpretation E: Rows are different If values, columns are different Ua values
# If = [0.600, 0.625, 0.650, 0.675, 0.700] A (5 values)
# Ua = [0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.00] V (7 values, from 16,25,...,100 divided by 100)

If_values = np.array([0.600, 0.625, 0.650, 0.675, 0.700])
Ua_values = np.array([0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.00])
T = 900 + 1430 * If_values

print("=== Interpretation E: Rows=If, Columns=Ua ===")
print(f"If = {If_values} A")
print(f"Ua = {Ua_values} V")
print(f"T = {T} K")
print()

# For each If (row), perform lg(Ia) vs sqrt(Ua) regression
sqrt_Ua = np.sqrt(Ua_values)
lg_Ia = np.log10(data_original.astype(float))

intercepts = []
for row in range(5):
    slope, intercept, r, _, _ = stats.linregress(sqrt_Ua, lg_Ia[row, :])
    intercepts.append(intercept)
    print(f"If = {If_values[row]:.3f} A, T = {T[row]:.1f} K: lg(I) = {intercept:.4f}, r = {r:.6f}")

lg_I = np.array(intercepts)
lg_I_over_T2 = lg_I - 2 * np.log10(T)
inv_T = 1.0 / T

print()
print("Richardson plot data:")
for i in range(5):
    print(f"  T = {T[i]:.1f} K: lg(I/T²) = {lg_I_over_T2[i]:.4f}, 1/T = {inv_T[i]:.6f}")

slope_rich, intercept_rich, r_rich, _, _ = stats.linregress(inv_T, lg_I_over_T2)
phi = -slope_rich * k_over_e * np.log(10)

print(f"\nRichardson plot: slope = {slope_rich:.4f}, r = {r_rich:.6f}")
print(f"Work function phi = {phi:.4f} eV")

if phi > 0 and phi < 10:
    print("*** REASONABLE! ***")
