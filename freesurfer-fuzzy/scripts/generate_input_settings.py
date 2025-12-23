import json
import argparse

directives = "-all"
vip_license = "/vip/Home/freesurfer-license/license.txt"


"""
VipSession.show_pipeline('FreeSurfer-Recon-all-fuzzy/v7.3.1')
=================================
FreeSurfer-Recon-all-fuzzy/v7.3.1
======================================================================
NAME: FreeSurfer-Recon-all-fuzzy | VERSION: v7.3.1
----------------------------------------------------------------------
DESCRIPTION:
    Performs all, or any part of, the FreeSurfer cortical 
    reconstruction process 
    (https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all).
----------------------------------------------------------------------
INPUT_SETTINGS:
REQUIRED..............................................................
- directives
    [STRING] $esc.xml($input.getDescription())
- license
    [FILE] Valid license file needed to run FreeSurfer.
- nifti
    [FILE] Single NIFTI file from series.
- subjid
    [STRING] $esc.xml($input.getDescription())
OPTIONAL..............................................................
- 3T_flag
    [BOOLEAN] The -3T flag enables two specific options in recon-all 
    for images acquired with a 3T scanner:  3T-specific NU intensity 
    correction parameters are used in the Non-Uniform normalization 
    stage, and the Schwartz 3T atlas is used for Talairach alignment
- brainstem_structures_flag
    [BOOLEAN] Segmentation of brainstem structures.
- cw256_flag
    [BOOLEAN] Include this flag after -autorecon1 if images have a FOV
     > 256.
- hippocampal_subfields_T1_flag
    [BOOLEAN] Segmentation of hippocampal subfields using input T1 
    scan.
- mprage_flag
    [BOOLEAN] Assume scan parameters are MGH MP-RAGE protocol.
- no_wsgcaatlas_flag
    [BOOLEAN] Do not use GCA atlas when skull stripping.
- noskullstrip_flag
    [BOOLEAN] Exclude skull strip step.
- notal_flag
    [BOOLEAN] Skip the automatic failure detection of Talairach 
    alignment.
- qcache_flag
    [BOOLEAN] Produce the pre-cached files required by the Qdec 
    utility, allowing rapid analysis of group data.
======================================================================
"""


"""
input_settings = {
    "directives": "-all",  # Options
    "license": "path/to/my/license.txt",  # License
    "nifti": [  # List of inputs files :
        "path/to/my/input/file_1.nii.gz",  # Input file 1
        "path/to/my/input/file_2.nii.gz",  # Input file 2
        # [...]
        "path/to/my/input/file_n.nii.gz",  # Input file N
    ],  # End of list
    "subjid": [
        "subjid1",  # Subject ID 1
        "subjid2",  # Subject ID 2
        # [...]
        "subjidN",  # Subject ID N
    ]
    # [...]
}
"""


def replace_root_path(path):
    return path.replace(".cache/inputs", "/vip/Home/API/freesurfer-fuzzy/INPUTS")


def generate_input_settings(input_data):
    nifti_files = []
    subject_ids = []
    PATNO_id = input_data["PATNO_id"].keys()

    for patno in PATNO_id:
        subject_visit = input_data["PATNO_id"][patno]
        filename = replace_root_path(input_data["File name"][patno])
        subject_ids.append(subject_visit)
        nifti_files.append(filename)

    settings = {
        "directives": directives,
        "license": vip_license,
        "nifti": nifti_files,
        "subjid": subject_ids,
    }
    return settings


def dump_settings(output, settings):
    with open(output, "w") as f:
        json.dump(settings, f, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate input settings for a VIP pipeline"
    )
    parser.add_argument("--input-data", help="Input data JSON file", required=True)
    parser.add_argument("--output", help="Output settings file", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    input_data = json.load(open(args.input_data))
    settings = generate_input_settings(input_data)
    dump_settings(args.output, settings)


if __name__ == "__main__":
    main()