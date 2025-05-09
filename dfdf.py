import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFileDialog,
    QPushButton, QComboBox, QMessageBox
)
import sys

# Create required folders if they don't exist
os.makedirs("system_LD/apk", exist_ok=True)
os.makedirs("system_LD/txt", exist_ok=True)
os.makedirs("system_LD/Viseo", exist_ok=True)
os.makedirs("system_LD/image", exist_ok=True)

class ComboSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        # ComboBox for selecting action
        self.selection_combo = QComboBox()
        self.selection_combo.addItems([
            "Select Folder",
            "Select .txt File",
            "Select .apk File",
            "Select .Viseo File",
            "Select .image File"
        ])
        self.layout.addWidget(self.selection_combo)

        # Browse Button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_selection)
        self.layout.addWidget(self.browse_button)

        # ComboBox to display added paths
        self.lD_nami = QComboBox()
        self.layout.addWidget(self.lD_nami)

        # Delete Button
        self.delete_button = QPushButton("Delete Selected Item")
        self.delete_button.clicked.connect(self.delete_name)
        self.layout.addWidget(self.delete_button)

        # Set style
        self.setStyleSheet("""
            QWidget {
                font-family: "Times New Roman";
                font-size: 13px;
                color: white;
                background-color: #333;
            }
            QPushButton, QSpinBox, QComboBox, QRadioButton, QCheckBox {
                font-family: "Times New Roman";
                font-size: 13px;
                color: white;
                background-color: #555;
                border: 1px solid #888;
                padding: 5px;
            }
            QPushButton:hover, QComboBox:hover, QRadioButton:hover, QCheckBox:hover {
                background-color: #777;
            }
            QTableWidget {
                font-family: "Times New Roman";
                font-size: 13px;
                color: white;
                background-color: #444;
                border: 1px solid #888;
            }
        """)

        self.setLayout(self.layout)
        self.load_data()

    def browse_selection(self):
        selection = self.selection_combo.currentText()

        if selection == "Select Folder":
            self.select_folder()
        elif selection == "Select .txt File":
            self.select_file(".txt")
        elif selection == "Select .apk File":
            self.select_file(".apk")
        elif selection == "Select .Viseo File":
            self.select_file(".mp4")  # You can allow more formats if needed
        elif selection == "Select .image File":
            self.select_file(".png", extra_formats=[".jpg", ".jpeg"])

    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path and path not in [self.lD_nami.itemText(i) for i in range(self.lD_nami.count())]:
            self.lD_nami.addItem(f"Folder: {path}")
            self.lD_nami.setCurrentText(f"Folder: {path}")
            self.save_data()

    def select_file(self, main_ext, extra_formats=None):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if extra_formats:
            formats = [f"*{main_ext}"] + [f"*{ext}" for ext in extra_formats]
            filter_string = "Files (" + " ".join(formats) + ")"
        else:
            filter_string = f"Files (*{main_ext})"
        file_dialog.setNameFilter(filter_string)

        if file_dialog.exec_():
            files = file_dialog.selectedFiles()
            for file_path in files:
                if file_path and file_path not in [self.lD_nami.itemText(i) for i in range(self.lD_nami.count())]:
                    file_type_name = main_ext[1:].upper() + " File"
                    self.lD_nami.addItem(f"{file_type_name}: {file_path}")
            if files:
                self.lD_nami.setCurrentText(f"{main_ext[1:].upper()} File: {files[0]}")
            self.save_data()

    def save_data(self):
        os.makedirs("NewFolder", exist_ok=True)
        file_path = os.path.join("NewFolder", "main.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            for i in range(self.lD_nami.count()):
                text = self.lD_nami.itemText(i).strip()
                if text:
                    file.write(text + "\n")

    def load_data(self):
        file_path = os.path.join("NewFolder", "main.txt")
        if os.path.exists(file_path):
            existing = set(self.lD_nami.itemText(i).strip() for i in range(self.lD_nami.count()))
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    path = line.strip()
                    if path and path not in existing:
                        self.lD_nami.addItem(path)

    def delete_name(self):
        selected_name = self.lD_nami.currentText()
        if selected_name:
            reply = QMessageBox.question(self, 'Confirm Delete',
                                         f"Are you sure you want to delete {selected_name}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                index = self.lD_nami.findText(selected_name)
                self.lD_nami.removeItem(index)
                self.save_data()
                print(f"✔️ {selected_name} has been deleted and saved successfully.")
            else:
                print("⚠️ Deletion cancelled.")
        else:
            print("⚠️ No item selected to delete.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComboSwitcher()
    window.show()
    sys.exit(app.exec_())
