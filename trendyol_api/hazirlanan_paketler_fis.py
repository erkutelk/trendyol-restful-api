import json
from PyQt5 import QtWidgets, QtCore
from trendyol_api.trendyol_servis import Trendyol

class hazirlanan_paketler_fis_cls(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.td = Trendyol()
        page = self.td.hazirlanan_siparisler()
        self.setWindowTitle("Hakat Hazırlanıyor")
        self.setGeometry(710, 290, 700, 700)
        main_layout = QtWidgets.QVBoxLayout(self)

        try:
            siparis_kitap = []
            fl = page
            for a in fl['content']:
                for urun in a['lines']:
                    kitap_var = False
                    for item in siparis_kitap:
                        if item['kitap_barkod'] == urun['barcode']:
                            item['kitap_adet'] += urun['quantity']
                            kitap_var = True
                            break
                    if not kitap_var:
                        siparis_kitap.append({
                            'kitap_isim': urun['productName'],
                            'kitap_barkod': urun['barcode'],
                            'kitap_adet': urun['quantity']
                        })
        except Exception as e:
            print('Hatası Meydana geldi')

        table = QtWidgets.QTableWidget(self)
        table.setRowCount(len(siparis_kitap)) 
        table.setColumnCount(3)  

        table.setHorizontalHeaderLabels(["Kitap İsmi", "Barkod", "Adet"])

        for row, a in enumerate(siparis_kitap):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(a['kitap_isim']))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(a['kitap_barkod']))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(a['kitap_adet'])))

        main_layout.addWidget(table)

        toplam_kitap_adeti = sum(a['kitap_adet'] for a in siparis_kitap)

        toplam_text_browser = QtWidgets.QLabel(f"<strong>Toplam Kitap Adedi: {toplam_kitap_adeti}</strong>")
        toplam_text_browser.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(toplam_text_browser)

        max_kitap = max(siparis_kitap, key=lambda x: x['kitap_adet'])
        max_kitap_isim = max_kitap['kitap_isim']
        max_kitap_adet = max_kitap['kitap_adet']

        max_kitap_label = QtWidgets.QLabel(f"<strong>En Fazla Olan Kitap: {max_kitap_isim} - Adet: {max_kitap_adet}</strong>")
        max_kitap_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(max_kitap_label)

        copy_button = QtWidgets.QPushButton("Tabloyu Kopyala", self)
        copy_button.clicked.connect(self.button_kopyalama)
        main_layout.addWidget(copy_button)

    def button_kopyalama(self):
        table_data = ""
        for row in range(self.findChild(QtWidgets.QTableWidget).rowCount()):
            for col in range(self.findChild(QtWidgets.QTableWidget).columnCount()):
                table_data += self.findChild(QtWidgets.QTableWidget).item(row, col).text() + "~\t"
            table_data = table_data.strip() + " \n~ "
        
        QtWidgets.QApplication.clipboard().setText(table_data)
        print("Tablo verisi panoya kopyalandı.")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = hazirlanan_paketler_fis_cls()
    window.show()
    app.exec_()
