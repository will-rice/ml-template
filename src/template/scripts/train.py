"""Train script."""

import json
from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv
from git import Repo
from lightning import seed_everything

from template.config import Config
from template.kaggle import (
    default_data_root,
    default_output_root,
    is_kaggle_environment,
)


def main() -> None:
    """Train script."""
    parser = ArgumentParser(description="Train script.")
    parser.add_argument("data_root", nargs="?", default=None, type=Path)
    parser.add_argument("--competition", default=None, type=str)
    parser.add_argument("--project", default="kaggle-template", type=str)
    parser.add_argument("--num_devices", default=1, type=int)
    parser.add_argument("--num_workers", default=12, type=int)
    parser.add_argument("--log_root", default=None, type=Path)
    parser.add_argument("--submission_path", default=None, type=Path)
    parser.add_argument("--checkpoint_path", default=None, type=Path)
    parser.add_argument("--weights_path", type=Path, default=None)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--fast_dev_run", action="store_true")
    args = parser.parse_args()
    load_dotenv()

    config = Config()
    running_in_kaggle = is_kaggle_environment()
    competition_name = args.competition or config.competition_name
    data_root = args.data_root or (
        config.kaggle_input_root / competition_name
        if running_in_kaggle
        else default_data_root(competition_name)
    )
    log_root = args.log_root or (
        config.kaggle_working_root if running_in_kaggle else default_output_root()
    )
    submission_path = (
        args.submission_path or log_root / f"{competition_name}-submission.csv"
    )

    seed_everything(config.seed, workers=True)

    git_repo = Repo()
    git_hash = git_repo.head.object.hexsha[:7]
    model_name = config.base_model.split("/")[-1]
    experiment_path = log_root / f"{model_name}-{git_hash}"
    experiment_path.mkdir(exist_ok=True, parents=True)
    submission_path.parent.mkdir(exist_ok=True, parents=True)
    run_config_path = experiment_path / "run_config.json"
    run_config_path.write_text(
        json.dumps(
            {
                "competition_name": competition_name,
                "data_root": str(data_root),
                "project": args.project,
                "log_root": str(log_root),
                "submission_path": str(submission_path),
                "num_devices": args.num_devices,
                "num_workers": args.num_workers,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
