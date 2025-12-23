import display

from enigmatoolbox.datasets import load_summary_stats

# Load summary statistics for ENIGMA-Epilepsy
sum_stats = load_summary_stats("epilepsy")

# Get case-control subcortical volume and cortical thickness tables
SV = sum_stats["SubVol_case_vs_controls_ltle"]
CT = sum_stats["CortThick_case_vs_controls_ltle"]

# Extract Cohen's d values
SV_d = SV["d_icv"]
CT_d = CT["d_icv"]

print("Cohen's d values for cortical thickness (case vs controls):")
print(CT)
print("\nCohen's d values for subcortical volume (case vs controls):")
print(SV)

print("Column names for cortical thickness:")
print(CT.columns.tolist())
print("Column names for subcortical volume:")
print(SV.columns.tolist())

print("Cohen's d values for cortical thickness (case vs controls):")
print(CT_d)
print("\nCohen's d values for subcortical volume (case vs controls):")
print(SV_d)
print("\nSummary statistics loaded successfully.")
# The code above loads the summary statistics for the ENIGMA-Epilepsy dataset.

# Visualize the Cohen's d values
from enigmatoolbox.utils.parcellation import parcel_to_surface
from enigmatoolbox.plotting import plot_cortical

# Map parcellated data to the surface
CT_d_fsa5 = parcel_to_surface(CT_d, "aparc_fsa5")

# Set up virtual display
display.launch_display()

print("Visualizing cortical thickness data...")
# Project the results on the surface brain
plot_cortical(
    array_name=CT_d_fsa5,
    surface_name="fsa5",
    size=(800, 400),
    cmap="RdBu_r",
    color_bar=True,
    color_range=(-0.5, 0.5),
    filename="ct_d_fsa5.png",
    screenshot=True,
)

# Visualize the subcortical volume data
print("Visualizing subcortical volume data...")
from enigmatoolbox.plotting import plot_subcortical

# Project the results on the surface brain
plot_subcortical(
    array_name=SV_d,
    size=(800, 400),
    cmap="RdBu_r",
    color_bar=True,
    color_range=(-0.5, 0.5),
    filename="sv_d.png",
    screenshot=True,
)
