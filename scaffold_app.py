from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QScrollArea, QWidget as QScrollWidget,
    QApplication, QMessageBox  # Import QMessageBox for displaying messages
)
from widgets import LabeledComboBox, LabeledLineEdit, ColumnInputWidget
from migration_generator import MigrationGenerator
from styles import apply_styles

class ScaffoldApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gerador de Scaffold')
        self.setGeometry(100, 100, 600, 600)

        # Create a container widget for the scroll area
        container_widget = QScrollWidget()
        container_layout = QVBoxLayout(container_widget)

        self.inflection_input = LabeledComboBox('Você olhou sua inflection?:', ["NÃO", "SIM"])
        self.inflection_input.combo.currentIndexChanged.connect(self.check_conditions)
        container_layout.addWidget(self.inflection_input)

        self.database_input = LabeledComboBox('Você olhou seu database?:', ["NÃO", "SIM"])
        self.database_input.combo.currentIndexChanged.connect(self.check_conditions)
        container_layout.addWidget(self.database_input)

        self.model_input = LabeledLineEdit('Escreva sua model:')
        self.model_input.line_edit.setEnabled(False)
        container_layout.addWidget(self.model_input)

        self.inflection_plural_label = QLabel('Inflection no plural:')
        self.inflection_plural_label.setVisible(False)
        container_layout.addWidget(self.inflection_plural_label)

        self.inflection_plural_input = QLineEdit()
        self.inflection_plural_input.setVisible(False)
        container_layout.addWidget(self.inflection_plural_input)

        self.colunas_layout = QVBoxLayout()
        container_layout.addLayout(self.colunas_layout)

        self.add_coluna_button = QPushButton('Adicionar Coluna')
        self.add_coluna_button.setEnabled(False)
        self.add_coluna_button.clicked.connect(self.add_coluna)
        container_layout.addWidget(self.add_coluna_button)

        self.remove_coluna_button = QPushButton('Remover Coluna')
        self.remove_coluna_button.setEnabled(False)
        self.remove_coluna_button.clicked.connect(self.remove_coluna)
        container_layout.addWidget(self.remove_coluna_button)

        self.generate_button = QPushButton('Gerar Scaffold')
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_scaffold)
        container_layout.addWidget(self.generate_button)

        self.command_output = QTextEdit()
        self.command_output.setPlaceholderText("O comando scaffold gerado será exibido aqui...")
        self.command_output.setReadOnly(True)
        container_layout.addWidget(self.command_output)

        self.migration_output = QTextEdit()
        self.migration_output.setPlaceholderText("O conteúdo do arquivo de migração gerado será exibido aqui...")
        self.migration_output.setReadOnly(True)
        container_layout.addWidget(self.migration_output)

        # Copy buttons
        self.copy_command_button = QPushButton('Copiar Comando')
        self.copy_command_button.clicked.connect(self.copy_command_output)
        container_layout.addWidget(self.copy_command_button)

        self.copy_migration_button = QPushButton('Copiar Migração')
        self.copy_migration_button.clicked.connect(self.copy_migration_output)
        container_layout.addWidget(self.copy_migration_button)

        # Create a scroll area and set the container widget as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container_widget)

        # Set the scroll area as the layout of the main widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        apply_styles(self)

    def check_conditions(self):
        enable = self.inflection_input.combo.currentText() == "SIM" and self.database_input.combo.currentText() == "SIM"
        self.model_input.line_edit.setEnabled(enable)
        self.add_coluna_button.setEnabled(enable)
        self.generate_button.setEnabled(enable)
        self.remove_coluna_button.setEnabled(enable)
        self.inflection_plural_label.setVisible(enable)
        self.inflection_plural_input.setVisible(enable)

    def add_coluna(self):
        coluna_widget = ColumnInputWidget()
        self.colunas_layout.addWidget(coluna_widget)

    def remove_coluna(self):
        if self.colunas_layout.count() > 0:
            widget = self.colunas_layout.itemAt(self.colunas_layout.count() - 1).widget()
            if widget:
                widget.deleteLater()

    def generate_scaffold(self):
        model = self.model_input.line_edit.text()

        colunas = []
        migration_columns = []
        for i in range(self.colunas_layout.count()):
            coluna_widget = self.colunas_layout.itemAt(i).widget()
            nome_coluna = coluna_widget.nome_coluna_input.text()
            tipo_coluna = coluna_widget.tipo_coluna_input.currentText()
            colunas.append(f"{nome_coluna}:{tipo_coluna}")
            migration_columns.append((nome_coluna, tipo_coluna))

        comando = f"rails g scaffold {model} " + " ".join(colunas) + " deleted_at:datetime updated_by:string created_by:string "

        # Exibir o comando scaffold na área de texto
        self.command_output.setPlainText(comando)

        # Chama a função para gerar o conteúdo da migração
        migration_generator = MigrationGenerator()
        migration_content = self.generate_migration_content(migration_generator, model, migration_columns)

        # Exibir o conteúdo da migração na área de texto
        self.migration_output.setPlainText(migration_content)

    def generate_migration_content(self, migration_generator, model, columns):
        table_name = self.inflection_plural_input.text()
        return migration_generator.generate_migration_file(model, columns, table_name)

    def copy_command_output(self):
        clipboard = QApplication.clipboard()  # Get the clipboard instance
        clipboard.setText(self.command_output.toPlainText())  # Set the command output text to clipboard
        self.show_message("Copiado com sucesso!")  # Show success message

    def copy_migration_output(self):
        clipboard = QApplication.clipboard()  # Get the clipboard instance
        clipboard.setText(self.migration_output.toPlainText())  # Set the migration output text to clipboard
        self.show_message("Copiado com sucesso!")  # Show success message

    def show_message(self, message):
        QMessageBox.information(self, "Informação", message)  # Show a message box with the given message

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ScaffoldApp()
    window.show()
    sys.exit(app.exec_())
