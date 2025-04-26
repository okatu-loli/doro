from src.const_hint import StyleSheetParam


def generate_preview_css(sheet: StyleSheetParam) -> str:
    return f"""
            background-color: {sheet.get("primary")};
            border-radius: 15px;
            border: 1px solid {sheet.get("border")};
        """


def generate_message_css(colors: StyleSheetParam) -> str:
    return f"""
            QWidget#PetInfoWindowInfoWidget {{
                background-color: {colors['background']};
                border-radius: 10px;
                color: {colors['primary']};
                border: 1px solid {colors['border']};
            }}
            QLabel {{
                color: {colors['primary']};
                font-size: 12px;
                background-color: transparent;
                border: none;
            }}
        """


def generate_menu_css() -> str:
    return """
            QMenu {
            background-color: #f5f5f5;
            border: 1px solid #aaa;
            padding: 8px;
            font-size: 14px;
        }
        QMenu::item {
            padding: 6px 24px 6px 24px;
            border-radius: 6px;
        }
        QMenu::item:selected {
            background-color: #87cefa;
            color: #222;
        }
    """


def generate_full_css(colors: StyleSheetParam) -> str:
    return f"""
            QDialog {{
                background-color: {colors['background']};
            }}
            QLabel {{
                color: {colors['primary']};
                font-size: 14px;
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors['border']};
                border-radius: 5px;
                padding: 5px;
                color: {colors['text']};
            }}
            QSpinBox {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors['border']};
                border-radius: 5px;
                padding: 5px;
                color: {colors['text']};
            }}
            QPushButton {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {colors['primary']};
            }}
            QCheckBox {{
                color: {colors['primary']};
            }}
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors['border']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors['primary']};
                border: 1px solid {colors['border']};
                border-radius: 3px;
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors['border']};
                border-radius: 5px;
                padding: 5px;
                color: {colors['text']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {colors['primary']};
                margin-right: 5px;
            }}
        """
