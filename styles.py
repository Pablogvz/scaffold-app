def apply_styles(app):
    app.setStyleSheet("""
        QWidget {
            font-size: 14px;
        }

        QLabel {
            color: #333;
        }

        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 5px;
        }

        QComboBox {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 5px;
        }

        QPushButton {
            background-color: #007aff;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
        }

        QPushButton:disabled {
            background-color: #cccccc;
            color: white;
        }
    """)
