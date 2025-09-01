# Installation Guide

This guide will help you set up the Hybrid-Retrieval-Augmented-Generation project on your system.

## Prerequisites

- Python 3.12 or higher
- uv (Python package installer)

## Installation Steps

1. First, install `uv` if you haven't already:

```bash
pip install uv
```

1. Clone the repository:

```bash
git clone https://github.com/py-mo/Hybrid-Retrieval-Augmented-Generation.git
cd Hybrid-Retrieval-Augmented-Generation
```

1. Create and activate a virtual environment using uv:

```bash
uv venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate  # On Windows
```

1. Install the project dependencies using uv:

```bash
uv pip install -r requirements.txt
```

1. Install the package in development mode:

```bash
uv pip install -e .
```

## Verifying Installation

To verify that the installation was successful, you can run:

```bash
python3 -c "import src; print('Installation successful!')"
```

## Troubleshooting

If you encounter any issues during installation:

1. Make sure you have Python 3.12 or higher installed
2. Ensure all prerequisites are properly installed
3. Try removing the virtual environment and starting fresh

For additional help, please open an issue on the GitHub repository.
