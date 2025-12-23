# Small example using VIP API

`./freesurfer-recon-all.sh` script launches Freesurfer on VIP server through VIP API.

## Requirements

### VIP API token

Export the API token before executing `./freesurfer-recon-all.sh`

`export VIP_API_TOKEN=<token>`

### Freesurfer license

Add your Freesurfer license in `inputs/LICENSE.txt`

### Get dataset

Install [`datalad`](https://handbook.datalad.org/en/latest/intro/installation.html)

For Linux:

via apt
```
sudo apt-get install datalad
```
or via PyPI
```
pip install datalad
```

Download the T1 image:
```
datalad get example/freesurfer/inputs/ds001600/sub-1/anat/sub-1_T1w.nii.gz
```

## Scripts

#### `download.py`

Download VIP session outputs (or list pipeline details) using a VIP API token.

#### `generate_inputs_json.py`

Scan the inputs directory for NIfTI files and generate an `inputs.json` mapping subjects to file paths (with optional checks).

#### `generate_input_settings.py`

Build the VIP pipeline input settings JSON from a prepared input data file, including directives, license, and NIfTI paths.

#### `run_pipeline.py`

Create a VIP session, optionally upload inputs, and launch the FreeSurfer pipeline with the provided settings.

