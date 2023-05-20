import pandas as _pd


def load_xlsx(
    path: str,
    sheet_name: str = None,
) -> _pd.DataFrame:
    with open(path, "rb") as f:
        df = _pd.read_excel(f, sheet_name or "Sheet1")
    
    return df


def write_xlsx(
    path: str,
    df: _pd.DataFrame,
    sheet_name: str = None,
):
    with _pd.ExcelWriter(path) as fw:
        df.to_excel(fw, sheet_name or "Sheet1", index=False)
