from pathlib import Path

import numpy as np
import pyreadstat

DATA = Path(__file__).resolve().parents[1] / "data" / "imported_excel.sav"


def load():
    return pyreadstat.read_sav(DATA)


def test_shape_and_missing_counts():
    df, _ = load()
    assert df.shape == (8, 12)
    assert df["rank"].isna().sum() == 3
    assert df.gender.isna().sum() == 1
    assert df.weight.isna().sum() == 2


def test_zscores_match_definition():
    df, _ = load()
    assert np.allclose(df.Zheight, (df.height - df.height.mean()) / df.height.std())
    assert np.allclose(
        df.Zweight, (df.weight - df.weight.mean()) / df.weight.std(), equal_nan=True
    )


def test_duplicate_zscore_columns():
    df, _ = load()
    assert np.allclose(df.Zheight, df.ZSco01)
    assert np.allclose(df.Zweight, df.ZSco02, equal_nan=True)
