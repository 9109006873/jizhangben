import os
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from app.database import Database
from app.export_excel import export_expenses
from app.screens import MainScreen, ExpenseScreen


class MyExpenseBookApp(App):
    title = "我的记账本"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = None
        self.main_screen = None
        self.root_container = None

    def build(self):
        Window.softinput_mode = "below_target"

        database_path = os.path.join(
            self.user_data_dir,
            "expenses.db"
        )

        self.database = Database(database_path)

        self.root_container = BoxLayout(
            orientation="vertical"
        )

        self.show_main()

        return self.root_container

    def show_main(self):
        self.root_container.clear_widgets()

        self.main_screen = MainScreen(self)

        self.root_container.add_widget(
            self.main_screen
        )

    def show_add(self):
        self.root_container.clear_widgets()

        self.root_container.add_widget(
            ExpenseScreen(self)
        )

    def show_edit(self, expense):
        self.root_container.clear_widgets()

        self.root_container.add_widget(
            ExpenseScreen(
                self,
                expense=expense
            )
        )

    def export_excel(self):
        expenses = self.database.get_all_expenses()

        if not expenses:
            self.show_message(
                "暂无记录",
                "当前没有可以导出的记账记录。"
            )
            return

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = f"我的记账本_{timestamp}.xlsx"

        export_dir = self.user_data_dir
        file_path = os.path.join(
            export_dir,
            filename
        )

        try:
            export_expenses(
                expenses,
                file_path
            )

            self.show_message(
                "导出成功",
                f"Excel 已生成：\n{filename}\n\n"
                f"文件位置：\n{file_path}"
            )

        except Exception as exc:
            self.show_message(
                "导出失败",
                str(exc)
            )

    def show_message(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.85, 0.4),
        )

        popup.open()

    def on_stop(self):
        if self.database:
            self.database.close()


if __name__ == "__main__":
    MyExpenseBookApp().run()
