import pandas as pd
from pandas.api import types as ptypes

from enigmatoolbox.datasets import load_summary_stats

subcortical_regions_template = [
    "Left-Thalamus",
    "Left-Caudate",
    "Left-Putamen",
    "Left-Pallidum",
    "Left-Hippocampus",
    "Left-Amygdala",
    "Left-Accumbens-area",
    "Left-Lateral-Ventricle",
    "Right-Thalamus",
    "Right-Caudate",
    "Right-Putamen",
    "Right-Pallidum",
    "Right-Hippocampus",
    "Right-Amygdala",
    "Right-Accumbens-area",
    "Right-Lateral-Ventricle",
]


cortical_regions_template = [
    "bankssts",
    "caudalanteriorcingulate",
    "caudalmiddlefrontal",
    "cuneus",
    "entorhinal",
    "fusiform",
    "inferiorparietal",
    "inferiortemporal",
    "isthmuscingulate",
    "lateraloccipital",
    "lateralorbitofrontal",
    "lingual",
    "medialorbitofrontal",
    "middletemporal",
    "parahippocampal",
    "paracentral",
    "parsopercularis",
    "parsorbitalis",
    "parstriangularis",
    "pericalcarine",
    "postcentral",
    "posteriorcingulate",
    "precentral",
    "precuneus",
    "rostralanteriorcingulate",
    "rostralmiddlefrontal",
    "superiorfrontal",
    "superiorparietal",
    "superiortemporal",
    "supramarginal",
    "frontalpole",
    "temporalpole",
    "transversetemporal",
    "insula",
]


plain_to_enigma_subcortical_regions = {
    "Left-Accumbens": "Laccumb",
    "Left-Accumbens-area": "Laccumb",
    "Left-Amygdala": "Lamyg",
    "Left-Caudate": "Lcaud",
    "Left-Hippocampus": "Lhippo",
    "Left-Pallidum": "Lpal",
    "Left-Putamen": "Lput",
    "Left-Thalamus": "Lthal",
    "Left-Lateral-Ventricle": "LLatVent",
    "Right-Accumbens": "Raccumb",
    "Right-Accumbens-area": "Raccumb",
    "Right-Amygdala": "Ramyg",
    "Right-Caudate": "Rcaud",
    "Right-Hippocampus": "Rhippo",
    "Right-Pallidum": "Rpal",
    "Right-Putamen": "Rput",
    "Right-Thalamus": "Rthal",
    "Right-Lateral-Ventricle": "RLatVent",
}

# ENIGMA subcortical regions
# Order is important for plotting
enigma_subcortical_regions = [
    "Laccumb",
    "Lamyg",
    "Lcaud",
    "Lhippo",
    "Lpal",
    "Lput",
    "Lthal",
    "LLatVent",
    "Raccumb",
    "Ramyg",
    "Rcaud",
    "Rhippo",
    "Rpal",
    "Rput",
    "Rthal",
    "RLatVent",
]

# ENIGMA cortical regions
# Order is important for plotting
enigma_cortical_regions = [
    "L_bankssts",
    "R_bankssts",
    "L_caudalanteriorcingulate",
    "R_caudalanteriorcingulate",
    "L_caudalmiddlefrontal",
    "R_caudalmiddlefrontal",
    "L_cuneus",
    "R_cuneus",
    "L_entorhinal",
    "R_entorhinal",
    "L_fusiform",
    "R_fusiform",
    "L_inferiorparietal",
    "R_inferiorparietal",
    "L_inferiortemporal",
    "R_inferiortemporal",
    "L_isthmuscingulate",
    "R_isthmuscingulate",
    "L_lateraloccipital",
    "R_lateraloccipital",
    "L_lateralorbitofrontal",
    "R_lateralorbitofrontal",
    "L_lingual",
    "R_lingual",
    "L_medialorbitofrontal",
    "R_medialorbitofrontal",
    "L_middletemporal",
    "R_middletemporal",
    "L_parahippocampal",
    "R_parahippocampal",
    "L_paracentral",
    "R_paracentral",
    "L_parsopercularis",
    "R_parsopercularis",
    "L_parsorbitalis",
    "R_parsorbitalis",
    "L_parstriangularis",
    "R_parstriangularis",
    "L_pericalcarine",
    "R_pericalcarine",
    "L_postcentral",
    "R_postcentral",
    "L_posteriorcingulate",
    "R_posteriorcingulate",
    "L_precentral",
    "R_precentral",
    "L_precuneus",
    "R_precuneus",
    "L_rostralanteriorcingulate",
    "R_rostralanteriorcingulate",
    "L_rostralmiddlefrontal",
    "R_rostralmiddlefrontal",
    "L_superiorfrontal",
    "R_superiorfrontal",
    "L_superiorparietal",
    "R_superiorparietal",
    "L_superiortemporal",
    "R_superiortemporal",
    "L_supramarginal",
    "R_supramarginal",
    "L_frontalpole",
    "R_frontalpole",
    "L_temporalpole",
    "R_temporalpole",
    "L_transversetemporal",
    "R_transversetemporal",
    "L_insula",
    "R_insula",
]


class ENIGMAParser:

    _disorders = {
        "22q",
        "adhd",
        "asd",
        "bipolar",
        "depression",
        "epilepsy",
        "ocd",
        "schizophrenia",
    }
    _metrics = {"thickness", "area", "volume", "subcortical_volume"}
    _metric_to_column_mapping = {
        "22q": {
            "thickness": "CortThick_case_vs_controls",
            "area": "CortSurf_case_vs_controls",
            "subcortical_volume": "SubVol_case_vs_controls",
        },
        "adhd": {
            "thickness": "CortThick_case_vs_controls_adult",
            "area": "CortSurf_case_vs_controls_adult",
            "subcortical_volume": "SubVol_case_vs_controls_adult",
        },
        "asd": {
            "thickness": "CortThick_case_vs_controls_meta_analysis",
            "area": "CortSurf_case_vs_controls_meta_analysis",
            "subcortical_volume": "SubVol_case_vs_controls_meta_analysis",
        },
        "bipolar": {
            "thickness": "CortThick_case_vs_controls_adult",
            "area": "CortSurf_case_vs_controls_adult",
            "subcortical_volume": [
                "SubVol_case_vs_controls_typeI",
                "SubVol_case_vs_controls_typeII",
            ],
        },
        "epilepsy": {
            "thickness": [
                "CortThick_case_vs_controls_allepilepsy",
                "CortThick_case_vs_controls_gge",
                "CortThick_case_vs_controls_rtle",
                "CortThick_case_vs_controls_ltle",
                "CortThick_case_vs_controls_allotherepilepsy",
            ],
            "subcortical_volume": [
                "SubVol_case_vs_controls_allepilepsy",
                "SubVol_case_vs_controls_gge",  # idiopathic generalized epilepsies
                "SubVol_case_vs_controls_rtle",  # right MTLE with right hippocampal sclerosis
                "SubVol_case_vs_controls_ltle",  # left MTLE with left hippocampal sclerosis
                "SubVol_case_vs_controls_allotherepilepsy",
            ],
        },
        "depression": {
            "thickness": "CortThick_case_vs_controls_adult",
            "area": "CortSurf_case_vs_controls_adult",
            "subcortical_volume": "SubVol_case_vs_controls",
        },
        "ocd": {
            "thickness": "CortThick_case_vs_controls_adult",
            "area": "CortSurf_case_vs_controls_adult",
            "subcortical_volume": "SubVol_case_vs_controls_adult",
        },
        "schizophrenia": {
            "thickness": "CortThick_case_vs_controls",
            "area": "CortSurf_case_vs_controls",
            "subcortical_volume": "SubVol_case_vs_controls",
        },
    }

    # None indicates that the number of patients is provided in the article or not available.
    _number_of_patients = {
        "22q": {
            "thickness": {
                "all": {
                    "n": 386,
                    "article": "https://www.nature.com/articles/s41380-018-0078-5#Sec24",
                    "section": "Statistical analysis - 22q11DS vs. controls",
                }
            },
            "area": {
                "all": {
                    "n": 386,
                    "article": "https://www.nature.com/articles/s41380-018-0078-5#Sec24",
                    "section": "Statistical analysis - 22q11DS vs. controls",
                }
            },
        },
        "adhd": None,
        "asd": None,
        "bipolar": {
            "subcortical_volume": {
                "typeI": {
                    "name": "n_typeI",
                },
                "typeII": {
                    "name": "n_typeII",
                },
            }
        },
        "depression": None,
        "epilepsy": None,
        "ocd": None,
        "schizophrenia": {
            "subcortical_volume": {
                "all": {
                    "n": 2028,
                    "article": "https://www.nature.com/articles/mp201563#Tab1",
                    "section": "Abstract",
                },
            },
        },
    }

    # None indicates that the number of controls is provided in the article or not available.
    _number_of_controls = {
        "22q": {
            "thickness": {
                "all": {
                    "n": 315,
                    "article": "https://www.nature.com/articles/s41380-018-0078-5#Sec24",
                    "section": "Statistical analysis - 22q11DS vs. controls",
                }
            },
            "area": {
                "all": {
                    "n": 315,
                    "article": "https://www.nature.com/articles/s41380-018-0078-5#Sec24",
                    "section": "Statistical analysis - 22q11DS vs. controls",
                }
            },
        },
        "adhd": None,
        "asd": None,
        "bipolar": None,
        "depression": None,
        "epilepsy": None,
        "ocd": None,
        "schizophrenia": {
            "subcortical_volume": {
                "all": {
                    "n": 2540,
                    "article": "https://www.nature.com/articles/mp201563#Tab1",
                    "section": "Abstract",
                },
            },
        },
    }

    def _assert_disorder(self, disorder):
        if disorder not in self._disorders:
            raise ValueError(
                f"Disorder '{disorder}' is not supported. Supported disorders are: {self._disorders}"
            )
        return disorder

    def _assert_metric(self, metric):
        if metric not in self._metrics:
            raise ValueError(
                f"Metric '{metric}' is not supported. Supported metrics are: {self._metrics}"
            )
        return metric

    def __init__(self, disorder, metric, cohen_d_name):
        self.disorder = self._assert_disorder(disorder)
        self.metric = self._assert_metric(metric)
        self.cohen_d_name = cohen_d_name

    def get_subgroup_from_column_name(self, column_name):
        fields = column_name.split("case_vs_controls")[-1].split("_")[1:]
        return "_".join(fields) if fields else "all"

    def correct_patients_size(self, stats, subgroup, summary_stats):
        if self._number_of_patients.get(self.disorder, None) is None:
            return
        patients_description = (
            self._number_of_patients.get(self.disorder, {})
            .get(self.metric, {})
            .get(subgroup, {})
        )
        if "n_patients" not in stats.columns:
            print(
                f"n_patients not found in summary statistics {self.disorder} and {self.metric}"
            )
            if "name" in patients_description:
                print(
                    f"Renaming column {patients_description['name']} for number of patients "
                )
                stats.rename(
                    columns={patients_description["name"]: "n_patients"},
                    inplace=True,
                )
            else:
                raise ValueError(
                    f"Number of patients for {self.disorder} and {self.metric} is not defined."
                )
        elif stats["n_patients"].isnull().any():
            print(
                f"n_patients is null in summary statistics {self.disorder} and {self.metric}"
            )
            if "n" in patients_description:
                print(f"Setting number of patients to {patients_description['n']}")
                stats["n_patients"] = patients_description["n"]
            else:
                raise ValueError(
                    f"Number of patients for {self.disorder} and {self.metric} is not defined."
                )

    def correct_control_size(self, stats, subgroup, summary_stats):
        if self._number_of_controls.get(self.disorder, None) is None:
            return

        controls_description = (
            self._number_of_controls.get(self.disorder, {})
            .get(self.metric, {})
            .get(subgroup, {})
        )
        if "n_controls" not in stats.columns:
            print(
                f"n_controls not found in summary statistics {self.disorder} and {self.metric}"
            )
            if "name" in controls_description:
                print(
                    f"Renaming column {controls_description['name']} for number of controls "
                )
                stats.rename(
                    columns={controls_description["name"]: "n_controls"},
                    inplace=True,
                )
            else:
                raise ValueError(
                    f"Number of controls for {self.disorder} and {self.metric} is not defined."
                )
        elif stats["n_controls"].isnull().any():
            print(
                f"n_controls is null in summary statistics {self.disorder} and {self.metric}"
            )
            if "n" in controls_description:
                print(f"Setting number of controls to {controls_description['n']}")
                stats["n_controls"] = controls_description["n"]
            else:
                raise ValueError(
                    f"Number of controls for {self.disorder} and {self.metric} is not defined."
                )

    def correct_population_size(self, stats, subgroup, summary_stats):
        for stats, subgroup in zip(
            summary_stats["statistics"], summary_stats["subgroup"]
        ):
            self.correct_patients_size(stats, subgroup, summary_stats)
            self.correct_control_size(stats, subgroup, summary_stats)
            if ptypes.is_string_dtype(stats["n_patients"]):
                stats["n_patients"] = pd.to_numeric(
                    stats["n_patients"].str.replace(",", "").replace("_", "")
                )
            if ptypes.is_string_dtype(stats["n_controls"]):
                stats["n_controls"] = pd.to_numeric(
                    stats["n_controls"].str.replace(",", "").replace("_", "")
                )
            stats["population_size"] = stats["n_patients"] + stats["n_controls"]
            # assert population_size is not null or population_size is null and cohen_d is not null
            if (
                stats[
                    stats["population_size"].isnull()
                    & ~stats[self.cohen_d_name].isnull()
                ]
                .any()
                .any()
            ):
                raise ValueError(
                    f"Population size for {self.disorder} and {self.metric} is not defined."
                )

    def load_summary_stats(self):
        """
        Load ENIGMA summary statistics.

        Parameters:
        - subcortical: Boolean indicating whether to load subcortical regions.

        Returns:
        - DataFrame containing the summary statistics in ENIGMA format.
        """
        if self.metric not in self._metric_to_column_mapping[self.disorder]:
            return None

        summary_stats = {
            "disorder": self.disorder,
            "metric": self.metric,
            "subgroup": [],
            "statistics": [],
        }
        data = load_summary_stats(self.disorder)
        column_names = self._metric_to_column_mapping[self.disorder][self.metric]
        if not isinstance(column_names, list):
            column_names = [column_names]
        if isinstance(column_names, list):
            for col in column_names:
                if col not in data:
                    continue
                subgroup = self.get_subgroup_from_column_name(col)
                summary_stats["subgroup"].append(subgroup)
                summary_stats["statistics"].append(data[col])
        self.correct_population_size(
            summary_stats["statistics"], summary_stats["subgroup"], summary_stats
        )
        return summary_stats


class GeneralParser:
    """
    General parser for ENIGMA summary statistics.
    This class is a base class for specific parsers like ENIGMAParser and LivingParkParser.
    """

    def __init__(self, disorder, metric, filename, threshold_name):
        self.disorder = disorder
        self.metric = metric
        self.filename = filename
        self.threshold_name = threshold_name
        self.data = None

    def _assert_cortical_regions(self):
        regions_lateralized = enigma_cortical_regions
        regions = self.data["Structure"]
        regions_missing = set(regions_lateralized) - set(regions)
        if regions_missing:
            raise ValueError(f"Data is missing cortical regions: {regions_missing}")

    def _assert_subcortical_regions(self):
        regions = self.data["Structure"]
        if not regions.isin(enigma_subcortical_regions).all():
            regions_missing = set(enigma_subcortical_regions) - set(regions)
            raise ValueError(f"Data is missing subcortical regions: {regions_missing}")

    def _assert_data(self):
        if "Structure" not in self.data.columns:
            raise ValueError("Data must contain 'Structure' column.")
        if self.threshold_name not in self.data.columns:
            raise ValueError(f"Data must contain '{self.threshold_name}' column.")
        if (
            self.metric == "thickness"
            or self.metric == "area"
            or self.metric == "volume"
        ):
            self._assert_cortical_regions()
        elif self.metric == "subcortical_volume":
            self._assert_subcortical_regions()
        else:
            raise ValueError(
                f"Metric '{self.metric}' is not supported. Supported metrics are: 'thickness', 'area', 'subcortical_volume'."
            )

    def _get_subgroup(self, filename):
        """
        Extracts the subgroup from the filename.
        Assumes the filename contains the subgroup information in a specific format.
        """
        # Example filename format: disorder_metric_subgroup.csv
        parts = filename.split("_")
        if len(parts) < 3:
            return "all"
        return parts[-1].split(".")[0]

    def convert_region_to_enigma_format(self, data, subcortical=False):
        """
        Convert data to ENIGMA format.

        Parameters:
        - data: DataFrame containing the data to be converted.
        - subcortical: Boolean indicating whether the data is for subcortical regions.

        Returns:
        - DataFrame in ENIGMA format.
        """
        # Subcortical regions
        if subcortical and set(data["Structure"]) != set(enigma_subcortical_regions):
            data["Structure"] = data["Structure"].str.replace(" ", "-")
            if "Hemisphere" in data.columns:
                data["Hemisphere"] = data["Hemisphere"].apply(
                    lambda x: "Left" if x.lower().startswith("l") else "Right"
                )
                data["Structure"] = data["Hemisphere"] + "-" + data["Structure"]
            data["Structure"] = data["Structure"].apply(
                lambda x: plain_to_enigma_subcortical_regions.get(x, x)
            )
            data = data[data["Structure"].isin(enigma_subcortical_regions)]
            # sort the regions to match ENIGMA order
            data = (
                data.set_index("Structure")
                .reindex(enigma_subcortical_regions)
                .reset_index()
            )

        # Cortical regions
        elif set(data["Structure"]) != set(enigma_cortical_regions):
            if "Hemisphere" in data.columns:
                data["Structure"] = data[["Hemisphere", "Structure"]].apply(
                    lambda x: (
                        "L_" + x[1]
                        if "lh" in x[0]
                        else "R_" + x[1] if "rh" in x[0] else x[1]
                    ),
                    axis=1,
                )
            data = data[data["Structure"].isin(enigma_cortical_regions)]
            # sort the regions to match ENIGMA order
            data = (
                data.set_index("Structure")
                .reindex(enigma_cortical_regions)
                .reset_index()
            )
        return data

    def parse_csv(self, filename):
        """
        Parses the CSV file and returns a DataFrame.
        Assumes the CSV file has a specific format.
        """
        data = pd.read_csv(filename)
        if "Cohen_d" in data.columns:
            data.rename(columns={"Cohen_d": self.threshold_name}, inplace=True)
        elif "Cohen's d" in data.columns:
            data.rename(columns={"Cohen's d": self.threshold_name}, inplace=True)
        if self.metric == "subcortical_volume":
            data = self.convert_region_to_enigma_format(data, subcortical=True)
        else:
            data = self.convert_region_to_enigma_format(data, subcortical=False)
        if "population_size" not in data.columns:
            data["population_size"] = (
                data["n_patients"] + data["n_controls"]
                if "n_patients" in data.columns and "n_controls" in data.columns
                else None
            )
        return data

    def load_summary_stats(self):
        self.data = self.parse_csv(self.filename)
        self._assert_data()
        subgroup = self._get_subgroup(self.filename)
        summary_stats = {
            "disorder": self.disorder,
            "metric": self.metric,
            "subgroup": [subgroup],
            "statistics": [self.data],
        }

        return summary_stats


class LivingParkParser:

    _subcortical_regions_enigma_mapping = {
        "Left-Accumbens-area": "Laccumb",
        "Left-Amygdala": "Lamyg",
        "Left-Caudate": "Lcaud",
        "Left-Hippocampus": "Lhippo",
        "Left-Pallidum": "Lpal",
        "Left-Putamen": "Lput",
        "Left-Thalamus": "Lthal",
        "Left-Lateral-Ventricle": "LLatVent",
        "Right-Accumbens-area": "Raccumb",
        "Right-Amygdala": "Ramyg",
        "Right-Caudate": "Rcaud",
        "Right-Hippocampus": "Rhippo",
        "Right-Pallidum": "Rpal",
        "Right-Putamen": "Rput",
        "Right-Thalamus": "Rthal",
        "Right-Lateral-Ventricle": "RLatVent",
    }

    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def convert_region_to_enigma_format(self, data, subcortical=False):
        """
        Convert data to ENIGMA format.

        Parameters:
        - data: DataFrame containing the data to be converted.

        Returns:
        - DataFrame in ENIGMA format.
        """
        # Assuming 'data' is a pandas DataFrame
        # Prefix the region names with 'L' or 'R' for left and right hemispheres
        if subcortical:
            data = data[
                data["region"].isin(self._subcortical_regions_enigma_mapping.keys())
            ]
            data["region"] = data["region"].apply(
                lambda x: self._subcortical_regions_enigma_mapping.get(x, x)
            )
        else:
            data["region"] = data[["hemisphere", "region"]].apply(
                lambda x: (
                    "L_" + x[1]
                    if "lh" in x[0]
                    else "R_" + x[1] if "rh" in x[0] else x[1]
                ),
                axis=1,
            )
            data = data[data["region"].isin(enigma_cortical_regions)]
        if "Structure" not in data.columns:
            data = data.rename(columns={"region": "Structure"})
        if "region" in data.columns:
            assert (data[data["Structure"] == data["region"]]).all().all()
        return data

    def load_summary_stats(self, subcortical=False):
        """
        Load LivingPark summary statistics.

        Parameters:
        - subcortical: Boolean indicating whether to load subcortical regions.

        Returns:
        - DataFrame containing the summary statistics in LivingPark format.
        """
        # Placeholder for actual implementation
        data = pd.read_csv(self.filename)
        self.data = self.convert_region_to_enigma_format(data, subcortical=subcortical)
        return self.data


def assert_ordered_regions(data, subcortical=False):
    """
    Assert that the regions in the data are ordered according to ENIGMA standards.

    Parameters:
    - data: DataFrame containing the data to be checked.
    - subcortical: Boolean indicating whether the data is for subcortical regions.

    Raises:
    - ValueError: If the regions are not ordered correctly.
    """
    if subcortical:
        expected_order = enigma_subcortical_regions
    else:
        expected_order = enigma_cortical_regions

    actual_order = data["Structure"].tolist()
    if actual_order != expected_order:
        print("Expected order:", expected_order)
        print("Actual order:", actual_order)
        raise ValueError("Regions are not ordered according to ENIGMA standards.")
