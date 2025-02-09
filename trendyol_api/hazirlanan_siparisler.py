import json
from PyQt5 import QtWidgets, QtCore
from trendyol_api.trendyol_servis import Trendyol

class hazirStatusundaOlanlar_cls(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.td = Trendyol()
        page = self.td.hazirlanan_siparisler()
        self.setWindowTitle("Pakat Hazırlanıyor")
        self.setGeometry(710, 290, 700, 700)

    #Hazırlanan siparişler adet bazında listelemek için kullanılıyor
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
        toplam_kitap_adeti=0
        for a in siparis_kitap:
            print(f"{a['kitap_adet']} x {a['kitap_isim']}x{a['kitap_barkod']}")
            toplam_kitap_adeti+=a['kitap_adet']

        main_layout = QtWidgets.QVBoxLayout(self)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_content_widget = QtWidgets.QWidget()
        scroll_content_layout = QtWidgets.QVBoxLayout(scroll_content_widget)

        for a in page['content']:
            product_info_widget = QtWidgets.QWidget()
            product_info_layout = QtWidgets.QVBoxLayout(product_info_widget)

            product_name_label = QtWidgets.QLabel(f"Kullanıcı: {a['shipmentAddress']['firstName']} {a['shipmentAddress']['lastName']}")
            product_info_layout.addWidget(product_name_label)

            siparis_numarasi = QtWidgets.QLabel(f"Sipariş Numarası: {a['orderNumber']}")
            product_info_layout.addWidget(siparis_numarasi)

            Kargo_sirekti = QtWidgets.QLabel(f"Kargo Şirekti: {a['cargoProviderName']}")
            product_info_layout.addWidget(Kargo_sirekti)

            shipmentPackageStatus = QtWidgets.QLabel(f"Paket Durumu: <strong>{a['shipmentPackageStatus'].replace('Picking','Toplamaya Başlandı')}</strong>")
            shipmentPackageStatus.setStyleSheet('color:red;')
            product_info_layout.addWidget(shipmentPackageStatus)

            adres = QtWidgets.QLabel(f"Adres: {a['shipmentAddress']['fullAddress']}")
            product_info_layout.addWidget(adres)

            for deger in a['lines']:
                ürün=QtWidgets.QLabel(f'<strong style="color:red;">{deger['quantity']} x </strong><strong style="color:red;"><u>{deger['productName']}</u></strong> Barkod :{deger['barcode']} Stok Kodu: {deger['sku']}')
                product_info_layout.addWidget(ürün)
                # print('quantity :', deger['quantity'])
                # print('productName :', deger['productName'])
                # print('productCode :', deger['productCode'])
                # print('sku :', deger['sku'])
                # print('barcode :', deger['barcode'])
                # print('orderLineItemStatusName :', deger['orderLineItemStatusName'])
                # print('price :', deger['price'])
                # print('--------------------\n')

            scroll_content_layout.addWidget(product_info_widget)
        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = hazirStatusundaOlanlar_cls()
    window.show()
    app.exec_()
