import json
from PyQt5 import QtWidgets, QtGui

class iade_edilenler(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gelen Siparişler")
        self.setGeometry(710, 290, 800, 600)
        self.setStyleSheet("background-color: #f4f7fa;")  

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(20)  
        self.main_layout.setContentsMargins(15, 15, 15, 15)  
        self.title_label = QtWidgets.QLabel('İade Siparişler', self)
        self.title_label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        """)
        self.main_layout.addWidget(self.title_label)

        with open('trendyol_api\\json_file\\iade_olusturulan.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            response = data['content']

            card_container = QtWidgets.QWidget()
            card_container_layout = QtWidgets.QVBoxLayout(card_container)
            card_container_layout.setSpacing(15)  
            card_container_layout.setContentsMargins(0, 0, 0, 0) 
            if response==None:
                print('Bir hata meydana geldi')
                self.title_label.setText('Mevcut iadeniz bulunmamaktadır.')
            else:
                for a in response:
                    order_number = a['orderNumber']
                    customer_name = f"{a['customerFirstName']} {a['customerLastName']}"
                    cargo_provider = a['cargoProviderName']
                    for item in a['items']:
                        product_name = item['orderLine']['productName']
                        claim_reason = item['claimItems'][0]['trendyolClaimItemReason']['name']
                        customer_note = item['claimItems'][0]['customerNote']

                        card_widget = QtWidgets.QWidget(self)
                        card_layout = QtWidgets.QVBoxLayout(card_widget)
                        card_layout.setSpacing(12)

                        card_title = QtWidgets.QLabel(f"İade Siparişi #{order_number}", self)
                        card_title.setStyleSheet("""
                            font-size: 20px;
                            font-weight: bold;
                            color: #333;
                            margin-bottom: 15px;
                        """)
                        card_layout.addWidget(card_title)

                        customer_info = QtWidgets.QLabel(f"Müşteri: {customer_name}", self)
                        customer_info.setStyleSheet("""
                            font-size: 15px;
                            color: #666;
                            margin-bottom: 8px;
                        """)
                        card_layout.addWidget(customer_info)

                        product_info = QtWidgets.QLabel(f"Ürün: {product_name}", self)
                        product_info.setStyleSheet("""
                            font-size: 15px;
                            color: #444;
                            margin-bottom: 8px;
                        """)
                        card_layout.addWidget(product_info)

                        cargo_info = QtWidgets.QLabel(f"Kargo Sağlayıcı: {cargo_provider}", self)
                        cargo_info.setStyleSheet("""
                            font-size: 15px;
                            color: #444;
                            margin-bottom: 8px;
                        """)
                        card_layout.addWidget(cargo_info)

                        claim_info = QtWidgets.QLabel(f"İade Sebebi: {claim_reason}", self)
                        claim_info.setStyleSheet("""
                            font-size: 15px;
                            color: #007BFF;
                            margin-bottom: 8px;
                        """)
                        card_layout.addWidget(claim_info)

                        customer_note_info = QtWidgets.QLabel(f"Müşteri Mesajı: {customer_note}", self)
                        customer_note_info.setStyleSheet("""
                            font-size: 15px;
                            color: #444;
                            margin-bottom: 15px;
                        """)
                        card_layout.addWidget(customer_note_info)

                        card_widget.setStyleSheet("""
                            background-color: white;
                            border-radius: 12px;
                            border: 1px solid #e0e0e0;
                            padding: 20px;
                            margin-bottom: 15px;
                        """)

                        card_container_layout.addWidget(card_widget)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)  
        scroll_area.setWidget(card_container)
        self.main_layout.addWidget(scroll_area)
        self.setLayout(self.main_layout)
