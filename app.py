import json
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import datetime
import time
from main_code_basari import basari_dagitim_object
from basari_app_design import Ui_MainWindow
from trendyol_api import trendyol_servis
from main_code_basari import basari_dagitim_object

class HatirlatıcıThread(QThread):
    update_signal = pyqtSignal(str)
    
    def __init__(self, interval_seconds, parent=None):
        super().__init__(parent)
        self.interval_seconds = interval_seconds

    def run(self):
        while True:
            try:
                test=Myapp()
                basari_dagitim_object.guncellenen_kitaplar_api()
                print('Her saat başı güncellenen kitaplar excel dosyasına aktarıldı.')
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_signal.emit(current_datetime)
                print(f'Program çalıştı, {current_datetime}')
                saat_calisma=test.calisma_araliklari()

                test.show_tray_notification("Excel'e kaydedildi",f"Veriler excel'e kaydedildi, program {saat_calisma} saniyede bir çalışıcak")
                
                time.sleep(self.interval_seconds)
            except Exception as e:
                print('An error occurred:', e)
                break


class Myapp(QtWidgets.QMainWindow):
    def __init__(self):
        self.td=trendyol_servis.Trendyol()
        super(Myapp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.button_funcation()
        self.page_load()

    def page_load(self):
        #Sayfa ilk yüklendiğinde çalışacak kodlar
        try:
            self.ui.label_52.setText('0')
            saat = basari_dagitim_object.en_son_guncelleme_tarihi()
            self.ui.label_56.setText(f'{saat['Saat']}| {saat['Tarih']}')
            self.ui.label_54.setText(basari_dagitim_object.kitap_sayisi_alma())
            self.siparis_adet()
            self.toplam_soru()
            self.bekleniyor('')
            self.ui.label_5.setText('00:00:00')
            self.ui.pushButton.setEnabled(False)
            self.ui.tabWidget.setCurrentIndex(0)
            self.setup_tray_icon()
            self.hazirlanan_siparisler()
            self.yola_cikan_siparisler()
            # self.ulasmayan_siparis()
            self.iade_olusturulan()
            # self.tasima_durumuna_gecen_siparisler()
            self.ui.label_44.setText(str(self.td.musteriye_ulasmayan_siparisler()['totalElements']))


            tab_layout = self.ui.tabWidget.widget(2)  # This is the first tab
        except Exception as e:
            print('Bir hata meydana geldi',e)


    def button_funcation(self):
        # Buton fonksyionları
        self.ui.checkBox_3.stateChanged.connect(self.durum)
        self.ui.pb_guncel_veriler.clicked.connect(self.pb_guncellenen_veriler)
        self.ui.pb_stok_bilgileri.clicked.connect(self.pb_stok_bilgileri_tumu)
        self.ui.pb_fiyat_iskonto.clicked.connect(self.pb_fiyat_iskonto)
        self.ui.pb_tamamini_guncelleme.clicked.connect(self.pb_tamamini_guncelle)
        self.ui.pushButton.clicked.connect(self.hatirlatici_save)
        self.ui.pushButton_2.clicked.connect(self.open_second_window)
        self.ui.pushButton_3.clicked.connect(self.pencere_ac)
        self.ui.pushButton_8.clicked.connect(self.iade_detay_trendyol)
        self.ui.pushButton_5.clicked.connect(self.hepsiburada_siparis)
        self.ui.pushButton_9.clicked.connect(self.siparis_hazirlama_ekrani)
        self.ui.pushButton_14.clicked.connect(self.ulasmayan_siparis)
        self.ui.pushButton_15.clicked.connect(self.hazir_statu)
        self.ui.pushButton_16.clicked.connect(self.tasima_durumuna_gecen_siparisler)
        self.ui.pushButton_4.clicked.connect(self.sayfa_yenile)


    def sayfa_yenile(self):
        self.td.siparisler()
        self.td.sorular()
        self.td.hazirlanan_siparisler()
        self.td.tasima_durumuna_gecen_siparisler()
        self.td.musteriye_ulasmayan_siparisler()
        self.td.iadesi_olusturlulan()
        

    def hazir_statu(self):
        from trendyol_api.hazirlanan_siparisler import hazirStatusundaOlanlar_cls
        from trendyol_api.hazirlanan_paketler_fis import hazirlanan_paketler_fis_cls

        self.page=hazirStatusundaOlanlar_cls()
        self.page.show()

        self.deger2=hazirlanan_paketler_fis_cls()
        self.deger2.show()

    def iade_detay_trendyol(self):
        from trendyol_api.iade_design import iade_edilenler
        self.iade_edilen_respones=iade_edilenler()
        self.iade_edilen_respones.show()

    def tasima_durumuna_gecen_siparisler(self):
        from trendyol_api.kargoda import kargoda_olan_urunler
        self.deger=kargoda_olan_urunler()
        self.deger.show()

    def ulasmayan_siparis(self):
        from trendyol_api.musteriye_ulasmayan import musteriye_ulasmayan_siparis_cls
        self.deger=musteriye_ulasmayan_siparis_cls()
        self.deger.show()


    def pencere_ac(self):
        from trendyol_api.siparisler_desigin import Siparis_design
        if not hasattr(self, 'siparisler_window') or not self.siparisler_window.isVisible():
            self.siparisler_window = Siparis_design()
            self.siparisler_window.show()
        else:
            self.siparisler_window.raise_()  
            self.siparisler_window.activateWindow()



    def open_second_window(self):
        from trendyol_api.sorular_design import SecondWindow
        from trendyol_api import trendyol_servis
        td=trendyol_servis.Trendyol()
        td.sorular()
        self.second_window = SecondWindow()
        self.second_window.show()
        

    def durum(self):
        durum = self.ui.checkBox_3.isChecked()
        if durum:
            print('Hatırlatma açıldı...')
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton.clicked.connect(self.hatiralatici_funcation)
        else:
            print('Hatırlatma kapatıldı...')
            self.ui.pushButton.setEnabled(False)
        return durum

    def hatiralatici_funcation(self):
        interval_seconds = self.calisma_araliklari()
        self.hatirlatıcı_thread = HatirlatıcıThread(interval_seconds)
        self.hatirlatıcı_thread.update_signal.connect(self.update_ui)
        self.hatirlatıcı_thread.start()

    def update_ui(self, message):
        self.ui.label_6.setText(message)

    def hatirlatici_save(self):
        spin_box_text = self.ui.timeEdit.time().toString('HH:mm:ss')
        data = {
            'saat': str(spin_box_text),
            'hatirlatma_oluşturma': self.durum()
        }

        with open('hatirlatici.json', 'w', encoding='utf-8') as dosya:
            json.dump(data, dosya, ensure_ascii=False, indent=4)

        def kaydet_button_sonra():
            self.show_message('Program belirlediğiniz sürede bir çalışmaya devam edecek, hatılatıcı oluşturulduktan sonra programı kapatmayınız.','Otomatik Çalışma Aktif')
            self.ui.pushButton.setEnabled(False)
            self.ui.checkBox_3.setEnabled(False)
            self.ui.label_5.setText(spin_box_text)
            self.ui.timeEdit.setEnabled(False)

        
        kaydet_button_sonra()

    def pb_guncellenen_veriler(self):
        try:
            self.show_message(text_message='Lütfen bilgiler alınmadan programı kapatmayınız', text_message_title='Güncellenen Ürünler')
            self.bekleniyor(text='Güncellenen veriler alınıyor')
            basari_dagitim_object.fiyati_guncellenen_24_saat_xml()
            self.bekleniyor(text='Başarı tarafından güncellenen veriler alındı')
            self.show_tray_notification("Güncellenen Ürünler", "24 Saat içerisindeki tüm güncellenen ürünler başarıyla alındı")
        except PermissionError:
            self.ui.label_20.setText('Excel dosyasını arkadan kapatınız tekrar çalıştırınız')
            self.show_tray_notification('Excel dosyasını arkadan kapatınız tekrar çalıştırınız','Excel dosyasını arkadan kapatınız tekrar çalıştırınız')

    def pb_stok_bilgileri_tumu(self):
        try:
            self.show_message(text_message_title='Ürün stok bilgileri', text_message='Lütfen bilgiler alınmadan programı kapatmayınız')
            self.bekleniyor(text='Tüm stok bilgileri çekme işlemi yapılıyor')
            basari_dagitim_object.tum_urunler_stok_miktarı()
            self.bekleniyor(text='Başarı tarafından tüm stok bilgileri işlemi bitti')
            self.show_tray_notification("Ürün Stok Bilgileri", "Tüm stok bilgileri başarıyla alındı.")
        except:
            self.show_tray_notification('Ürün stok bilgileri', 'Ürün stok bilgileri güncellenirken bir hata meydana geldi')

    def pb_fiyat_iskonto(self):
        try:
            self.show_message(text_message_title='Fiyat bilgileri', text_message='Tüm ürünlerin fiyat & iskonto bilgileri')
            self.bekleniyor('İskonto bilgileri çekiyor')
            basari_dagitim_object.tum_urunler_fiyat()
            self.bekleniyor('İskonto bilgileri çekme işlemi bitti')
            self.show_tray_notification("Fiyat ve İskonto Bilgileri", "Tüm ürünlerin fiyat ve iskonto bilgileri başarıyla alındı.")
        except Exception as e:
            print(e)
            self.show_tray_notification('Fiyat ve iskonto bilgileri alınırken bir hata meydana geldi.','test')

    def pb_tamamini_guncelle(self):
        try:
            print('Tüm dosyalar güncel hali almak için hazırlanıyor')
            basari_dagitim_object.tum_urunler_fiyat()
            basari_dagitim_object.tum_urunler_stok_miktarı()
            basari_dagitim_object.guncellenen_kitaplar_api()
            basari_dagitim_object.fiyati_guncellenen_24_saat_xml()
            self.show_tray_notification("Tüm Dosyalar Güncellendi", "Tüm dosyalar başarıyla güncellendi.")
        except:
            self.show_tray_notification('Tüm dosyalar güncellendi', 'Dosyalar güncellenirken bir hata meydana geldi.')

    def show_message(self, text_message, text_message_title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text_message)
        msg.setWindowTitle(text_message_title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def bekleniyor(self, text):
        self.ui.label_20.setText(text)
        self.ui.label_20.setStyleSheet('color:red;')

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon('Adsız tasarım.png'), self)
        tray_menu = QMenu(self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_tray_notification(self, title, message):
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 10000)

    def calisma_araliklari(self):
        with open('hatirlatici.json', 'r', encoding='utf-8') as dosya:
            dosya_object = json.load(dosya)
            time_str = dosya_object['saat']
            
            hour = int(time_str[:2])
            minute = int(time_str[3:5])
            second = int(time_str[6:8])

            total_minutes = (hour * 60) + minute
            total_seconds = (total_minutes * 60) + second

            return total_seconds
        
    def siparis_adet(self):
        try:
            '''Toplam Sipariş Sayınız'''
            deger=self.td.siparisler()
            self.ui.label_14.setText(f'{str(deger)}')
        except Exception as e:
            print('Sipariş adtlerini alırken bir hata meydana geldi',e)

    def toplam_soru(self):
        try:
            '''Toplam Soru sayınız'''
            deger=self.td.sorular()
            self.ui.label_15.setText(str(deger))
        except Exception as e:
            print('Bir hata meydana geldi',e)

    def hazirlanan_siparisler(self):
        try:
            ''''Hazirlanan Siparisler'''
            deger=self.td.hazirlanan_siparisler()['totalElements']
            self.ui.label_17.setText(str(deger))
        except Exception as e:
            print('Bir hata meydana geldi',e)
        
    def yola_cikan_siparisler(self):
        try:
            ''''Kargoda Olan Siparisler'''
            object=self.td.tasima_durumuna_gecen_siparisler()['totalElements']
            self.ui.label_18.setText(str(object))
        except Exception as e:
            print('Bir hata meydana geldi',e)

    def iade_olusturulan(self):
        ''''Müşteri iadelerini gösteren'''
        print('Adet İadeniz Mevcut: ',self.td.iadesi_olusturlulan())
        adet_iade=self.td.iadesi_olusturlulan()
        self.ui.label_16.setText(str(adet_iade))

    def hepsiburada_siparis(self):
        pass
    
    def siparis_hazirlama_ekrani(self):
        from trendyol_api.siparis_hazirlama import SiparisHazirlaDialog
        dialog = SiparisHazirlaDialog()
        dialog.exec_()
        
def start():
    baslangic=time.time()
    if __name__ == "__main__":
        app = QApplication([])
        window = Myapp()
        bitis=time.time()
        window.show()
        print('Programın toplam açılış süresi',bitis-baslangic)
        app.exec_()


start()

