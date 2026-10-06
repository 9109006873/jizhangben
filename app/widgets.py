# app/widgets.py
from kivy.uix.button import Button
from kivy.uix.label import Label


class ExpenseItem(Button):
    def __init__(self, expense, **kwargs):
        self.expense = expense

        amount = expense["amount"] / 100
        note = expense["note"] or "无备注"

        text = (
            f"{expense['expense_date']}\n"
            f"¥ {amount:.2f}    {note}"
        )

        super().__init__(
            text=text,
            size_hint_y=None,
            height=72,
            halign="left",
            valign="middle",
            **kwargs
        )

        self.bind(size=self._update_text_size)

    def _update_text_size(self, *_):
        self.text_size = (self.width - 30, None)
