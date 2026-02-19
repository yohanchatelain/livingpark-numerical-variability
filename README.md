# Repo layout

## Freesurfer-fuzzy

Contains fuzzy experiments with FreeSurfer 7.3.1.

### Cohort

Notebooks relative to cohort build.
- `cohort_builder.ipynb`: Build cross-sectional and longitudinal cohort from PPMI.
- `executions_stats_info.ipynb`: Gather information about run on VIP and filter out QC failures.

### Container

Dockerfile and Python scripts to reproduce NPVR maps with EnigmaToolBox.
- `ENIGMA/Dockerfile.enigma`: Docker file to build script environment.
- `ENIGMA/navr.sh`: Plot NPVR maps.
- `ENIGMA/threshold_cohen_d.sh`, `ENIGMA/threshold_cohen_d_all.sh`: Threshold Cohen's d maps.
- `ENIGMA/*.py`: Python scripts relative to plotting (`add_hemi_region.py`, `display.py`, `parser.py`, `plot.py`).

### Scripts

Scripts to run FreeSurfer on the VIP platform via the VIP API. See `scripts/README.md` for setup instructions (VIP API token, FreeSurfer license, dataset).
- `freesurfer-recon-all.sh`: Launch FreeSurfer recon-all on VIP server.
- `download.py`: Download VIP session outputs or list pipeline details.
- `generate_inputs_json.py`: Scan the inputs directory for NIfTI files and generate an `inputs.json` mapping subjects to file paths.
- `generate_input_settings.py`: Build the VIP pipeline input settings JSON from a prepared input data file.
- `run_pipeline.py`: Create a VIP session, optionally upload inputs, and launch the FreeSurfer pipeline.

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

Notebooks comparing formula and std sampling. Each subdirectory (`ancova`, `correlation`, `cohen_d`, `t_test`) contains one notebook per brain measure:
- `cortical_area.ipynb`, `cortical_thickness.ipynb`, `cortical_volume.ipynb`, `subcortical_volume.ipynb`

Additional notebook:
- `aggregated_relative_difference_boxplots.ipynb`: Aggregate and plot relative differences across all statistical tests and brain measures.

#### Papers data

Notebooks computing the numerical variability on findings from published articles.
- `parkinson`: A list of directories, one per article. Each article contains:
  - `consistency.ipynb`: A notebook that contains numerical variability computations.
  - `table*.csv`: Files that contain raw results from original article.
  - `uncertainty.csv`: Summary statistics of numerical variability computations.
- `alzheimer`: Same structure as `parkinson`, for Alzheimer's disease articles.
- `figure-PPMI.ipynb`: Plot numerical variability figures for PPMI-based results.
- `figure-distance.ipynb`, `figure-distance-histogram.ipynb`, `figure-distance-polar.ipynb`: Plot figures of numerical variability distances.
- `figure-entropy.ipynb`: Plot figures summarizing entropy of numerical variability.
