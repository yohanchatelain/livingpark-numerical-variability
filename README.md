# Repo layout

## Freesurfer-fuzzy

Contains fuzzy experiments with FreeSurfer 7.3.1.

### Cohort

Notebooks relative to cohort build.
- `cohort_builder.ipynb`: Build cross-sectional and longitudinal cohort from PPMI.
- `execution_stats_info.ipynb`: Gather information about run on VIP and filter out QC failures.

### Container

Dockerfile and Python scritps to reproduce NVPR maps with EnigmaToolBox.
- `Dockerfile.enigma`: Docker file to build script environment.
- `navr.sh`: Plot NPVR maps.
- `*.py`: Python scripts relative to plotting.

### Notebooks

#### Cross-sectional

Notebooks relative to cross-sectional analysis.
- `cross-sectional-fuzzy.ipynb`: Gather aseg+aparc statistics across MCA repetitions in parquet table.
- `cross-sectional-ieee.ipynb`: Gather aseg+aparc statistics for the IEEE repetition in parquet table.

#### Longitudinal

Notebooks relative to longitudinal analysis.
- `baseline-ancova.ipynb`: Compute ANCOVA at baseline between HC and PD across MCA repetitions.
- `baseline-partial-correlation.ipynb`: Compute partial correlation at baseline between PD and UPDRS-III score across MCA repetitions.
- `longitudinal-ancova.ipynb`: Compute ANCOVA between HC and PD longitudinally across MCA repetitions.
- `longitudinal-partial-correlation.ipynb`: Compute partial correlation between PD and UPDRS-III score longitudinally for MCA repetitions.
- `ieee/baseline-ancova.ipynb`: Compute ANCOVA at baseline between HC and PD for IEEE repetition.
- `ieee/baseline-partial-correlation.ipynb`: Compute partial correlation at baseline between PD and UPDRS-III score for IEEE repetition.
- `ieee/longitudinal-ancova.ipynb`: Compute ANCOVA between HC and PD longitudinally for IEEE repetition.
- `ieee/longitudinal-partial-correlation.ipynb`: Compute partial correlation between PD and UPDRS-III score longitudinally for IEEE repetition.
  
Notebooks to plot longitudinal analysis:
- `plot/plot-cortical_area.ipynb`: Plot cortical surface area.
- `plot/plot-cortical_thickness.ipynb`: Plot cortical thickness.
- `plot/plot-cortical_volume.ipynb`: Plot cortical volumes.
- `plot/plot-subcortical_volume.ipynb`: Plot subcortical volumes

#### Inconsistency

Notebooks relative to inconsistency plots measuring proportion of flipped significance in longitudinal analysis.
- `inconsistency_p-value.ipynb`: Statistics about flipped significance of p-value.
- `variance_comparison.ipynb`: Ansari-Bradley statistical test to compare baseline vs longitudinal variances.

#### NPVR

Notebooks relative NPVR maps.
- `cortical_area.ipynb`: Plot NPVR maps for cortical surface area.
- `cortical_thickness.ipynb`: Plot NPVR maps for cortical thickness.
- `cortical_volume.ipynb`: Plot NPVR maps for cortical volumes.
- `subcortical_volume.ipynb`: Plot NPVR maps for subcortical volumes.
- `statistics.ipynb`: Statistics about NPVR maps and bootstrap comparison of mean between HC and PD NPVRs.

#### Numerical validation

Notebooks comparing formula and std sampling.
- `ancova`: ANCOVA
- `correlation`: Partial-correlation
- `cohen_d`: Cohen's d
- `t_test`: Two-sample t-test

#### Papers data

Notebooks computing the numerical variability on finding from published articles.
- `parkinson`: A list of directories, one per article. Each article contains:
  - `consistency.ipynb`: A notebook that contains numerical variability computations.
  - `table*.csv`: Files that contain raw results from original article.
  - `uncertainty.csv`: Summary statistics of numerical variability computations.
- `figure-*.ipynb`: Plot figures summarizing numerical-induced misclassifications.