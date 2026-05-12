"""Shared per-school data types.

Holds the `IQBEduData` wrapper and the column/percentile constants that
both `aggregate.py` (which produces it) and `reader.py` (which loads it)
need. Lifting these out avoids a circular import between the two.
"""

from dataclasses import dataclass

import pandas as pd
from iqb.cache.mlab import IQBDataMLab

VALID_PERCENTILES = (1, 5, 10, 25, 50, 75, 90, 95, 99)

EXPECTED_COLUMNS = (
    ["school_id", "giga_id_school", "download_sample_count"]
    + [f"download_p{p}" for p in VALID_PERCENTILES]
    + [f"latency_p{p}" for p in VALID_PERCENTILES]
    + [f"loss_p{p}" for p in VALID_PERCENTILES]
    + ["upload_sample_count"]
    + [f"upload_p{p}" for p in VALID_PERCENTILES]
)


@dataclass(frozen=True)
class IQBEduData:
    """Per-school IQB percentile data."""

    df: pd.DataFrame

    @property
    def schools(self) -> list[str]:
        """Sorted list of school IDs."""
        return sorted(self.df["school_id"].tolist())

    @property
    def sample_counts(self) -> pd.DataFrame:
        """School IDs with download and upload sample counts."""
        return (
            self.df[["school_id", "download_sample_count", "upload_sample_count"]]
            .sort_values("download_sample_count", ascending=False)
            .reset_index(drop=True)
        )

    def to_iqb_data(self, school_id: str, *, percentile: int = 95) -> IQBDataMLab:
        """Extract IQB metrics for a school at a given percentile.

        Returns an IQBDataMLab instance ready for use with IQBCalculator.
        """
        if percentile not in VALID_PERCENTILES:
            raise ValueError(
                f"percentile must be one of {VALID_PERCENTILES}, got {percentile}"
            )
        rows = self.df[self.df["school_id"] == school_id]
        if len(rows) == 0:
            raise KeyError(f"school not found: {school_id}")
        row = rows.iloc[0]
        return IQBDataMLab(
            download=float(row[f"download_p{percentile}"]),
            upload=float(row[f"upload_p{percentile}"]),
            latency=float(row[f"latency_p{percentile}"]),
            loss=float(row[f"loss_p{percentile}"]),
        )
