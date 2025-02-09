from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
import json
from  trendyol_api.trendyol_servis import Trendyol
class SiparisHazirlaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.trendyol=Trendyol()
        if self.trendyol.siparisler()>0:
            print(f'{self.trendyol.siparisler()} adet trendyol siparişiniz bulunmakta.')
        else:
            print('Trendyol siparişi yoktur')
        self.setWindowTitle("Siparişi Hazırla")
        self.setGeometry(750, 350, 600, 500)
        self.tasarim()  
        self.json_read()



    def tasarim(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_label = QtWidgets.QLabel("Sipariş Bilgileri", self)
        header_label.setStyleSheet('font-size:20px; font-weight: bold; color: #2C3E50; background-color:white;')
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        self.yenile_page=QtWidgets.QPushButton('Yenile',self)
        self.yenile_page.setFixedSize(50,20)
        main_layout.addWidget(self.yenile_page)

        self.yenile_page.clicked.connect(self.basari_tarafi_istenilen_siparisler)
        
        

        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setColumnCount(3) 
        self.table_widget.setHorizontalHeaderLabels(["Kitap", "Adet", "Barkod"])
        self.table_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  
        self.table_widget.setSortingEnabled(True)

        self.table_widget.setColumnWidth(0, 181) 
        self.table_widget.setColumnWidth(1, 181)  
        self.table_widget.setColumnWidth(2, 181)  

        main_layout.addWidget(self.table_widget)



    def basari_tarafi_istenilen_siparisler(self):
        print(f'{self.trendyol.siparisler()} siparişiniz mevcuz')
        self.json_read()

    def json_read(self):
        try:
            siparis_kitap = []
            with open('trendyol_api\\json_file\\siparisler.json', 'r', encoding='utf-8') as file:
                fl = json.load(file)

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
                
                self.tablo_widget(siparis_kitap)

        except Exception as e:
            print(f"Bir hata oluştu {e}")

    def tablo_widget(self, siparis_kitap):
        self.table_widget.setRowCount(len(siparis_kitap))

        for row, a in enumerate(siparis_kitap):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(a['kitap_isim']))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a['kitap_adet'])))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(a['kitap_barkod']))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SiparisHazirlaDialog()
    window.show()
    app.exec_()
