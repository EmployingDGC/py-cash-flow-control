import pandas as _pd
import math as _mt
import re as _re

from msvcrt import getch as _getch

from ..file import (
    load_xlsx as _load_xlsx,
    write_xlsx as _write_xlsx,
    file_exists as _file_exists,
)


class Expense:
    _DF_COLUMNS = ("expense", "amount", "payment_day", "paid")
    _DF_TYPES = ("string", "float64", "int64", "bool")
    _DF_QTT_ITEMS_PER_PAGE = 10
    _RE_DUPLICATED_SPACES = r" {2,}"
    
    def __init__(
        self,
        file_path: str
    ) -> None:
        self._file_path: str = file_path
        
        if not _file_exists(file_path):
            _write_xlsx(file_path, _pd.DataFrame(columns=self._DF_COLUMNS))

        self.df = _load_xlsx(file_path).astype(dict(zip(self._DF_COLUMNS, self._DF_TYPES)))

    def new(
        self,
        description: str,
        value: float,
        day: int,
    ):
        data = dict(zip(self._DF_COLUMNS, ([description], [value], [day], [False])))
        
        new = _pd.DataFrame(data)
        
        self.df = _pd.concat([self.df, new]).reset_index(drop=True)
        
        return self

    def save(self):
        _write_xlsx(self._file_path, self.df)
        
        return self

    def _slice_df(self):
        for i in range(0, self.df.shape[0], self._DF_QTT_ITEMS_PER_PAGE):
            yield self.df.iloc[i: i + self._DF_QTT_ITEMS_PER_PAGE]

    def print(self):
        for i, _df in enumerate(self._slice_df(), 1):
            print(f"\n{_df}\n")
            print(f"Página {i} de {_mt.ceil(self.df.shape[0] / self._DF_QTT_ITEMS_PER_PAGE)}")
            print("Precione Qualquer Tecla para ir para a próxima página (ESC - Sair)\n")
            
            if _getch() == b'\x1b':
                break
        
        return self
