from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication,
    QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QHBoxLayout
)
from db import Session
from models import Student, Group

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление студентами")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QTableWidget {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #444444;
            }
            QTableWidget::item {
                border: 1px solid #444444;
            }
            QPushButton {
                background-color: #007BFF;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QComboBox {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #444444;
                padding: 5px;
            }
        """)

        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Пол", "Группа"])
        self.layout.addWidget(self.table)
        
        self.init_input_fields()
        self.load_data()
        
        self.setLayout(self.layout)

    def init_input_fields(self):
        self.last_name_input = QLineEdit(self)
        self.first_name_input = QLineEdit(self)
        self.middle_name_input = QLineEdit(self)
        self.gender_input = QCheckBox("Мужской", self)
        self.group_input = QComboBox(self)
        with Session() as session:
            groups = session.query(Group).all()
            for group in groups:
                self.group_input.addItem(group.name)
        add_button = QPushButton("Добавить студента", self)
        add_button.clicked.connect(self.add_student)
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Фамилия:"))
        input_layout.addWidget(self.last_name_input)
        input_layout.addWidget(QLabel("Имя:"))
        input_layout.addWidget(self.first_name_input)
        input_layout.addWidget(QLabel("Отчество:"))
        input_layout.addWidget(self.middle_name_input)
        input_layout.addWidget(self.gender_input)
        input_layout.addWidget(QLabel("Группа:"))
        input_layout.addWidget(self.group_input)
        input_layout.addWidget(add_button)
        self.layout.addLayout(input_layout)

    def load_data(self):
        with Session() as session:
            self.table.setRowCount(0)
            students = session.query(Student).all()
            for i, s in enumerate(students):
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(s.last_name))
                self.table.setItem(i, 1, QTableWidgetItem(s.first_name))
                self.table.setItem(i, 2, QTableWidgetItem(s.middle_name))
                self.table.setItem(i, 3, QTableWidgetItem("Мужской" if s.gender else "Женский"))
                self.table.setItem(i, 4, QTableWidgetItem(s.group.name))

    def add_student(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_name = self.middle_name_input.text()
        gender = self.gender_input.isChecked()
        group_name = self.group_input.currentText()
        with Session() as session:
            new_student = Student(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                gender=gender,
                group=session.query(Group).filter_by(name=group_name).first()
            )
            session.add(new_student)
            session.commit()
        self.load_data()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()