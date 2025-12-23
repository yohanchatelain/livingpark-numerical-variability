import argparse
from vip_client import VipSession
import json


def load_input_settings(input_settings_file):
    with open(input_settings_file, "r") as f:
        input_settings = json.load(f)
    return input_settings


def create_session(api_key, session):
    VipSession.init(api_key)
    session = VipSession(session_name=session)
    return session


def upload_inputs(session, input_dir):
    session.upload_inputs(input_dir=input_dir)


def launch_pipeline(session, pipeline_id, input_settings, nb_runs):
    session.launch_pipeline(
        pipeline_id=pipeline_id, input_settings=input_settings, nb_runs=nb_runs
    )


def parse_args():

    parser = argparse.ArgumentParser(description="Run a VIP pipeline")
    parser.add_argument("--api-key", help="API key for VIP", required=True)
    parser.add_argument("--session", help="Session name", required=True)
    parser.add_argument(
        "--pipeline-id",
        default="FreeSurfer-Recon-all-fuzzy/v7.3.1",
        help="Pipeline ID",
    )
    parser.add_argument("--input-dir", help="Input directory")
    parser.add_argument("--input-settings", help="Input settings", required=True)
    parser.add_argument(
        "--nb-runs", type=int, help="Number of parallel runs", required=True
    )
    parser.add_argument("--upload-inputs", action="store_true", help="Upload inputs")
    return parser.parse_args()


def main():
    args = parse_args()
    session = create_session(args.api_key, args.session)
    if args.upload_inputs:
        upload_inputs(session, args.input_dir)
    input_settings = load_input_settings(args.input_settings)
    launch_pipeline(session, args.pipeline_id, input_settings, args.nb_runs)


if __name__ == "__main__":
    main()