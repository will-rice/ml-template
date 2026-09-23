"""Tests for Kaggle helpers."""

from pathlib import Path

import pytest

from template.kaggle import (
    default_data_root,
    default_output_root,
    default_submission_path,
    write_submission,
)


def test_default_data_root_prefers_local_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default data path should stay local outside Kaggle."""
    monkeypatch.delenv("KAGGLE_URL_BASE", raising=False)
    assert default_data_root("titanic") == Path("data") / "titanic"


def test_default_data_root_prefers_kaggle_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default data path should use Kaggle mounts inside Kaggle."""
    monkeypatch.setenv("KAGGLE_URL_BASE", "https://www.kaggle.com")
    assert default_data_root("titanic") == Path("/kaggle/input") / "titanic"
    assert default_output_root() == Path("/kaggle/working")
    assert default_submission_path("titanic") == Path(
        "/kaggle/working/titanic-submission.csv"
    )


def test_write_submission_writes_expected_csv(tmp_path: Path) -> None:
    """Submission files should contain the expected header and rows."""
    output_path = tmp_path / "submissions" / "submission.csv"

    write_submission(
        ids=[1, 2],
        predictions=[0.1, 0.9],
        output_path=output_path,
        id_column="PassengerId",
        target_column="Survived",
    )

    assert output_path.read_text(encoding="utf-8").splitlines() == [
        "PassengerId,Survived",
        "1,0.1",
        "2,0.9",
    ]


def test_write_submission_rejects_mismatched_lengths(tmp_path: Path) -> None:
    """Submission files require ids and predictions to align."""
    with pytest.raises(ValueError, match="same length"):
        write_submission(
            ids=[1],
            predictions=[0.1, 0.9],
            output_path=tmp_path / "submission.csv",
        )
