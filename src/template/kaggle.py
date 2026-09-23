"""Helpers for Kaggle-oriented workflows."""

import csv
import os
from collections.abc import Sequence
from pathlib import Path

KAGGLE_INPUT_ROOT = Path("/kaggle/input")
KAGGLE_WORKING_ROOT = Path("/kaggle/working")


def is_kaggle_environment() -> bool:
    """Return whether the current process is running inside Kaggle."""
    return os.getenv("KAGGLE_URL_BASE") is not None or (
        KAGGLE_INPUT_ROOT.exists() and KAGGLE_WORKING_ROOT.exists()
    )


def default_data_root(competition_name: str | None = None) -> Path:
    """Return the default data root for local and Kaggle runs."""
    base_path = KAGGLE_INPUT_ROOT if is_kaggle_environment() else Path("data")
    return base_path / competition_name if competition_name else base_path


def default_output_root() -> Path:
    """Return the default output root for local and Kaggle runs."""
    return KAGGLE_WORKING_ROOT if is_kaggle_environment() else Path("logs")


def default_submission_path(competition_name: str | None = None) -> Path:
    """Return a default submission path."""
    filename = "submission.csv"
    if competition_name:
        filename = f"{competition_name}-submission.csv"
    return default_output_root() / filename


def write_submission(
    ids: Sequence[str | int],
    predictions: Sequence[str | int | float],
    output_path: Path,
    id_column: str = "id",
    target_column: str = "target",
) -> Path:
    """Write a Kaggle submission file."""
    if len(ids) != len(predictions):
        msg = "ids and predictions must have the same length."
        raise ValueError(msg)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([id_column, target_column])
        writer.writerows(zip(ids, predictions, strict=True))

    return output_path
