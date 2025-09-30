import numpy as np
import matplotlib.pyplot as plt
import pyiast
import pandas as pd

# Load the data (assuming your CSV files are available)
df_ch4 = pd.read_csv("CH4_IRMOF1.csv")
df_co2 = pd.read_csv("CO2_IRMOF1.csv")

# Alternative: Try using Langmuir model fit for better extrapolation
# This often works better for IAST calculations
try:
    # Fit Langmuir model to CH4 data
    ch4_langmuir = pyiast.ModelIsotherm(df_ch4,
                                        loading_key="Loading(mmol/g)",
                                        pressure_key="Pressure(bar)",
                                        model="Langmuir")
    
    # Fit Langmuir model to CO2 data  
    co2_langmuir = pyiast.ModelIsotherm(df_co2,
                                        loading_key="Loading(mmol/g)",
                                        pressure_key="Pressure(bar)",
                                        model="Langmuir")
    
    print("Using Langmuir model fits for better extrapolation")
    ch4_isotherm = ch4_langmuir
    co2_isotherm = co2_langmuir
    
except Exception as e:
    print("Langmuir fit failed, using InterpolatorIsotherm with extrapolation")
    # Create isotherms using InterpolatorIsotherm with extrapolation enabled
    ch4_isotherm = pyiast.InterpolatorIsotherm(df_ch4,
                                        loading_key="Loading(mmol/g)",
                                        pressure_key="Pressure(bar)",
                                        fill_value=df_ch4["Loading(mmol/g)"].iloc[-1])

    co2_isotherm = pyiast.InterpolatorIsotherm(df_co2,
                                        loading_key="Loading(mmol/g)",
                                        pressure_key="Pressure(bar)",
                                        fill_value=df_co2["Loading(mmol/g)"].iloc[-1])

# First, let's check the pressure ranges of our data
print("CH4 pressure range:", df_ch4['Pressure(bar)'].min(), "to", df_ch4['Pressure(bar)'].max(), "bar")
print("CO2 pressure range:", df_co2['Pressure(bar)'].min(), "to", df_co2['Pressure(bar)'].max(), "bar")

# Show all pressure points to debug
print("\nAll CH4 pressures:", sorted(df_ch4['Pressure(bar)'].tolist()))
print("All CO2 pressures:", sorted(df_co2['Pressure(bar)'].tolist()))

# Use exactly the pressure range requested: 0.1 to 4.0 with 0.2 increments
pressures = np.arange(0.1, 4.1, 0.2)
print(f"Requested pressure range: 0.1 to 4.0 bar")
print(f"Generated pressure points: {len(pressures)} points from {pressures[0]:.1f} to {pressures[-1]:.1f}")

# Define molar fractions (0.5 for both components in binary mixture)
y_ch4 = 0.5  # Molar fraction of CH4 in gas phase
y_co2 = 0.5  # Molar fraction of CO2 in gas phase

# Initialize arrays to store results
ch4_loadings = []
co2_loadings = []
successful_pressures = []

# Calculate binary mixture isotherms using IAST
for P_total in pressures:
    try:
        # Calculate partial pressures
        P_ch4 = y_ch4 * P_total  # 0.5 * P_total
        P_co2 = y_co2 * P_total  # 0.5 * P_total
        
        print(f"Trying P_total = {P_total:.1f} bar (P_CH4 = {P_ch4:.1f}, P_CO2 = {P_co2:.1f})")
        
        # Try the IAST calculation - let pyIAST handle extrapolation if needed
        # Calculate mixture loadings using IAST
        partial_pressures = [P_ch4, P_co2]
        isotherms = [ch4_isotherm, co2_isotherm]
        
        # Use pyiast.iast to calculate mixture loadings
        q_mix = pyiast.iast(partial_pressures, isotherms, verboseflag=False)
        
        ch4_loadings.append(q_mix[0])  # CH4 loading
        co2_loadings.append(q_mix[1])  # CO2 loading
        successful_pressures.append(P_total)
        print(f"  ✓ Success: CH4 = {q_mix[0]:.3f}, CO2 = {q_mix[1]:.3f}")
            
    except Exception as e:
        print(f"  ✗ Error at pressure {P_total:.1f} bar: {str(e)[:150]}...")
        continue

# Update pressures to only include successful calculations
pressures = np.array(successful_pressures)

# Convert to numpy arrays for easier handling
ch4_loadings = np.array(ch4_loadings)
co2_loadings = np.array(co2_loadings)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(pressures, ch4_loadings, 'b-', marker='o', linewidth=2, markersize=6, label='CH₄')
plt.plot(pressures, co2_loadings, 'r-', marker='s', linewidth=2, markersize=6, label='CO₂')

plt.xlabel('Total Pressure (bar)', fontsize=12)
plt.ylabel('Loading (mmol/g)', fontsize=12)
plt.title('Binary Mixture Isotherms (CH₄/CO₂) in IRMOF-1\nMolar fractions: y_CH₄ = y_CO₂ = 0.5', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xlim(0, 4.2)
plt.ylim(0, max(max(ch4_loadings), max(co2_loadings)) * 1.1)

# Add some styling
plt.tight_layout()
plt.show()

# Print some results for verification
print("\nBinary Mixture Isotherm Results:")
print("="*50)
print(f"{'Pressure (bar)':<15} {'CH4 Loading':<15} {'CO2 Loading':<15}")
print("="*50)
for i in range(0, len(pressures), max(1, len(pressures)//8)):  # Print ~8 points
    print(f"{pressures[i]:<15.1f} {ch4_loadings[i]:<15.3f} {co2_loadings[i]:<15.3f}")
print("="*50)
print(f"Total data points calculated: {len(pressures)}")