"""Main config class."""

from pydantic import BaseModel


class Config(BaseModel):
    """Main config class."""

    # Reproducibility
    seed: int = 42

    # Data
    test_split: float = 0.1
    batch_size: int = 16

    # Training
    max_epochs: int = 200
    early_stopping_patience: int = 30
    learning_rate: float = 1e-4
    min_learning_rate: float = 1e-6
    weight_decay: float = 1e-2

    # Model
    base_model: str = "some_pretrained_model"
