import src


_FILE_PATH = r"./downloads/cash_flow_control.xlsx"


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
    expense: src.Expense
):
    description = input("Informe a descrição da despesa: ").strip().upper()
    value = float(input("Informe o valor da despesa: ").strip().replace(",", "."))
    day = int(input("Informe o dia do vencimento da despesa: ").strip())

    expense.new(description, value, day)


def save_expenses(
    expense: src.Expense
):
    expense.save()


def print_expenses(
    expense: src.Expense
):
    expense.print()


def close_expenses(
    expense: src.Expense
):
    exit(0)


def main():
    str_menu = menu(
        title="MENU",
        options={
            "1": "Cadastrar Despesa",
            "2": "Salvar Alterações",
            "3": "Exibir Despesas",
            "0": "Sair",
        }
    )
    
    expense = src.Expense(_FILE_PATH)
    
    all_options = {
        "0": close_expenses,
        "1": new_expense,
        "2": save_expenses,
        "3": print_expenses,
    }
    
    while True:
        print(str_menu)
        op = input("Escolha uma opção acima: ")
        
        option = all_options.get(op)
        
        if not option:
            print("Opção inválida")
            continue
        
        option(expense)


if __name__ == "__main__":
    main()
