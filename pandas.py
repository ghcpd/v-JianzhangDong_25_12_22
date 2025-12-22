"""Minimal pandas stub to enable the project's simple tests without installing full pandas.
This implements only the small API used by the tests: DataFrame constructor, to_csv, read_csv,
__getitem__ returning a Series-like object with to_numpy(), .columns and .empty.
"""
from pathlib import Path
import csv
import numpy as np

class Series:
    def __init__(self, data):
        self._data = list(data)

    def to_numpy(self):
        return np.array(self._data)

class DataFrame:
    def __init__(self, data):
        # Accept dict of lists or list of dicts
        if isinstance(data, dict):
            self._data = {k: list(v) for k, v in data.items()}
        else:
            # list of rows
            cols = set()
            for r in data:
                cols.update(r.keys())
            self._data = {c: [row.get(c) for row in data] for c in cols}

    @property
    def columns(self):
        return list(self._data.keys())

    @property
    def empty(self):
        # empty if no rows
        any_col = next(iter(self._data.values()), [])
        return len(any_col) == 0

    def __getitem__(self, key):
        return Series(self._data[key])

    def to_csv(self, path, index=False):
        path = Path(path)
        cols = self.columns
        rows = list(zip(*[self._data[c] for c in cols]))
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            for row in rows:
                writer.writerow(row)

def read_csv(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        data = {c: [] for c in cols}
        for r in reader:
            for c in cols:
                data[c].append(r[c])
        return DataFrame(data)

# Convenience alias
DataFrame = DataFrame
read_csv = read_csv
