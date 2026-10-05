from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


def export_expenses(expenses, file_path):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "记账明细"

    headers = [
        "日期",
        "金额",
        "备注",
    ]

    worksheet.append(headers)

    for cell in worksheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    total = 0

    for expense in expenses:
        amount = expense["amount"] / 100
        total += expense["amount"]

        worksheet.append(
            [
                expense["expense_date"],
                amount,
                expense["note"] or "",
            ]
        )

    worksheet.append(
        [
            "合计",
            total / 100,
            "",
        ]
    )

    worksheet.column_dimensions["A"].width = 18
    worksheet.column_dimensions["B"].width = 15
    worksheet.column_dimensions["C"].width = 40

    for row in worksheet.iter_rows(min_row=2, min_col=2, max_col=2):
        row[0].number_format = '0.00'

    filename = file_path

    workbook.save(filename)

    return filename
