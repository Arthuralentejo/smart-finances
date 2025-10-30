"""CSV file parser for bank statements."""

import pandas as pd


def load_csv(file_path: str) -> str:
    """Load a CSV file and return its contents as a Markdown table.

    Args:
        file_path: Path to the CSV file.

    Returns:
        CSV contents formatted as a Markdown table.
    """
    df = pd.read_csv(file_path)
    return df.to_markdown(index=False)
