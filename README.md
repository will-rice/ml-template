# Kaggle Machine Learning Template

A Kaggle-focused template for PyTorch machine learning projects using Lightning, wandb, and modern Python tooling.

## Features

- **PyTorch Lightning**: Structured training framework with minimal boilerplate
- **Kaggle-first Workflow**: Defaults to `/kaggle/input` and `/kaggle/working` when running in Kaggle
- **Pydantic Configuration**: Type-safe configuration management
- **Weights & Biases**: Integrated experiment tracking
- **Modern Tooling**: Built with `uv` for fast dependency management
- **Code Quality**: Pre-configured with `ruff`, `ty`, `pytest`, and `pre-commit` hooks
- **Git-based Versioning**: Automatic experiment naming using git commit hashes
- **Submission Helpers**: Utilities for generating competition-ready CSV submissions

## Project Structure

```
.
├── src/template/
│   ├── config.py              # Pydantic configuration classes
│   ├── lightning_module.py    # Base Lightning module
│   ├── datasets/              # Dataset implementations
│   ├── modeling/              # Model architectures
│   └── scripts/
│       └── train.py          # Training script
├── tests/                     # Test files
├── pyproject.toml            # Project metadata and dependencies
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
└── .env.example              # Example environment variables
```

## Quick Start

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Use this template for a new Kaggle project

When creating a new project from this template:

1. Clone or fork this repository
2. Rename the `src/template` directory to your project name:
   ```bash
   mv src/template src/your_project_name
   ```
3. Update `pyproject.toml`:
   - Change `name = "template"` to your project name
   - Update `module-name = ["template"]` to your project name
   - Update the `train` script path in `[project.scripts]`
4. Update import statements in Python files to use your new project name

### 3. Install dependencies

```bash
uv sync
```

### 4. Set up environment variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
# Edit .env and add your Kaggle, wandb, and other credentials
```

### 5. Install pre-commit hooks

```bash
uv run pre-commit install
```

## Usage

### Training

Run the training script:

```bash
uv run train --competition titanic --project my-project --num_devices 1
```

Available arguments:

- `data_root`: Optional path to your dataset root. Defaults to `data/<competition>` locally or `/kaggle/input/<competition>` in Kaggle
- `--competition`: Kaggle competition slug (default: `"titanic"` from config)
- `--project`: Wandb project name (default: `"kaggle-template"`)
- `--num_devices`: Number of GPUs to use (default: 1)
- `--num_workers`: Number of data loading workers (default: 12)
- `--log_root`: Directory for logs and checkpoints. Defaults to `logs/` locally or `/kaggle/working` in Kaggle
- `--submission_path`: Where to write the submission CSV. Defaults to `logs/<competition>-submission.csv` locally or `/kaggle/working/<competition>-submission.csv` in Kaggle
- `--checkpoint_path`: Resume from checkpoint
- `--weights_path`: Load model weights
- `--debug`: Enable debug mode
- `--fast_dev_run`: Run a quick test with minimal data

Typical workflows:

- **Local development**: `uv run train --competition titanic`
- **Kaggle notebook**: `uv run train --competition titanic --log_root /kaggle/working`
- **Custom data mount**: `uv run train /path/to/data --competition titanic`

### Configuration

Edit `src/template/config.py` to customize hyperparameters and competition defaults:

```python
from pydantic import BaseModel

class Config(BaseModel):
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

    # Kaggle
    competition_name: str = "titanic"
    submission_id_column: str = "PassengerId"
    submission_target_column: str = "Survived"
```

### Creating submissions

Use `template.kaggle.write_submission(...)` to write a CSV with the exact ID and target column names required by your competition.

### Implementing Your Model

1. **Create your Lightning module** by inheriting from `BaseLightningModule`:

   ```python
   from template.lightning_module import BaseLightningModule

   class MyModel(BaseLightningModule):
       def training_step(self, batch, batch_idx):
           # Your training logic here
           pass

       def validation_step(self, batch, batch_idx):
           # Your validation logic here
           pass
   ```

2. **Add your dataset** in `src/template/datasets/`:

   ```python
   from torch.utils.data import Dataset

   class MyDataset(Dataset):
       def __init__(self, data_root, config):
           # Initialize your dataset
           pass
   ```

3. **Update the training script** to use your model and dataset

## Development

### Running Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run ty check
```

### Linting and Formatting

```bash
uv run ruff check src/
uv run ruff format src/
```

### Pre-commit Hooks

Pre-commit hooks will automatically run on every commit to ensure code quality. To run manually:

```bash
uv run pre-commit run --all-files
```

## Dependencies

Core dependencies:

- **PyTorch**: Deep learning framework (with GPU support)
- **Lightning**: High-level PyTorch wrapper
- **Pydantic**: Data validation and configuration
- **Wandb**: Experiment tracking
- **python-dotenv**: Environment variable management

Development tools:

- **ruff**: Fast Python linter and formatter
- **ty**: Static type checker
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality

## Build System

This project uses `uv_build` as the build backend, which is significantly faster than traditional build systems like setuptools or hatchling.

To build the project:

```bash
uv build
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Ensure all tests pass and pre-commit hooks succeed
4. Submit a pull request

## Tips

- Experiment names automatically include the git commit hash for reproducibility
- Use `.env` for sensitive information (API keys, credentials)
- The config system uses Pydantic for type safety and validation
- Lightning automatically handles distributed training, gradient accumulation, and mixed precision
