import argparse
import glob
import os
import json


def check_inputs(paths):
    """
    check that nifti images name are unique
    """
    names = [os.path.split(path)[1] for path in paths]
    assert len(paths) == set(names)
    for path in paths:
        fields = os.path.split(path)
        assert "anat" in fields


def get_fields(input_path):
    """
    inputs/sub-3857/ses-BL/anat/PPMI_3857_MR_MPRAGE_GRAPPA_br_raw_20131021151217013_168_S204398_I395284.nii
    """
    fields = input_path.split(os.path.sep)
    subject = fields[1]
    session = fields[2]
    image = fields[4]
    return {"subject": subject, "session": session, "image": image}


def get_inputs_files(inputs_path):
    regexp = os.path.join(inputs_path, "**", "*.nii")
    files = glob.glob(regexp, recursive=True)
    return files


def create_inputs_file(inputs_files, output, check=False):
    subjid = {}
    paths = {}
    for i, path in enumerate(inputs_files):
        fields = get_fields(path)
        subjid[i] = "_".join((fields["subject"], fields["session"]))
        paths[i] = path

    if check:
        check_inputs(paths)

    obj = {"subjid": subjid, "nifti": paths}
    with open(output, "w", encoding="utf-8") as fo:
        json.dump(obj, fo)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="inputs", action="store_true", help="inputs directory"
    )
    parser.add_argument("--output", default="inputs.json", help="JSON output file")
    parser.add_argument("--check", action="store_true", help="Sanity check inputs")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    inputs_file = get_inputs_files(args.input)
    create_inputs_file(inputs_file, args.output)


if "__main__" == __name__:
    main()