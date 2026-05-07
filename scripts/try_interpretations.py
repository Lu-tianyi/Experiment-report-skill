import numpy as np
from scipy import stats

# Raw data
Ua = np.array([0.600, 0.625, 0.650, 0.675, 0.700])
Ia_data = np.array([
    [59, 62, 66, 69, 68, 72, 76],
    [110, 117, 125, 127, 131, 137, 142],
    [199, 211, 221, 230, 238, 244, 252],
    [336, 365, 383, 399, 410, 423, 437],
    [544, 603, 637, 670, 693, 719, 736],
])

k_over_e = 8.617333262e-5  # k/e in eV/K
sqrt_Ua = np.sqrt(Ua)
lg_Ia = np.log10(Ia_data.astype(float))

# Try different interpretations of If column headers [16, 25, 36, 49, 64, 81, 100]
interpretations = {
    "Interpretation A: If = [0.600, 0.625, ..., 0.750] A (from manual description)":
        np.array([0.600, 0.625, 0.650, 0.675, 0.700, 0.725, 0.750]),
    "Interpretation B: If = sqrt([16,25,...,100])/10 = [0.4, 0.5, ..., 1.0] A":
        np.sqrt(np.array([16, 25, 36, 49, 64, 81, 100])) / 10.0,
    "Interpretation C: If = [16,25,...,100]/100 = [0.16, 0.25, ..., 1.00] A":
        np.array([16, 25, 36, 49, 64, 81, 100]) / 100.0,
    "Interpretation D: If = [16,25,...,100]/1000 = [0.016, 0.025, ..., 0.100] A":
        np.array([16, 25, 36, 49, 64, 81, 100]) / 1000.0,
}

for name, If_values in interpretations.items():
    print(f"\n{'='*80}")
    print(f"{name}")
    print(f"{'='*80}")
    
    T = 900 + 1430 * If_values
    
    # Linear regression for each temperature
    intercepts = []
    for col in range(7):
        slope, intercept, r, _, _ = stats.linregress(sqrt_Ua, lg_Ia[:, col])
        intercepts.append(intercept)
    
    lg_I = np.array(intercepts)
    lg_I_over_T2 = lg_I - 2 * np.log10(T)
    inv_T = 1.0 / T
    
    slope_rich, intercept_rich, r_rich, _, _ = stats.linregress(inv_T, lg_I_over_T2)
    phi = -slope_rich * k_over_e * np.log(10)
    
    print(f"If values: {If_values}")
    print(f"T values: {T}")
    print(f"lg(I) intercepts: {lg_I}")
    print(f"Richardson plot slope: {slope_rich:.4f}")
    print(f"Richardson plot r: {r_rich:.6f}")
    print(f"Work function phi: {phi:.4f} eV")
    
    if phi > 0 and phi < 10:
        print(f"*** REASONABLE! Tungsten work function is typically ~4.5 eV ***")
