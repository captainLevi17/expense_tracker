# Imports
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import sys
# Objects
class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.resize(550, 500)
        
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        self.dropdown.addItems(["Food", "Transport", "Utilities", "Entertainment", "Other"])

        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID"," Date", "Category", "Amount", "Description"])
        
# Layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addWidget(self.table)

        self.load_table()
        self.setLayout(self.master_layout)

    def load_table(self):
            self.table.setRowCount(0)

            query = QSqlQuery("SELECT * FROM expenses")
            row = 0
            while query.next():
                expense_id = query.value(0)
                date = query.value(1)
                category = query.value(2)
                amount = query.value(3)
                description = query.value(4)
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
                self.table.setItem(row, 1, QTableWidgetItem(date))
                self.table.setItem(row, 2, QTableWidgetItem(category))
                self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
                self.table.setItem(row, 4, QTableWidgetItem(description))
                row += 1

    def add_expense(self):
            date = self.date_box.date().toString("yyyy-MM-dd")
            category = self.dropdown.currentText()
            amount = self.amount.text()
            description = self.description.text()

            if not amount:
                QMessageBox.warning(self, "Input Error", "Amount cannot be empty.")
                return

            query = QSqlQuery()
            query.prepare("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)")
            query.addBindValue(date)
            query.addBindValue(category)
            query.addBindValue(amount)
            query.addBindValue(description)
            query.exec_()

            self.date_box.setDate(QDate.currentDate())
            self.dropdown.setCurrentIndex(0)
            self.amount.clear()
            self.description.clear()

            self.load_table()

        
 
        

        

# Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expenses.db")
if not database.open():
    QMessageBox.critical(None, "Database Error", "Opening database failed.")
    print("Unable to open data source file.")
    sys.exit(1)
query = QSqlQuery()
query.exec_("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")




# Execution
if __name__ == "__main__":
    app = QApplication([])
    main = ExpenseTracker()
    main.show()
    app.exec_()



