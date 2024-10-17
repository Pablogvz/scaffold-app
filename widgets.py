from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QHBoxLayout
import scaffold_app

class LabeledComboBox(QWidget):
    def __init__(self, label_text, items):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(label_text)
        layout.addWidget(self.label)
        self.combo = QComboBox()
        self.combo.addItems(items)
        layout.addWidget(self.combo)
        self.setLayout(layout)

class LabeledLineEdit(QWidget):
    def __init__(self, label_text):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(label_text)
        layout.addWidget(self.label)
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

class ColumnInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.nome_coluna_input = QLineEdit()
        self.nome_coluna_input.setPlaceholderText('Nome da Coluna')
        layout.addWidget(self.nome_coluna_input)

        self.tipo_coluna_input = QComboBox()
        self.tipo_coluna_input.addItems(["string", "integer", "date", "datetime", "boolean", "references", "text", "float", "double"])
        layout.addWidget(self.tipo_coluna_input)

        self.setLayout(layout)
