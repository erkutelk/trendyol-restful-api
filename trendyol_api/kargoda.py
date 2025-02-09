import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtCore import Qt
from trendyol_api.trendyol_servis import Trendyol

class kargoda_olan_urunler(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.td = Trendyol()
        self.setWindowTitle("Kargoda Olan Ürünler")
        self.setGeometry(710, 290, 900, 700)

        self.setStyleSheet("""
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        """)

        main_layout = QtWidgets.QVBoxLayout()
        scroll_area = QtWidgets.QScrollArea()
        scroll_content = QtWidgets.QWidget()

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.setLayout(main_layout)

        print(f'Kargoda olan sipariş adeti')
        response_value = self.td.tasima_durumuna_gecen_siparisler()

        for a in response_value['content']:
            user_card = QtWidgets.QWidget()
            user_card.setStyleSheet("""
                background-color: white; 
                border-radius: 15px; 
                padding: 20px; 
                margin-bottom: 20px;
                border: 1px solid #e0e0e0;
            """)
            user_layout = QtWidgets.QVBoxLayout(user_card)

            kullanici = QtWidgets.QLabel(f"<b>Kullanıcı:</b> {a['shipmentAddress']['firstName']} {a['shipmentAddress']['lastName']}")
            kullanici.setStyleSheet("font-size: 16px; color: #2c3e50; font-weight: bold;")
            user_layout.addWidget(kullanici)

            adres = QtWidgets.QLabel(f"<strong>Adres:</strong> {a['shipmentAddress']['fullAddress']}")
            adres.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-top: 8px;")
            user_layout.addWidget(adres)

            siparis_numarasi = QtWidgets.QLabel(f"<b>Sipariş Numarası:</b> {a['orderNumber']} - {a['cargoTrackingNumber']}")
            siparis_numarasi.setStyleSheet("font-size: 14px; color: #2980b9; margin-top: 8px;")
            user_layout.addWidget(siparis_numarasi)

            for b in a['lines']:
                line_widget = QtWidgets.QWidget()
                line_widget.setStyleSheet("""
                    background-color: #ecf0f1; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-top: 12px;
                """)
                line_layout = QtWidgets.QHBoxLayout(line_widget)

                adet = QtWidgets.QLabel(f"<b>Adet:</b> {b['quantity']}")
                adet.setStyleSheet("font-size: 14px; margin-right: 20px;")
                line_layout.addWidget(adet)

                market_stok_kodu = QtWidgets.QLabel(f"<b>Stok Kodu:</b> {b['merchantSku']}")
                market_stok_kodu.setStyleSheet("font-size: 14px; margin-right: 20px;")
                line_layout.addWidget(market_stok_kodu)

                kitap_name = QtWidgets.QLabel(f"<b>Ürün Adı:</b> {b['productName']}")
                kitap_name.setStyleSheet("font-size: 14px;")
                line_layout.addWidget(kitap_name)

                user_layout.addWidget(line_widget)

            scroll_layout.addWidget(user_card)

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = kargoda_olan_urunler()
    window.show()
    app.exec_()
