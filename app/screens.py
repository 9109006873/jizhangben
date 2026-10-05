from datetime import date

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from app.widgets import ExpenseItem


def format_money(cents):
    return f"¥ {cents / 100:.2f}"


def parse_amount(text):
    text = text.strip().replace("¥", "").replace(",", "")

    if not text:
        raise ValueError("请输入金额")

    value = float(text)

    if value < 0:
        raise ValueError("金额不能为负数")

    cents = round(value * 100)

    if cents <= 0:
        raise ValueError("金额必须大于 0")

    return cents


class MainScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=8,
            padding=12,
            **kwargs
        )

        self.app = app

        self.summary = Label(
            text="",
            size_hint_y=None,
            height=90,
            font_size=18,
        )

        self.add_widget(self.summary)

        button_bar = BoxLayout(
            size_hint_y=None,
            height=52,
            spacing=8,
        )

        add_button = Button(text="＋ 记一笔")
        add_button.bind(on_release=lambda *_: self.app.show_add())

        export_button = Button(text="导出 Excel")
        export_button.bind(on_release=lambda *_: self.app.export_excel())

        button_bar.add_widget(add_button)
        button_bar.add_widget(export_button)

        self.add_widget(button_bar)

        self.scroll = ScrollView()

        self.list_box = BoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint_y=None,
        )

        self.list_box.bind(
            minimum_height=self.list_box.setter("height")
        )

        self.scroll.add_widget(self.list_box)
        self.add_widget(self.scroll)

        self.refresh()

    def refresh(self):
        today = date.today().isoformat()
        month = today[:7]

        today_total = self.app.database.get_today_total(today)
        month_total = self.app.database.get_month_total(month)
        total = self.app.database.get_total()

        self.summary.text = (
            f"今天：{format_money(today_total)}\n"
            f"本月：{format_money(month_total)}\n"
            f"累计：{format_money(total)}"
        )

        self.list_box.clear_widgets()

        expenses = self.app.database.get_all_expenses()

        if not expenses:
            self.list_box.add_widget(
                Label(
                    text="暂无记账记录\n点击“＋ 记一笔”开始记录",
                    size_hint_y=None,
                    height=120,
                    halign="center",
                    valign="middle",
                )
            )
            return

        for expense in expenses:
            item = ExpenseItem(expense)
            item.bind(
                on_release=lambda instance,
                expense=expense: self.app.show_edit(expense)
            )
            self.list_box.add_widget(item)


class ExpenseScreen(BoxLayout):
    def __init__(self, app, expense=None, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=12,
            padding=16,
            **kwargs
        )

        self.app = app
        self.expense = expense

        title = "编辑账单" if expense else "记一笔"

        self.add_widget(
            Label(
                text=title,
                font_size=24,
                size_hint_y=None,
                height=50,
            )
        )

        self.amount_input = TextInput(
            hint_text="金额，例如 25.50",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=52,
        )

        self.date_input = TextInput(
            hint_text="日期，例如 2026-10-05",
            multiline=False,
            size_hint_y=None,
            height=52,
        )

        self.note_input = TextInput(
            hint_text="备注（可选）",
            multiline=False,
            size_hint_y=None,
            height=52,
        )

        self.add_widget(self.amount_input)
        self.add_widget(self.date_input)
        self.add_widget(self.note_input)

        save_button = Button(
            text="保存",
            size_hint_y=None,
            height=52,
        )
        save_button.bind(on_release=self.save)

        self.add_widget(save_button)

        if expense:
            delete_button = Button(
                text="删除这条记录",
                size_hint_y=None,
                height=52,
            )
            delete_button.bind(on_release=self.delete)
            self.add_widget(delete_button)

        cancel_button = Button(
            text="返回",
            size_hint_y=None,
            height=52,
        )
        cancel_button.bind(
            on_release=lambda *_: self.app.show_main()
        )

        self.add_widget(cancel_button)

        if expense:
            self.amount_input.text = f"{expense['amount'] / 100:.2f}"
            self.date_input.text = expense["expense_date"]
            self.note_input.text = expense["note"] or ""
        else:
            self.date_input.text = date.today().isoformat()

    def show_error(self, message):
        popup = Popup(
            title="提示",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
        )
        popup.open()

    def save(self, *_):
        try:
            amount = parse_amount(self.amount_input.text)
        except ValueError as exc:
            self.show_error(str(exc))
            return

        expense_date = self.date_input.text.strip()

        try:
            date.fromisoformat(expense_date)
        except ValueError:
            self.show_error("日期格式错误，请使用 YYYY-MM-DD")
            return

        note = self.note_input.text.strip()

        if self.expense:
            self.app.database.update_expense(
                self.expense["id"],
                amount,
                expense_date,
                note,
            )
        else:
            self.app.database.add_expense(
                amount,
                expense_date,
                note,
            )

        self.app.show_main()

    def delete(self, *_):
        popup_content = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10,
        )

        popup_content.add_widget(
            Label(text="确定删除这条记录吗？")
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10,
        )

        yes_button = Button(text="删除")
        no_button = Button(text="取消")

        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)

        popup_content.add_widget(buttons)

        popup = Popup(
            title="确认删除",
            content=popup_content,
            size_hint=(0.8, 0.3),
        )

        no_button.bind(
            on_release=popup.dismiss
        )

        def confirm_delete(*_):
            self.app.database.delete_expense(
                self.expense["id"]
            )
            popup.dismiss()
            self.app.show_main()

        yes_button.bind(on_release=confirm_delete)

        popup.open()
