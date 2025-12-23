#!/bin/bash

set -e

# Cross-sectional NAVR figures
for group in "hc" "pd"; do
  for study in "baseline" "followup"; do
    metrics=(thickness area volume subcortical_volume)
    for metric in "${metrics[@]}"; do
      output_dir="navr/figures/${group}/${study}/${metric}"
      mkdir -p $output_dir
      cp notebooks/navr/csv_all/navr_${group}_${study}_${metric}.csv navr_${group}_${metric}_${study}.csv
      if [ "$metric" == "subcortical_volume" ]; then
        # add hemi_region column (maps 'lh'->'L', 'rh'->'R') and overwrite navr.csv
        arg="--subcortical-volume"
      else
        arg=""
      fi
      python3 ./container/ENIGMA/add_hemi_region.py navr_${group}_${metric}_${study}.csv --overwrite ${arg}
      ./container/ENIGMA/threshold_cohen_d.sh \
      --disorder_filename navr_${group}_${metric}_${study}.csv \
      --cohen_d_name NAVR \
      --vmin 0 \
      --vmax 1 \
      --livingpark_input navr_${group}_${metric}_${study}.csv \
      --disorder NAVR \
      --do-not-threshold \
      --threshold_name NAVR \
      --metric $metric \
      --cmap jet \
      --output_dir $output_dir
    done
  done
done

# Longitudinal NAVR figures
for group in "hc" "pd" ; do
  metrics=(thickness area volume subcortical_volume)
  for metric in "${metrics[@]}"; do
    output_dir="navr/figures_longitudinal/${group}/${metric}"
    mkdir -p $output_dir
    cp notebooks/navr/csv_all/navr_${group}_${metric}_longitudinal.csv navr_${group}_${metric}_longitudinal.csv
    if [ "$metric" == "subcortical_volume" ]; then
      # add hemi_region column (maps 'lh'->'L', 'rh'->'R') and overwrite navr.csv
      arg="--subcortical-volume"
    else
      arg=""
    fi
    python3 ./container/ENIGMA/add_hemi_region.py navr_${group}_${metric}_longitudinal.csv --overwrite ${arg}
    ./container/ENIGMA/threshold_cohen_d.sh \
    --disorder_filename navr_${group}_${metric}_longitudinal.csv \
    --cohen_d_name NAVR \
    --vmin 0 \
    --vmax 1 \
    --livingpark_input navr_${group}_${metric}_longitudinal.csv \
    --disorder NAVR \
    --do-not-threshold \
    --threshold_name NAVR \
    --metric $metric \
    --cmap jet \
    --output_dir $output_dir
  done
done
