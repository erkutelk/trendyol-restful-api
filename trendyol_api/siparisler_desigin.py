import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

class Siparis_design(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gelen Siparişler")
        self.setGeometry(710, 290, 600, 600)
        self.setStyleSheet("background-color: #f7f9fc;")  
        
        self.main_layout = QtWidgets.QVBoxLayout()

        self.title_label = QtWidgets.QLabel('Gelen Siparişler', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 15px;")
        self.main_layout.addWidget(self.title_label)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #f7f9fc;")  

        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(self.main_layout)

        scroll_area.setWidget(container_widget)
        
        main_layout_outer = QtWidgets.QVBoxLayout(self)
        main_layout_outer.addWidget(scroll_area)

        self.setLayout(main_layout_outer)

        self.json_read()

    def json_read(self):
        try:
            with open('trendyol_api\\json_file\\siparisler.json', 'r', encoding='utf-8') as file:
                deger = json.load(file)
                deger_object = deger['content']
                self.siparis_oku(deger, deger_object)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            error_label = QtWidgets.QLabel("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", self)
            error_label.setStyleSheet('color: red; font-size: 16px; padding: 10px; border-radius: 5px; background-color: #f8d7da;')
            self.main_layout.addWidget(error_label)

    def siparis_oku(self, deger, deger_object):
        if int(deger['totalElements']) > 0:
            for a in deger_object:
                self.siparis_detay(a)
                for lines in a['lines']:
                    self.urun_bilgileri(lines)
                self.fatura_turu(a['commercial'])
        else:
            no_order_label = QtWidgets.QLabel("Siparişiniz yoktur✔", self)
            self.main_layout.addWidget(no_order_label)
            no_order_label.setStyleSheet('padding-left:220px; background-color:#DBF227;')

    def siparis_detay(self, a):
        customer_layout = QtWidgets.QVBoxLayout()

        name_label = QtWidgets.QLabel(f"Adı: {a['shipmentAddress']['firstName']} {a['shipmentAddress']['lastName']}", self)
        name_label.setStyleSheet('font-size: 14px; color: white; padding: 8px; border-radius: 5px; background-color: #0056B3;')
        name_label.setWordWrap(True)  
        customer_layout.addWidget(name_label)

        address_label = QtWidgets.QLabel(f"Adres: {a['shipmentAddress']['fullAddress']}", self)
        address_label.setStyleSheet('font-size: 14px; color: black; padding: 8px; border-radius: 5px; background-color: #ffffff;')
        address_label.setWordWrap(True)  
        customer_layout.addWidget(address_label)

        siparis_numarasi = QtWidgets.QLabel(f"Sipariş No: {a['orderNumber']}", self)
        siparis_numarasi.setStyleSheet('font-size: 14px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        customer_layout.addWidget(siparis_numarasi)

        siparis_numarasi = QtWidgets.QLabel(f"Sipariş Tarihi: {a['orderDate']}", self)
        siparis_numarasi.setStyleSheet('font-size: 14px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        customer_layout.addWidget(siparis_numarasi)
        
        siparis_numarasi = QtWidgets.QLabel(f"Kargo No: {a['cargoTrackingNumber']}", self)
        siparis_numarasi.setStyleSheet('font-size: 14px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        customer_layout.addWidget(siparis_numarasi)

        customer_widget = QtWidgets.QWidget()
        customer_widget.setLayout(customer_layout)
        self.main_layout.addWidget(customer_widget)

    def urun_bilgileri(self, lines):
        product_layout = QtWidgets.QVBoxLayout()  # Ana düzen dikey olacak

        product_name_label = QtWidgets.QLabel(f"{lines['productName']}", self)
        product_name_label.setStyleSheet('font-size: 13px; color: black; font-weight: bold; padding: 10px; background-color: #ffffff; border-radius: 8px;')
        product_name_label.setWordWrap(True)
        product_layout.addWidget(product_name_label)

        barcode_label = QtWidgets.QLabel(f"Barkod: {lines['barcode']}", self)
        barcode_label.setStyleSheet('font-size: 13px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        barcode_label.setWordWrap(True)
        product_layout.addWidget(barcode_label)

        price_label = QtWidgets.QLabel(f"Fiyat: {lines['price']} TL", self)
        price_label.setStyleSheet('font-size: 13px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        product_layout.addWidget(price_label)

        quantity_label = QtWidgets.QLabel(f"Adet: {lines['quantity']}", self)
        quantity_label.setStyleSheet('font-size: 13px; color: black; padding: 8px; background-color: #ffffff; border-radius: 5px;')
        product_layout.addWidget(quantity_label)

        # Başarı Stok ve Başarı Fiyat için yeni yatay bir layout oluşturuyoruz
        success_layout = QtWidgets.QHBoxLayout()

        # self.basari_stok = QtWidgets.QLabel('Başarı Stok: 5', self)
        # self.basari_stok.setStyleSheet('font-size: 14px; color: black; font-weight: bold; padding: 8px; background-color: #ecf0f1; border-radius: 5px;')
        # success_layout.addWidget(self.basari_stok)
        # self.basari_stok.setFixedWidth(948)  

        # self.başarı_fiyat = QtWidgets.QLabel('Başarı Fiyat: 99$', self)
        # self.başarı_fiyat.setStyleSheet('font-size: 14px; color: black; font-weight: bold; padding: 8px; background-color: #ecf0f1; border-radius: 5px;')
        # success_layout.addWidget(self.başarı_fiyat)
        # self.başarı_fiyat.setFixedWidth(948)

        # self.siparisi_hazirla = QtWidgets.QPushButton('Siparişi Hazırla', self)
        # self.siparisi_hazirla.setStyleSheet('font-size: 14px; color: black; font-weight: bold; padding: 8px; background-color: #ecf0f1; border-radius: 5px;')
        # success_layout.addWidget(self.siparisi_hazirla)
        # self.siparisi_hazirla.setFixedWidth(948)

        # Başarı Stok ve Başarı Fiyat'ı ana dikey layout'a ekliyoruz
        product_layout.addLayout(success_layout)

        # Ürün widget'ını oluşturup ekliyoruz
        product_widget = QtWidgets.QWidget()
        product_widget.setLayout(product_layout)
        self.main_layout.addWidget(product_widget)


        # self.siparisi_hazirla.clicked.connect(lambda: self.siparisi_hazirla_dialog(deger_object[0]))
        



    def fatura_turu(self, durum):
        invoice_layout = QtWidgets.QHBoxLayout()
        
        invoice_type = 'Kurumsal Fatura' if durum else 'Varsayılan Fatura'
        
        invoice_label = QtWidgets.QLabel(f"{invoice_type}", self)
        invoice_label.setStyleSheet('font-size: 14px; color: black; font-weight: bold; padding: 8px; background-color: #ecf0f1; border-radius: 5px;')
        
        invoice_layout.addWidget(invoice_label)
        # invoice_layout.addWidget(self.basari_stok)
        # invoice_layout.addWidget(self.başarı_fiyat)

        invoice_widget = QtWidgets.QWidget()
        invoice_widget.setLayout(invoice_layout)
        invoice_widget.setFixedWidth(600)

        # Ana layout'a widget ekleniyor
        self.main_layout.addWidget(invoice_widget)
        self.main_layout.addStretch(1)
    
    def resizeEvent(self, event):
        """
        Handle window resizing.
        """
        self.updateGeometry()
        super().resizeEvent(event)
