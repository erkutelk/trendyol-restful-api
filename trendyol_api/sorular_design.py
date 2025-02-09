import json
from PyQt5 import QtWidgets
''''Soruların gösterileceği sayfa'''
class SecondWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gelen Sorular")
        self.setGeometry(710, 290, 600, 600)

        self.label2 = QtWidgets.QLabel('Trendyol>Gelen Sorular', self)
        self.label2.setStyleSheet('font-size:10px;')
        self.label2.move(0, 10)
        oran = 100
        with open('trendyol_api\\json_file\\sorular.json', 'r', encoding='utf-8') as file:
            deger = json.load(file)
            deger_object = deger['content']
            if int(deger['totalElements'])>0:
                for a in deger_object:
                    layout=QtWidgets.QVBoxLayout()
                    soru_label = QtWidgets.QLabel(self)
                    soru_label.setText(f'{a["text"]}')
                    soru_label.adjustSize()
                    soru_label.setGeometry(3, oran, 250, 30)
                    soru_label.setStyleSheet('font-size:15px;color:#0D0D0D;')
                    soru_label.setFixedWidth(1000)
                    layout.addWidget(soru_label)
                    
                    ürün_label = QtWidgets.QLabel(self)
                    ürün_label.setText(f'{a["productName"]}')
                    ürün_label.adjustSize()
                    ürün_label.setGeometry(3, oran+20, 250, 30)
                    ürün_label.setStyleSheet('font-size:12px;color:#737373;')
                    ürün_label.setFixedWidth(1000)
                    layout.addWidget(ürün_label)


                    product_label2 = QtWidgets.QLabel(self)
                    product_label2.setText(f'{a["webUrl"]}')
                    product_label2.adjustSize()
                    product_label2.setGeometry(3, oran+40, 250, 30)
                    product_label2.setStyleSheet('font-size:12px;color:#737373;')
                    product_label2.setFixedWidth(1000)
                    layout.addWidget(product_label2)
                    oran += 80
            else:
                question_label = QtWidgets.QLabel(self)
                question_label.setText('✔Bütün sorular cevaplandı.')
                question_label.adjustSize()
                question_label.setGeometry(3, oran, 250, 30)
                question_label.setStyleSheet('font-size:25px;color:#021526; background-color:#0FF247; border-radius:5px; padding-left:150px;')
                question_label.setFixedWidth(600)

if __name__=='__main__':
    app=QtWidgets.QApplication([])
    window=SecondWindow()
    window.show()
    app.exec_()