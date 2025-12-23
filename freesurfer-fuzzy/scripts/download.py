import argparse

from vip_client import VipSession

apikey_filename = ".api_token.txt"
fs_pipeline_id = "FreeSurfer-Recon-all-fuzzy/v7.3.1"
retry_max = 100

def login(api_key):
    VipSession.init(api_key=api_key)


def create_session(session_name, pipeline_id):
    session = VipSession(session_name=session_name, pipeline_id=pipeline_id)
    return session


def download_outputs(session):
    retry = 0
    while retry < retry_max:
        try:
            session.download_outputs(unzip=False, init_timeout=0)
        except Exception as e:
            print(e)
            retry += 1


def show_pipeline():
    VipSession.show_pipeline()


def get_args():
    parser = argparse.ArgumentParser(description="Download Freesurfer Fuzzy Session")
    parser.add_argument(
        "--api-key", default=apikey_filename, type=str, help="API key for VIP"
    )
    parser.add_argument("--show-pipeline", action="store_true", help="Show pipeline")
    parser.add_argument(
        "--session-name", default="freesurfer-fuzzy", type=str, help="Session name"
    )
    parser.add_argument(
        "--pipeline-id", default=fs_pipeline_id, type=str, help="Pipeline ID"
    )
    return parser.parse_args()


def main():
    args = get_args()
    login(args.api_key)

    if args.show_pipeline:
        show_pipeline()
        return

    session = create_session(args.session_name, args.pipeline_id)
    download_outputs(session)


if __name__ == "__main__":
    main()