import pandas as _pd
import math as _mt

from msvcrt import getch

import src


def menu(
    title: str,
    options: dict[str, str],
) -> str:
    
    max_option = max(map(len, options.keys()))
    max_value = max(map(len, options.values()))
    
    len_line_top = max_option + max_value + 5
    len_line_left = max_option + 2
    len_line_right = max_value + 2
    
    line_top = "-" * len_line_top
    line_left = "-" * len_line_left
    line_right = "-" * len_line_right
    
    line_middle_and_bottom = f"+{line_left}+{line_right}+"
    
    header = (
        f"+{line_top}+"
        f"\n|{title:^{len_line_top}}|"
        f"\n{line_middle_and_bottom}"
    )
    
    body = "\n".join(
        f"| {k:>{len_line_left - 2}} | {v:<{len_line_right - 2}} |"
        for k, v in options.items()
    )
    
    footer = f"{line_middle_and_bottom}"
    
    return f"{header}\n{body}\n{footer}"


def new_expense(
    df: _pd.DataFrame,
    file_path: str,
) -> _pd.DataFrame:
    description = input("Informe a descrição da despesa: ").strip()
    value = float(input("Informe o valor da despesa: ").strip().replace(",", "."))
    day = int(input("Informe o dia do vencimento da despesa: ").strip())
    
    data = dict(zip(df.columns, ([description], [value], [day], [False])))
    
    new = _pd.DataFrame(data)
    
    return _pd.concat([df, new]).reset_index(drop=True)


def save_expenses(
    df: _pd.DataFrame,
    file_path: str,
) -> _pd.DataFrame:
    src.write_xlsx(file_path, df)
    
    return src.load_xlsx(file_path).astype(df.dtypes)


def print_expenses(
    df: _pd.DataFrame,
    file_path: str,
) -> _pd.DataFrame:
    def slice_df(df: _pd.DataFrame, qtt_slice: int):
        for i in range(0, df.shape[0], qtt_slice):
            yield df.iloc[i: i + qtt_slice]
    
    qtt_slice = 10
    
    for i, _df in enumerate(slice_df(df, qtt_slice), 1):
        print(f"\n{_df}\n")
        print(f"Página {i} de {_mt.ceil(df.shape[0] / qtt_slice)}")
        print("Precione Qualquer Tecla para ir para a próxima página (ESC - Sair)\n")
        if getch() == b'\x1b':
            break
    
    return df


def main():
    FILE_PATH = r"./downloads/cash_flow_control.xlsx"
    
    COLUMNS = ("expense", "amount", "payment_day", "paid")
    TYPES = ("string", "float64", "int64", "bool")
    
    if not src.file_exists(FILE_PATH):
        src.write_xlsx(FILE_PATH, _pd.DataFrame(columns=COLUMNS))

    df = src.load_xlsx(FILE_PATH).astype(dict(zip(COLUMNS, TYPES)))
    
    str_menu = menu(
        title="MENU",
        options={
            "1": "Cadastrar Despesa",
            "2": "Salvar Alterações",
            "3": "Exibir Despesas",
            "0": "Sair",
        }
    )
    
    all_options = {
        "1": new_expense,
        "2": save_expenses,
        "3": print_expenses,
    }
    
    while True:
        print(str_menu)
        op = input("Escolha uma opção acima: ")
        
        if op == "0":
            break
        
        option = all_options.get(op)
        
        if not option:
            print("Opção inválida")
            continue
        
        df = option(df, FILE_PATH)


if __name__ == "__main__":
    main()
