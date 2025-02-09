import json
from PyQt5 import QtWidgets, QtCore
from trendyol_api.trendyol_servis import Trendyol

class musteriye_ulasmayan_siparis_cls(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.td = Trendyol()
        page = self.td.musteriye_ulasmayan_siparisler()
        self.setWindowTitle("Gelen Sorular")
        self.setGeometry(710, 290, 700, 700)

        self.label2 = QtWidgets.QLabel('Trendyol > Gelen Sorular', self)
        self.label2.move(20, 20)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_content)

        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(25)  
        for a in page['content']:
            user_info_widget = QtWidgets.QWidget()
            user_info_layout = QtWidgets.QVBoxLayout(user_info_widget)

            user_label = QtWidgets.QLabel(f"Kullanıcı: {a['shipmentAddress']['firstName']} {a['shipmentAddress']['lastName']}")
            user_info_layout.addWidget(user_label)

            address_label = QtWidgets.QLabel(f"Adres: {a['shipmentAddress']['fullAddress']}")
            address_label.setStyleSheet("font-size: 12px; color: #666;")
            user_info_layout.addWidget(address_label)

            order_number_label = QtWidgets.QLabel(f"Sipariş Numarası: {a['orderNumber']}")
            user_info_layout.addWidget(order_number_label)

            cargo_tracking_label = QtWidgets.QLabel(f"Kargo Takip Linki: {a['cargoTrackingLink']}")
            user_info_layout.addWidget(cargo_tracking_label)

            cargo_sender_number_label = QtWidgets.QLabel(f"Kargo Gönderen Numarası: {a['cargoSenderNumber']}")
            user_info_layout.addWidget(cargo_sender_number_label)

            cargo_provider_label = QtWidgets.QLabel(f"Kargo Sağlayıcı: {a['cargoProviderName']}")
            user_info_layout.addWidget(cargo_provider_label)

            scroll_layout.addWidget(user_info_widget) 

            for deger in a['lines']:
                product_info_widget = QtWidgets.QWidget()
                product_info_layout = QtWidgets.QVBoxLayout(product_info_widget)
                product_name_label = QtWidgets.QLabel(f"Ürün Adı: {deger['productName']}")
                product_info_layout.addWidget(product_name_label)
                product_code_label = QtWidgets.QLabel(f"Ürün Kodu: {deger['productCode']}")
                product_info_layout.addWidget(product_code_label)
                quantity_label = QtWidgets.QLabel(f"Adet: {deger['quantity']}")
                product_info_layout.addWidget(quantity_label)
                sales_campaign_id_label = QtWidgets.QLabel(f"Satış Kimliği: {deger['salesCampaignId']}")
                product_info_layout.addWidget(sales_campaign_id_label)
                merchant_sku_label = QtWidgets.QLabel(f"Market Stok Kodu: {deger['merchantSku']}")
                product_info_layout.addWidget(merchant_sku_label)
                discount_label = QtWidgets.QLabel(f"Iskonto: {deger['discount']}")
                product_info_layout.addWidget(discount_label)

                barcode_label = QtWidgets.QLabel(f"Barkod: {deger['barcode']}")
                product_info_layout.addWidget(barcode_label)

                scroll_layout.addWidget(product_info_widget)  # Add product info card

        # Total Orders Count
        total_orders_label = QtWidgets.QLabel(f"Adet Müşteriye ulaşmayan sipariş mevcut: {page['totalElements']}", self)
        scroll_layout.addWidget(total_orders_label)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = musteriye_ulasmayan_siparis_cls()
    window.show()
    app.exec_()
