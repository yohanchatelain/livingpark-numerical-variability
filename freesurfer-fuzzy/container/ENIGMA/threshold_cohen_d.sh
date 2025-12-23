#!/bin/bash

# Default values
DISORDER=""
DISORDER_FILENAME=""
COHEN_D_NAME="d_icv"
CMAP="RdBu_r"
VMIN="-0.5"
VMAX="0.5"
METRIC=""
LIVINGPARK_INPUT=""
OUTPUT_DIR="$(pwd)/cohen_d_map"
ENIGMA_DIR="$(pwd)/container/ENIGMA"
TITLE=""

# Default arguments
OUTPUT_DIR_ARG="--output_dir /output"

# Volume mount
OUTPUT_DIR_VOLUME="-v ${OUTPUT_DIR}:/output"



# Function to display help
show_help() {
    cat << EOF
Plot ENIGMA summary statistics.

Usage: $0 [OPTIONS]

Required arguments:
  --disorder DISORDER           Disorder to plot
  --metric METRIC              Metric to plot (choices: thickness, area, subcortical_volume)
  --livingpark_input PATH      Path to LivingPark summary statistics CSV file

Optional arguments:
  --disorder_filename PATH     Path to the disorder summary statistics CSV file
  --cohen_d_name NAME          Name of the column containing Cohen's d values (default: d_icv)
  --threshold_name NAME       Name of the column containing threshold values (default: Cohen_d)
  --do-not-threshold           Do not apply a threshold to the summary statistics
  --cmap COLORMAP             Colormap to use for plotting (default: RdBu_r)
  --vmin VALUE                Minimum value for the color scale (default: -0.5)
  --vmax VALUE                Maximum value for the color scale (default: 0.5)
  --output_dir DIR            Directory to save output plots and CSV files (default: ./enigma_map)
  --title TITLE               Title for the plot
  -h, --help                  Show this help message and exit

Examples:
  $0 --disorder depression --metric thickness --livingpark_input data.csv
  $0 --disorder schizophrenia --metric area --livingpark_input data.csv --output_dir ./results
EOF
}

# Function to validate metric choice
validate_metric() {
    local metric="$1"
    case "$metric" in
        thickness|area|volume|subcortical_volume)
            return 0
            ;;
        *)
            echo "Error: Invalid metric '$metric'. Choices are: thickness, area, volume, subcortical_volume" >&2
            return 1
            ;;
    esac
}

# Function to validate numeric value
validate_numeric() {
    local value="$1"
    local param_name="$2"

    if ! [[ "$value" =~ ^-?[0-9]*\.?[0-9]+$ ]]; then
        echo "Error: $param_name must be a numeric value, got '$value'" >&2
        return 1
    fi
    return 0
}

# Function to check if file exists
validate_file() {
    local file="$1"
    local param_name="$2"

    if [[ -n "$file" && ! -f "$file" ]]; then
        echo "Error: File specified for $param_name does not exist: $file" >&2
        return 1
    fi
    return 0
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --disorder)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --disorder requires a value" >&2
                    exit 1
                fi
                DISORDER="$2"
                DISORDER_ARG="--disorder $DISORDER"
                shift 2
                ;;
            --disorder_filename)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --disorder_filename requires a value" >&2
                    exit 1
                fi
                DISORDER_FILENAME="$2"
                DISORDER_FILENAME_BASENAME=$(basename "${DISORDER_FILENAME}")
                DISORDER_FILENAME_ARG="--disorder_filename /input/disorder/$DISORDER_FILENAME_BASENAME"
                DIRNAME_INPUT=$(dirname "${DISORDER_FILENAME}")
                DIRNAME_INPUT_PATH=$(realpath ${DIRNAME_INPUT})
                DISORDER_FILENAME_DIR_VOLUME="-v ${DIRNAME_INPUT_PATH}:/input/disorder/"
                shift 2
                ;;
            --cohen_d_name)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --cohen_d_name requires a value" >&2
                    exit 1
                fi
                COHEN_D_NAME="$2"
                COHEN_D_NAME_ARG="--cohen_d_name $COHEN_D_NAME"
                shift 2
                ;;
            --threshold_name)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --threshold_name requires a value" >&2
                    exit 1
                fi
                THRESHOLD_NAME="$2"
                THRESHOLD_NAME_ARG="--threshold_name $THRESHOLD_NAME"
                shift 2
                ;;
            --do-not-threshold)
                DO_NOT_THRESHOLD="--do-not-threshold"
                DO_NOT_THRESHOLD_ARG="--do-not-threshold"
                shift 1
                ;;
            --cmap)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --cmap requires a value" >&2
                    exit 1
                fi
                CMAP="$2"
                CMAP_ARG="--cmap $CMAP"
                shift 2
                ;;
            --vmin)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --vmin requires a value" >&2
                    exit 1
                fi
                if ! validate_numeric "$2" "--vmin"; then
                    exit 1
                fi
                VMIN="$2"
                VMIN_ARG="--vmin $VMIN"
                shift 2
                ;;
            --vmax)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --vmax requires a value" >&2
                    exit 1
                fi
                if ! validate_numeric "$2" "--vmax"; then
                    exit 1
                fi
                VMAX="$2"
                VMAX_ARG="--vmax $VMAX"
                shift 2
                ;;
            --metric)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --metric requires a value" >&2
                    exit 1
                fi
                if ! validate_metric "$2"; then
                    exit 1
                fi
                METRIC="$2"
                METRIC_ARG="--metric $METRIC"
                shift 2
                ;;
            --livingpark_input)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --livingpark_input requires a value" >&2
                    exit 1
                fi
                LIVINGPARK_INPUT="$2"
                LIVINGPARK_INPUT_BASENAME=$(basename "${LIVINGPARK_INPUT}")
                LIVINGPARK_INPUT_ARG="--livingpark_input /input/livingpark/$LIVINGPARK_INPUT_BASENAME"
                DIRNAME_INPUT=$(dirname "${LIVINGPARK_INPUT}")
                DIRNAME_INPUT_PATH=$(realpath ${DIRNAME_INPUT})
                LIVINGPARK_INPUT_DIR_VOLUME="-v ${DIRNAME_INPUT_PATH}:/input/livingpark/"
                shift 2
                ;;
            --output_dir)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --output_dir requires a value" >&2
                    exit 1
                fi
                OUTPUT_DIR="$2"
                OUTPUT_DIR_ARG="--output_dir output/"
                OUTPUT_DIR_VOLUME="-v $(realpath ${OUTPUT_DIR}):/output"
                shift 2
                ;;
            --title)
                if [[ -z "$2" || "$2" == --* ]]; then
                    echo "Error: --title requires a value" >&2
                    exit 1
                fi
                TITLE="$2"
                TITLE_ARG="--title $TITLE"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Error: Unknown option '$1'" >&2
                echo "Use --help for usage information." >&2
                exit 1
                ;;
        esac
    done
}

# Function to validate all arguments after parsing
validate_args() {
    local errors=0

    # Check required arguments
    if [[ -z "$DISORDER" ]]; then
        echo "Error: --disorder is required" >&2
        errors=1
    fi

    if [[ -z "$METRIC" ]]; then
        echo "Error: --metric is required" >&2
        errors=1
    fi

    if [[ -z "$LIVINGPARK_INPUT" ]]; then
        echo "Error: --livingpark_input is required" >&2
        errors=1
    fi

    # Validate file paths
    if ! validate_file "$LIVINGPARK_INPUT" "--livingpark_input"; then
        errors=1
    fi

    if ! validate_file "$DISORDER_FILENAME" "--disorder_filename"; then
        errors=1
    fi

    # Create output directory if it doesn't exist
    if [[ ! -d "$OUTPUT_DIR" ]]; then
        if ! mkdir -p "$OUTPUT_DIR" 2>/dev/null; then
            echo "Error: Cannot create output directory: $OUTPUT_DIR" >&2
            errors=1
        fi
    fi

    if [[ $errors -eq 1 ]]; then
        echo "Use --help for usage information." >&2
        exit 1
    fi
}

# Function to display parsed arguments (for debugging)
show_parsed_args() {
    echo "Parsed arguments:"
    echo "  DISORDER: $DISORDER"
    echo "  DISORDER_FILENAME: $DISORDER_FILENAME"
    echo "  COHEN_D_NAME: $COHEN_D_NAME"
    echo "  THRESHOLD_NAME: $THRESHOLD_NAME"
    echo "  DO_NOT_THRESHOLD: $DO_NOT_THRESHOLD"
    echo "  CMAP: $CMAP"
    echo "  VMIN: $VMIN"
    echo "  VMAX: $VMAX"
    echo "  METRIC: $METRIC"
    echo "  LIVINGPARK_INPUT: $LIVINGPARK_INPUT"
    echo "  OUTPUT_DIR: $OUTPUT_DIR"
    echo "  TITLE: $TITLE"
}

# Main function to parse and validate arguments
parse_and_check_args() {
    parse_args "$@"
    validate_args
}

# Example usage function
main() {
    parse_and_check_args "$@"

    # Uncomment to see parsed arguments
    # show_parsed_args

    # Your main script logic would go here
    echo "Running ENIGMA analysis with:"
    echo "  Disorder: $DISORDER"
    echo "  Metric: $METRIC"
    echo "  Input: $LIVINGPARK_INPUT"
    echo "  Output: $OUTPUT_DIR"
    if [[ -n "$COHEN_D_NAME" ]]; then
        echo "  Cohen's d name: $COHEN_D_NAME"
    fi
    if [[ -n "$DISORDER_FILENAME" ]]; then
        echo "  Disorder filename: $DISORDER_FILENAME"
    fi
    if [[ -n "$TITLE" ]]; then
        echo "  Title: $TITLE"
    fi
    echo "  Colormap: $CMAP"
    echo "  VMin: $VMIN"
    echo "  VMax: $VMAX"

    docker run --rm -it \
        -v ${ENIGMA_DIR}:/opt/ENIGMA \
        ${OUTPUT_DIR_VOLUME} \
        ${DISORDER_FILENAME_DIR_VOLUME} \
        ${LIVINGPARK_INPUT_DIR_VOLUME} \
        enigma:latest \
        python3 /opt/ENIGMA/plot.py \
        ${DISORDER_ARG} \
        ${DISORDER_FILENAME_ARG} \
        ${COHEN_D_NAME_ARG} \
        ${THRESHOLD_NAME_ARG} \
        ${DO_NOT_THRESHOLD_ARG} \
        ${CMAP_ARG} \
        ${VMIN_ARG} \
        ${VMAX_ARG} \
        ${METRIC_ARG} \
        ${LIVINGPARK_INPUT_ARG} \
        ${OUTPUT_DIR_ARG} \
        ${TITLE_ARG}
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
