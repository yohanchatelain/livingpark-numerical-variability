import pandas as pd
import numpy as np
from pathlib import Path
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap


from enigmatoolbox.datasets import load_summary_stats
from enigmatoolbox.utils.parcellation import parcel_to_surface
from enigmatoolbox.plotting import plot_cortical
from enigmatoolbox.plotting import plot_subcortical

import display
from parser import LivingParkParser, ENIGMAParser, GeneralParser, assert_ordered_regions


def threshold_summary_stats(enigma_data, livingpark_data, metric, cohen_d_name):
    """
    Threshold summary statistics based on a p-value threshold.

    Parameters:
    - data: DataFrame containing the summary statistics.
    - threshold: p-value threshold for significance.

    Returns:
    - DataFrame with significant results.
    """
    livingpark_data["NAVR_corrected"] = (
        2 / np.sqrt(enigma_data["population_size"])
    ) * livingpark_data["NAVR"]
    merged_data = pd.merge(
        enigma_data,
        livingpark_data,
        on=["Structure"],
        how="inner",
        suffixes=("_input", "_livingpark"),
    ).rename(columns={"population_size_input": "population_size"})
    merged_data[f"{cohen_d_name}_thresholded"] = np.where(
        merged_data["NAVR_corrected"] >= merged_data[cohen_d_name].abs(),
        np.nan,
        merged_data[cohen_d_name],
    )

    return merged_data


def plot_summary_stats(
    data,
    metric,
    filename,
    cmap="RdBu_r",
    vmin=-0.5,
    vmax=0.5,
    subcortical=False,
    title=None,
    threshold=None,
):
    """
    Plot summary statistics.

    Parameters:
    - data: DataFrame containing the summary statistics.
    - metric: Metric to plot.
    - title: Title of the plot.
    """
    nan_color = (0.15, 0.15, 0.20, 1)
    scale = (4, 4)
    print(f"Plotting {metric} with vmin={vmin}, vmax={vmax}")
    if subcortical:
        plot_subcortical(
            array_name=data[metric],
            size=(800, 400),
            cmap=cmap,
            color_bar=False,
            color_range=(vmin, vmax),
            nan_color=nan_color,  # White for NaN values
            filename=filename,
            screenshot=True,
            scale=scale,
        )
    else:
        surface = parcel_to_surface(data[metric], "aparc_fsa5")
        plot_cortical(
            array_name=surface,
            surface_name="fsa5",
            size=(800, 400),
            cmap=cmap,
            color_bar=False,
            color_range=(vmin, vmax),
            nan_color=nan_color,  # White for NaN values
            filename=filename,
            screenshot=True,
            label_text={"top": ["", "", "", ""]},
            scale=scale,
        )
    print(f"Plot saved to {filename}")


def save_thresholded_summary_stats(data, metric, filename, cohen_d_name):
    """
    Save thresholded summary statistics to a CSV file.

    Parameters:
    - data: DataFrame containing the thresholded summary statistics.
    - filename: Name of the file to save the data.
    """
    data_thresholded = data[data[metric].isna()]
    print(f"Thresholded summary statistics for {metric}:")

    columns_to_keep = [
        "Structure",
        metric,
        "NAVR_corrected",
        cohen_d_name,
        "population_size",
    ]
    if "fdr_p" in data.columns:
        columns_to_keep.append("fdr_p")
    print(data_thresholded[columns_to_keep])

    data.to_csv(filename, index=False)
    print(f"Thresholded summary statistics saved to {filename}")


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Plot ENIGMA summary statistics.")
    parser.add_argument(
        "--disorder",
        type=str,
        required=True,
        help="Disorder to plot.",
    )
    parser.add_argument(
        "--disorder_filename",
        type=str,
        required=False,
        help="Path to the disorder summary statistics CSV file.",
    )
    parser.add_argument(
        "--cohen_d_name",
        type=str,
        default="d_icv",
        help="Name of the column containing Cohen's d values.",
    )
    parser.add_argument(
        "--threshold_name",
        type=str,
        default="Cohen_d",
        help="Name of the column containing threshold values",
    )
    parser.add_argument(
        "--do-not-threshold",
        action="store_true",
        help="Whether to apply a threshold to the summary statistics.",
    )
    parser.add_argument(
        "--cmap",
        type=str,
        default="RdBu_r",
        help="Colormap to use for plotting.",
    )
    parser.add_argument(
        "--vmin",
        type=float,
        default=-0.5,
        help="Minimum value for the color scale.",
    )
    parser.add_argument(
        "--vmax",
        type=float,
        default=0.5,
        help="Maximum value for the color scale.",
    )
    parser.add_argument(
        "--metric",
        type=str,
        required=True,
        choices=["thickness", "area", "volume", "subcortical_volume"],
        help="Metric to plot.",
    )
    parser.add_argument(
        "--livingpark_input",
        type=str,
        required=True,
        help="Path to LivingPark summary statistics CSV file.",
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="Name of the output file for the plot.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=Path.cwd() / "enigma_map",
        help="Directory to save output plots and CSV files.",
    )
    parser.add_argument("--title", type=str, default=None, help="Title for the plot.")

    return parse_and_check_args(parser)


def parse_and_check_args(parser):
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    disorder = args.disorder
    disorder_filename = args.disorder_filename
    metric = args.metric
    cohen_d_name = args.cohen_d_name
    subcortical = args.metric == "subcortical_volume"
    livingpark_input = args.livingpark_input
    title = args.title
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if disorder_filename:
        # Load General summary statistics from the specified file
        general_parser = GeneralParser(
            disorder=disorder,
            metric=metric,
            filename=disorder_filename,
            threshold_name=args.threshold_name,
        )
        enigma_data = general_parser.load_summary_stats()
        print(f"Loaded data from {disorder_filename} with metric {metric}")
    elif disorder:
        # Load ENIGMA summary statistics for the specified disorder
        enigma_parser = ENIGMAParser(
            disorder=disorder,
            metric=metric,
            cohen_d_name=cohen_d_name,
        )
        enigma_data = enigma_parser.load_summary_stats()
        if not enigma_data:
            print(f"No data found for disorder {disorder} with metric {metric}.")
            return
        print(f"Loaded ENIGMA data for {disorder} with metric {metric}")

    # Load LivingPark summary statistics
    livingpark_parser = LivingParkParser(
        filename=livingpark_input,
    )
    livingpark_data = livingpark_parser.load_summary_stats(subcortical=subcortical)
    print(f"Loaded LivingPark data from {livingpark_input}")

    # Set up virtual display
    display.launch_display()

    for subgroup, data in zip(enigma_data["subgroup"], enigma_data["statistics"]):
        print(f"Processing subgroup: {subgroup}")
        png_dir = output_dir / disorder / "png"
        os.makedirs(png_dir, exist_ok=True)

        # Plotting summary statistics
        print(f"Plotting summary statistics for {disorder}, {metric}, {subgroup}")
        filename = png_dir / f"{disorder}_{metric}_{subgroup}.png"
        assert_ordered_regions(data, subcortical=subcortical)
        plot_summary_stats(
            data,
            metric=f"{cohen_d_name}",
            filename=str(filename.resolve()),
            vmin=args.vmin,
            vmax=args.vmax,
            cmap=args.cmap,
            subcortical=subcortical,
            title=title,
        )
        if args.do_not_threshold is None or not args.do_not_threshold:
            # Plotting thresholded summary statistics
            print(
                f"Plotting thresholded summary statistics for {disorder}, {metric}, {subgroup}"
            )
            thresholded_data = threshold_summary_stats(
                data, livingpark_data, metric, cohen_d_name
            )
            filename = png_dir / f"{disorder}_{metric}_{subgroup}_thresholded.png"
            assert_ordered_regions(thresholded_data, subcortical=subcortical)
            plot_summary_stats(
                thresholded_data,
                metric=f"{cohen_d_name}_thresholded",
                filename=str(filename.resolve()),
                subcortical=subcortical,
                vmin=args.vmin,
                vmax=args.vmax,
                cmap=args.cmap,
                title=title,
                threshold=True,
            )

            csv_dir = output_dir / disorder / "csv"
            os.makedirs(csv_dir, exist_ok=True)
            # Save thresholded summary statistics to CSV
            filename = csv_dir / f"{disorder}_{metric}_{subgroup}_thresholded.csv"
            save_thresholded_summary_stats(
                thresholded_data,
                metric=f"{cohen_d_name}_thresholded",
                filename=str(filename.resolve()),
                cohen_d_name=cohen_d_name,
            )


if __name__ == "__main__":
    main()
