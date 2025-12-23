#!/bin/bash

set -e

function get_livingpark_input() {
  local metric="$1"
  if [[ "$metric" == "subcortical_volume" ]]; then
    echo "navr_subcortical_volume.csv"
  else
    echo "navr_cortical_${metric}.csv"
  fi
}

# # Plot ENIGMA results for all disorders and metrics
# disorders=("22q" "adhd" "asd" "bipolar" "depression" "epilepsy" "ocd" "schizophrenia")
# metrics=("thickness" "area" "subcortical_volume")
# for disorder in "${disorders[@]}"; do
#     for metric in "${metrics[@]}"; do
#         echo "Processing disorder: $disorder, metric: $metric"
#         LIVINGPARK_INPUT=$(get_livingpark_input "$metric")
#         ./container/ENIGMA/threshold_cohen_d.sh \
#         --disorder "$disorder" \
#         --metric "$metric" \
#         --livingpark_input "$PWD/cohen_d/csv/${LIVINGPARK_INPUT}" \
#         --output_dir "$PWD/cohen_d_map/enigma"
#         echo -e "\n"
#     done
# done

# # Plot Cohen's d for Hettwer et al. 2022
# INPUT_DIR="$PWD/container/ENIGMA/data/Hettwer_2022"
# disorders=("adhd" "asd" "bd" "mdd" "ocd" "scz")
# metrics=("thickness")
# for disorder in "${disorders[@]}"; do
#     for metric in "${metrics[@]}"; do
#         echo "Processing disorder: $disorder, metric: $metric"
#         LIVINGPARK_INPUT=$(get_livingpark_input "$metric")
#         DISORDER_FILENAME="${INPUT_DIR}/${disorder}_cohen_d.csv"
#         ./container/ENIGMA/threshold_cohen_d.sh \
#         --disorder "$disorder" \
#         --metric "$metric" \
#         --disorder_filename "$DISORDER_FILENAME" \
#         --livingpark_input "$PWD/cohen_d/csv/${LIVINGPARK_INPUT}" \
#         --cohen_d_name "Cohen_d" \
#         --vmin "-0.35" \
#         --vmax "0.35" \
#         --output_dir "$PWD/cohen_d_map/Hettwer_2022"
#         echo -e "\n"
#     done
# done

# Plot Cohen's d for Laansma et al. 2021
# INPUT_DIR="$PWD/container/ENIGMA/data/Laansma_2021"
# disorders=("parkinson")
# metrics=("thickness" "area" "subcortical_volume")
# for disorder in "${disorders[@]}"; do
#   for metric in "${metrics[@]}"; do
#     echo "Processing disorder: $disorder, metric: $metric"
#     LIVINGPARK_INPUT=$(get_livingpark_input "$metric")
#     DISORDER_FILENAMES="${INPUT_DIR}/${disorder}_${metric}_*.csv"
#     for DISORDER_FILENAME in $DISORDER_FILENAMES; do
#       echo "Using disorder filename: $DISORDER_FILENAME"
#       ./container/ENIGMA/threshold_cohen_d.sh \
#       --disorder "$disorder" \
#       --metric "$metric" \
#       --disorder_filename "$DISORDER_FILENAME" \
#       --livingpark_input "$PWD/cohen_d/csv/${LIVINGPARK_INPUT}" \
#       --cohen_d_name "Cohen_d" \
#       --vmin "-0.6" \
#       --vmax "0.6" \
#       --output_dir "$PWD/cohen_d_map/Laansma_2021"
#       echo -e "\n"
#     done
#   done
# done

# Plot Cohen's d for Gurholt et al. 2020
INPUT_DIR="$PWD/container/ENIGMA/data/Gurholt_2020"
disorders=("eop")
metrics=("subcortical_volume")
for disorder in "${disorders[@]}"; do
  for metric in "${metrics[@]}"; do
    echo "Processing disorder: $disorder, metric: $metric"
    LIVINGPARK_INPUT=$(get_livingpark_input "$metric")
    DISORDER_FILENAMES="${INPUT_DIR}/${disorder}_${metric}_*.csv"
    for DISORDER_FILENAME in $DISORDER_FILENAMES; do
      echo "Using disorder filename: $DISORDER_FILENAME"
      ./container/ENIGMA/threshold_cohen_d.sh \
      --disorder "$disorder" \
      --metric "$metric" \
      --disorder_filename "$DISORDER_FILENAME" \
      --livingpark_input "$PWD/cohen_d/csv/${LIVINGPARK_INPUT}" \
      --cohen_d_name "Cohen_d" \
      --vmin "-0.4" \
      --vmax "0.4" \
      --output_dir "$PWD/cohen_d_map/Gurholt_2020"
      echo -e "\n"
    done
  done
done
