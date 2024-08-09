import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QSpinBox, QMessageBox
)
from pathlib import Path

class FileDestroyer(QWidget):
    def __init__(self):
        super().__init__()
        self.filenames = []
        self.initUI()

    def initUI(self):
        # Impostazioni della finestra
        self.setWindowTitle("Distruttore di File")
        self.setWindowIcon(QIcon("ico3.png"))
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("background-color: #1e1e1e; border-radius: 20px;")

        # Layout principale verticale
        main_layout = QVBoxLayout()

        # Layout orizzontale per i pulsanti di selezione
        selection_layout = QHBoxLayout()

        # Layout verticale per pulsanti selezione a destra
        button_layout = QVBoxLayout()

        # Pulsante per aprire i file
        open_file_btn = QPushButton(" Seleziona File")
        # open_file_btn.setIcon(QIcon("ico1.png"))
        open_file_btn.setFixedWidth(250)
        open_file_btn.setFixedHeight(50)
        open_file_btn.setStyleSheet(self.getButtonStyle())
        open_file_btn.clicked.connect(self.open_files)
        button_layout.addWidget(open_file_btn)

        # Pulsante per aprire la cartella
        open_folder_btn = QPushButton(" Seleziona Cartella")
        # open_folder_btn.setIcon(QIcon("ico2.png"))
        open_folder_btn.setFixedWidth(250)
        open_folder_btn.setFixedHeight(50)
        open_folder_btn.setStyleSheet(self.getButtonStyle())
        open_folder_btn.clicked.connect(self.open_folder)
        button_layout.addWidget(open_folder_btn)

        selection_layout.addLayout(button_layout)

        main_layout.addLayout(selection_layout)

        # Selettore per il numero di sovrascritture con etichetta
        spinbox_label = QLabel("Inserisci il numero di sovrascritture desiderate:")
        spinbox_label.setStyleSheet("color: #a3e4d7; font-size: 16px;")
        spinbox_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spinbox_label.setMargin(10)  # Margine tra l'etichetta e il selettore
        main_layout.addWidget(spinbox_label)

        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(1, 100)
        self.spinbox.setValue(2)
        self.spinbox.setFixedHeight(50)
        self.spinbox.setFixedWidth(400)
        self.spinbox.setStyleSheet(self.getSpinBoxStyle())
        main_layout.addWidget(self.spinbox, alignment=Qt.AlignmentFlag.AlignCenter)

        # Testo esplicativo sotto il selettore
        explanation_label = QLabel("Più volte il file viene sovrascritto e più sarà difficile recuperarlo.")
        explanation_label.setStyleSheet("color: #a3e4d7; font-size: 14px;")
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        explanation_label.setMargin(2)  # Margine tra il selettore e il testo esplicativo
        main_layout.addWidget(explanation_label)

        # Pulsante per distruggere i file
        destroy_btn = QPushButton("Distruggi File")
        destroy_btn.setFixedHeight(50)
        destroy_btn.setFixedWidth(400)
        destroy_btn.setStyleSheet(self.getButtonStyle())
        destroy_btn.clicked.connect(self.delete_files)
        main_layout.addWidget(destroy_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Messaggio di stato
        self.message = QLabel("")
        self.message.setStyleSheet("color: #a3e4d7; font-size: 18px;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.message, alignment=Qt.AlignmentFlag.AlignCenter)

        # Layout per il testo "by Tecnologiko" in basso a destra
        bottom_layout = QHBoxLayout()
        bottom_right_label = QLabel("by Tecnologiko")
        bottom_right_label.setStyleSheet("color: #a3e4d7; font-size: 12px;")
        bottom_right_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottom_layout.addStretch()
        bottom_layout.addWidget(bottom_right_label)

        # Aggiungi il layout per il testo di credito alla parte inferiore del layout principale
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()

        # Imposta il layout principale
        self.setLayout(main_layout)

    def getButtonStyle(self):
        return ("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                border-radius: 25px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)

    def getSpinBoxStyle(self):
        return ("""
            QSpinBox {
                background-color: #2c3e50;
                color: white;
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                border-radius: 25px;
                padding: 6px 12px;
                margin: 10px;
                text-align: center;
                border: 2px solid #2ecc71;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #2ecc71;
                width: 25px;
                border-radius: 10px;
                margin: 3px;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                color: white;
            }
        """)

    def open_files(self):
        self.filenames, _ = QFileDialog.getOpenFileNames(self, "Seleziona file")
        if self.filenames:
            self.message.setText('\n'.join(self.filenames))

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleziona Cartella")
        if folder:
            self.filenames = [str(p) for p in Path(folder).rglob('*') if p.is_file()]
            self.message.setText(f"Cartella selezionata: {folder}\n{len(self.filenames)} file trovati.")

    def delete_files(self):
        if not self.filenames:
            self.show_warning_message("Nessun file selezionato", "Per favore, seleziona prima i file da distruggere.")
            return
        
        reply = QMessageBox.question(
            self, "Conferma Distruzione", 
            "Sei sicuro di voler distruggere questi file?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            num = self.spinbox.value()

            for filename in self.filenames:
                path = Path(filename)
                try:
                    length = os.path.getsize(filename)
                    with open(filename, "ba+", buffering=0) as f:
                        for _ in range(num):
                            f.seek(0)
                            f.write(os.urandom(length))
                    path.unlink()
                except Exception as e:
                    self.show_error_message("Errore", f"Si è verificato un errore: {e}")
            self.message.setText("Distruzione completata con successo!")
            self.filenames = []
        else:
            self.message.setText("Operazione annullata.")

    def show_warning_message(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStyleSheet("QLabel { color: white; font-size: 18px; font-family: 'Arial', sans-serif; }"
                              "QPushButton { " + self.getButtonStyle() + " }")
        msg_box.exec()

    def show_error_message(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStyleSheet("QLabel { color: white; font-size: 18px; font-family: 'Arial', sans-serif; }"
                              "QPushButton { " + self.getButtonStyle() + " }")
        msg_box.exec()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    window = FileDestroyer()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
