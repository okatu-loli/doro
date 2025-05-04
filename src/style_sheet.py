from .auto_typehint import ThemeHint


def generate_preview_css(sheet: ThemeHint.ThemeParam) -> str:
    return f"""
            background-color: {sheet.get("primary")};
            border-radius: 15px;
            border: 1px solid {sheet.get("border")};
        """


def generate_pet_info_css(colors: ThemeHint.ThemeParam) -> str:
    return f"""
            QWidget#PetInfoWindowInfoWidget {{
                background-color: {colors.get("background")};
                border-radius: 10px;
                color: {colors.get("primary")};
                border: 1px solid {colors.get("border")};
            }}
            QLabel {{
                color: {colors.get("primary")};
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
            color: black;
        }
        QMenu::item:selected {
            background-color: #87cefa;
            color: #222;
        }
    """


def generate_messagebox_css() -> str:
    return """
    QMessageBox {
        background-color: #fdf5fe; /* 淡灰色背景 */
    }
    QLabel { /* 调整文本标签样式 */
        color: #ef5aad; /* 深灰色文本 */
        font-size: 13px; /* 稍大字体 */
    }
    QPushButton { /* 按钮样式 */
        background-color: #f771c8;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        min-width: 60px;
    }
    QPushButton:hover {
        background-color: #f282cb;
    }
    """


def generate_full_css(colors: ThemeHint.ThemeParam) -> str:
    return f"""
            QDialog {{
                background-color: {colors.get("background")};
            }}
            QLabel {{
                color: {colors.get('primary')};
                font-size: 14px;
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors.get('border')};
                border-radius: 5px;
                padding: 5px;
                color: {colors.get('text')};
            }}
            QSpinBox {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors.get('border')};
                border-radius: 5px;
                padding: 5px;
                color: {colors.get('text')};
            }}
            QPushButton {{
                background-color: {colors.get('primary')};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors.get('secondary')};
            }}
            QPushButton:pressed {{
                background-color: {colors.get('primary')};
            }}
            QCheckBox {{
                color: {colors.get('primary')};
            }}
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors.get('border')};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors.get('primary')};
                border: 1px solid {colors.get('border')};
                border-radius: 3px;
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid {colors.get('border')};
                border-radius: 5px;
                padding: 5px;
                color: {colors.get('text')};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {colors.get('primary')};
                margin-right: 5px;
            }}
        """
