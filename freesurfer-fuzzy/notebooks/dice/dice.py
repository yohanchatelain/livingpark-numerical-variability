import glob
import os
import numpy as np
import nibabel
import joblib
import numpy as np
import argparse
import pandas as pd
from tqdm import tqdm

profile = False
progress_bar = True


# Read annotation file
def read_annot(annot_file):
    # Read annotation file
    # labels: Annotation id for each vertex
    # ctab: RGBT + label id for each label
    # names: label names
    (labels, ctab, names) = nibabel.freesurfer.read_annot(annot_file)
    return (labels, ctab, names)


# Read segmentation file
def read_seg(seg_file):
    # Read segmentation file
    # data: segmentation data
    # affine: affine transformation matrix
    # header: header information
    return nibabel.load(seg_file).get_fdata().ravel().astype(np.int16)


def time_stamp(label):
    if not profile:
        return

    import time

    return time.strftime(f"[{label}] %Y-%m-%d %H:%M:%S", time.gmtime())


def time_stamp_start(label):
    if not profile:
        return
    print(time_stamp(f"START {label}"))


def time_stamp_end(label):
    if not profile:
        return
    print(time_stamp(f" END  {label}"))


def compute_dice_N_gpu(segs, label, divide=10):
    import cupy as cp

    time_stamp_start("compute_dice_N_gpu")

    print("=== label === ", label)
    print("segs.shape", segs.shape)
    n = segs.shape[0]

    if divide > 1:
        # divide the data into chunks
        segs_chunks = np.array_split(segs, divide)

        time_stamp_start("init")
        cards = 0
        intersection = cp.ones(segs.shape[1], dtype=np.bool_)
        time_stamp_end("init")

        for i, segs_chunk in enumerate(segs_chunks):
            time_stamp_start(f"chunk {i}")

            time_stamp_start(f"to_gpu {i}")
            seg = cp.asarray(segs_chunk)
            time_stamp_end(f"to_gpu {i}")

            # Compute the intersection of all segmentations
            eq = seg == label
            cards += cp.sum(eq)
            intersection = cp.logical_and(intersection, cp.prod(eq, axis=0))
            time_stamp_end(f"chunk {i}")

        time_stamp_start("dice")
        intersection = cp.sum(intersection)
        if cards == 0:
            dice = 0
        else:
            dice = (n * intersection) / cards
    else:
        seg = cp.asarray(segs)
        eq = seg == label
        cards = cp.sum(eq)
        if cards == 0:
            dice = 0
        else:
            intersection = cp.prod(eq, axis=0)
            intersection = cp.sum(intersection)
            dice = (n * intersection) / cards

    time_stamp_end("dice")

    print("n", n)
    print("cards       ", cards)
    print("intersection", intersection)
    print("dice        ", dice)

    time_stamp_end("compute_dice_N_gpu")

    return dice


def compute_dice_N_cpu(segs, label):
    n = segs.shape[0]
    # Compute the intersection of all segmentations
    eq = segs == label
    cards = np.sum(eq)
    if cards == 0:
        return 0
    intersection = np.prod(eq, axis=0)
    intersection = np.sum(intersection)
    dice = (n * intersection) / cards
    return dice


def compute_dice_N(segs, label, gpu):
    if gpu:
        return compute_dice_N_gpu(segs, label)
    else:
        return compute_dice_N_cpu(segs, label)


def compute_dice_labels(segs, labels, i, gpu):
    dices = {
        label: compute_dice_N(segs, label, gpu)
        for label in tqdm(
            labels,
            disable=not progress_bar,
            position=i,
            total=len(labels),
            desc="Computing Dice",
        )
    }
    return dices


def compute_dice(subject, segmentation_files, labels, i, gpu):
    pbar = tqdm(
        segmentation_files,
        disable=not progress_bar,
        desc="Reading Segmentation",
        total=len(segmentation_files),
        position=i,
    )

    segs = joblib.Parallel(n_jobs=-1, verbose=0, return_as="generator")(
        joblib.delayed(read_seg)(seg) for seg in pbar
    )

    segs = np.fromiter(segs, dtype=(np.int16, 256 * 256 * 256))

    dices = compute_dice_labels(segs, labels, i, gpu)

    return (subject, dices)


def compute_within_subject_dice(segmentations):
    # make map between subject and segmentation files
    subject_segmentation_map = {}
    for seg in segmentations:
        subject = os.path.basename(os.path.dirname(os.path.dirname(seg)))
        subject_segmentation_map[subject] = subject_segmentation_map.get(
            subject, []
        ) + [seg]

    return subject_segmentation_map


def compute_between_subject_dice(segmentations):
    # make map between subject and segmentation files
    repetition_segmentation_map = {}
    for seg in segmentations:
        repetition = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.dirname(seg)))
        )
        repetition_segmentation_map[repetition] = repetition_segmentation_map.get(
            repetition, []
        ) + [seg]

    return repetition_segmentation_map


def run_compute_dice(iter_segmentation_map, labels, gpu):
    pbar = tqdm(
        enumerate(iter_segmentation_map.items()),
        desc="Computing Dice",
        total=len(iter_segmentation_map),
        position=0,
        disable=not progress_bar,
    )
    subject_dice_map = {}
    for i, (iteration, segmentations) in pbar:
        dices = compute_dice(iteration, segmentations, labels, i, gpu)
        subject_dice_map[iteration] = dices
        pd.DataFrame.from_dict(dices).to_csv(
            f"dice_between_subjects_{iteration}.csv", index=False
        )
    return subject_dice_map


def parse_labels(labels_file):
    labels = []
    with open(labels_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            labels.append(int(line.strip().split()[0]))
    return labels


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Path to the repetitions directory",
    )
    parser.add_argument(
        "--between-subjects",
        action="store_true",
        help="Compute dice between subjects",
    )
    parser.add_argument(
        "--labels",
        type=str,
        help="Path to the labels file",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use GPU",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    labels = parse_labels(args.labels)

    # flatten the list
    # Parse labels
    labels = parse_labels(args.labels)
    print(f"Loaded {len(labels)} labels")

    # Find all segmentation files
    cohort = pd.read_csv(args.cohort_file)
    cohort["path"] = (
        args.input_dir
        + "/"
        + "rep"
        + cohort["repetition"].astype(str)
        + "/"
        + cohort["subject"].astype(str)
        + "/"
        + "mri"
        + "/"
        + "aparc+aseg.mgz"
    )
    segmentations = cohort["path"].tolist()

    print("Number of segmentations: ", len(segmentations))

    # make map between subject and segmentation files
    iter_segmentation_map = {}
    if args.between_subjects:
        iter_segmentation_map = compute_between_subject_dice(segmentations)
    else:
        iter_segmentation_map = compute_within_subject_dice(segmentations)

    iterations = list(iter_segmentation_map.keys())

    if args.between_subjects:
        print("Number of repetitions: ", len(iterations))
    else:
        print("Number of subjects: ", len(iterations))

    if args.between_subjects:
        subject_dice_map = run_compute_dice(iter_segmentation_map, labels, args.gpu)
    else:
        # Compute dice for each subject
        subject_dice_map = joblib.Parallel(n_jobs=-1, verbose=10)(
            joblib.delayed(compute_dice)(iteration, segmentations, labels, i, args.gpu)
            for (i, (iteration, segmentations)) in enumerate(
                iter_segmentation_map.items()
            )
        )
        pd.DataFrame.from_dict(subject_dice_map).to_csv(
            "dice_within_subjects.csv", index=False
        )


if "__main__" == __name__:
    main()
