# app/database.py
import os
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "expenses.db"
            )

        self.db_path = db_path
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount INTEGER NOT NULL,
                    expense_date TEXT NOT NULL,
                    note TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_expenses_date
                ON expenses(expense_date)
                """
            )

            conn.commit()

    def add_expense(self, amount, expense_date, note=""):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO expenses
                (amount, expense_date, note, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    amount,
                    expense_date,
                    note,
                    now,
                    now,
                ),
            )

            conn.commit()
            return cursor.lastrowid

    def update_expense(self, expense_id, amount, expense_date, note=""):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._connect() as conn:
            conn.execute(
                """
                UPDATE expenses
                SET amount = ?,
                    expense_date = ?,
                    note = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    amount,
                    expense_date,
                    note,
                    now,
                    expense_id,
                ),
            )

            conn.commit()

    def delete_expense(self, expense_id):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM expenses WHERE id = ?",
                (expense_id,),
            )
            conn.commit()

    def get_expense(self, expense_id):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM expenses
                WHERE id = ?
                """,
                (expense_id,),
            ).fetchone()

            return dict(row) if row else None

    def get_all_expenses(self):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM expenses
                ORDER BY expense_date DESC, id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]

    def get_today_total(self, today):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM expenses
                WHERE expense_date = ?
                """,
                (today,),
            ).fetchone()

            return row["total"]

    def get_month_total(self, month_prefix):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM expenses
                WHERE expense_date LIKE ?
                """,
                (month_prefix + "%",),
            ).fetchone()

            return row["total"]

    def get_total(self):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM expenses
                """
            ).fetchone()

            return row["total"]

    def close(self):
        pass
