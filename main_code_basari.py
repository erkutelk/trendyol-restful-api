import requests
import xml.etree.ElementTree as ET
import json
import datetime
import pandas
import re
import time
from user_info import Password,CustomerId
class basari_dagitim:
    adet=0
    def __init__(self):
        try:
            self.date = datetime.datetime.now().strftime('%Y-%m-%d').replace('-','')
            self.headers = {'Content-Type': 'application/json',
                            'Accept': 'application/xml'}
            self.load_token()
            self.token_control()
            self.en_son_guncelleme_tarihi()
            self.tarih=datetime.datetime.now().strftime('%d-%m-%Y').replace('-','.')
            print('Main Başarı Çalışıyor.')

        except Exception as e:
            print('bir hata meydana geldi',e)

    def load_token(self):
        try:
            with open('token-key.json', 'r', encoding='utf-8') as dosya:
                token_key = json.load(dosya)
                self.data={
                        "Password": Password,
                        "Token": token_key,
                        "CustomerId":CustomerId}
        except:
            return 'token bilgileri alınırken bir hata meydana geldi'

    def token_control(self):
        try:
            url='http://195.175.203.62/Api/XML/CheckToken'
            response=requests.post(url,headers=self.headers,json=self.data)
            root=ET.fromstring(response.content)
            if root.text=='FALSE':
                self.token_alma()
            else:
                return 'Geçerli bir token değeri'
        except:
            return 'Token alma sırasında meydana geldi...'

    def token_alma(self):
        try:
            url='http://195.175.203.62/Api/XML/Login'
            data={
                "CustomerId": CustomerId,
                "Password": Password
            }
            response=requests.post(url=url,headers=self.headers,json=data)
            root=ET.fromstring(response.content)
            self.data['Token']=root.text
        except TimeoutError:
            print('Token alırken bir hata meydana geldi...')

        with open('token-key.json','w',encoding='utf-8') as dosya:
            json.dump(root.text, dosya, ensure_ascii=False, indent=4)
            #Yeni token değerini almak için
        return root.text

    def kitap_sayisi_alma(self):
        try:
            url='http://195.175.203.62/Api/XML/GetProductCount'
            data={
                "Token": self.data['Token'],
                "CustomerId":CustomerId
                }
            response=requests.post(url,headers=self.headers,json=data,timeout=5)
            root=ET.fromstring(response.content)
            return f'{root.text}'
        except TimeoutError as e:
            return 'Kitap Sayısı Alınamadı',e
    

    def guncellenen_kitaplar_api(self):
        güncellenen_kitaplar = []
        url = 'http://195.175.203.62/Api/XML/GetDeltaData'
        page_number = 1
        records_per_page = 5000
        total_records = 0
        while True:
            data = {
                "RecordCount": records_per_page,
                "PageNumber": page_number,
                "Hour": 1,
                "Token": self.data['Token'],
                "CustomerId": CustomerId
            }
            response = requests.post(url=url, headers=self.headers, json=data)
            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    products = root.findall('.//Product')
                    
                    if not products:
                        break
                    
                    for product in products:
                        row = {
                            'stok_kod': product.find('stok_kod').text,
                            'urun_ad': product.find('urun_ad').text,
                            'yazar': product.find('yazar').text,
                            'kategori': product.find('Kategori').text,
                            'stok_durum': product.find('StokDurum').text,
                            'barkod': product.find('barkod').text,
                            'kdv': float(product.find('kdv').text),
                            'marka': product.find('marka').text,
                            'iskonto': product.find('Iskonto').text,
                            'kapak_turu': product.find('KapakTuru').text,
                            'Iskonto': product.find('Iskonto').text,
                            'isk_fiyat': float(product.find('IskFiyat').text),
                            'satis_fiyat': float(product.find('satis_fiyat').text),
                            'DepoStok': int(product.find('DepoStok').text),
                        }
                        güncellenen_kitaplar.append(row)
                        total_records += 1

                    if len(products) < records_per_page:
                        break
                    page_number += 1
                except ET.ParseError as e:
                    print(f"Error parsing XML: {e}")
            else:
                print(f"Hata meydana geldi hata kodu {response.status_code}")
                break

        self.excell_kayit_funcation(dosya_name='Guncellenen Urunler 1H',liste=güncellenen_kitaplar)
        print('Bitti')


    

    def en_cok_satan_kitaplar(self):
        populer_kitaplar=[]
        url='http://195.175.203.62/Api/XML/GetBestSellers'
        data={"RecordCount": 10000,"PageNumber": 1,"Token": self.data['Token'],"CustomerId": CustomerId}
        response=requests.post(url=url,headers=self.headers,json=data)
        if response.status_code==200:
            root = ET.fromstring(response.content)
            products = root.findall('.//Product')
            kitap_sayisi=0
            for proadact in products:
                row={}
                row['stok_kod']=proadact.find('stok_kod').text
                row['urun_ad']=proadact.find('urun_ad').text
                row['barkod']=proadact.find('barkod').text
                row['StokDurum']=proadact.find('StokDurum').text
                row['satis_fiyat']=proadact.find('satis_fiyat').text.replace('.',',')
                row['DepoStok']=proadact.find('DepoStok').text
                row['IskFiyat']=proadact.find('IskFiyat').text.replace('.',',')
                row['Iskonto']=proadact.find('Iskonto').text
                populer_kitaplar.append(row)
                kitap_sayisi+=1

            self.excell_kayit_funcation(dosya_name='Cok Satan Kitaplar',liste=populer_kitaplar)
        else:
            return 'En çok satan kitapları alırken bir hata meydna geldi'


    def fiyati_guncellenen_24_saat_xml(self):
        '''Başarıda bulunan bütün 24 saatlik veriler '''
        url = f'http://195.175.203.62/Api/XML/A03272_PRODUCTDELTA_{self.date}.XML'
        time.sleep(5)
        response = requests.get(url)
        if response:
            #Eğer response değeri geliyorsa veya boş değil ise
            if response.status_code == 200:
                    data=[]
                    a = 0
                    root = ET.fromstring(response.content)
                    while True:
                        try:
                            row={}
                            row['stok_kod'] = root[a].find('stok_kod').text
                            row['urun_ad'] = root[a].find('urun_ad').text
                            row['marka'] = root[a].find('marka').text
                            row['barkod'] = root[a].find('barkod').text
                            row['Kategori'] = root[a].find('Kategori').text
                            row['kdv'] = root[a].find('kdv').text
                            row['yazar'] = root[a].find('yazar').text
                            row['cevirmen'] = root[a].find('cevirmen').text
                            row['StokDurum'] = root[a].find('StokDurum').text
                            row['BaskiSayisi'] = root[a].find('BaskiSayisi').text
                            row['KagitCinsi'] = root[a].find('KagitCinsi').text
                            row['KapakTuru'] = root[a].find('KapakTuru').text
                            row['OlcuBirimi'] = root[a].find('OlcuBirimi').text.title()
                            row['sayfasayisi'] = root[a].find('sayfasayisi').text
                            row['renk'] = root[a].find('renk').text
                            row['ebat'] = root[a].find('ebat').text
                            row['DepoStok'] = root[a].find('DepoStok').text
                            row['IskFiyat'] = root[a].find('IskFiyat').text.replace('.',',')
                            row['satis_fiyat'] = root[a].find('satis_fiyat').text.replace('.',',')
                            data.append(row)
                            a += 1
                            basari_dagitim.adet+=1

                        except:
                            self.excell_kayit_funcation(dosya_name=f'Guncellenen Urunler 24H',liste=data)
                            break

                            
        else:
            print('Response değeri boş')

    
    def json_guncelleme_tarih(self):
        try:
            with open('calisan-saat-araliklari.json', 'r', encoding='utf-8') as dosya:
                text = json.load(dosya)

        except FileNotFoundError:
            text = []
            print("JSON dosyası bulunamadı, yeni dosya oluşturulacak.")

        basari_dagitim_object = basari_dagitim()
        yeni_tarih = {'saat': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'kitap-sayisi': basari_dagitim_object.adet}
        
        text.append(yeni_tarih)
        with open('calisan-saat-araliklari.json', 'w', encoding='utf-8') as dosya:
            json.dump(text, dosya, ensure_ascii=False, indent=4)
    
    def en_son_guncelleme_tarihi(self):
        with open('calisan-saat-araliklari.json', 'r', encoding='utf-8') as dosya:
            veri = json.load(dosya)
            son_guncelleme_tarihi=veri[-1]['saat'].split()

            return {'Saat':son_guncelleme_tarihi[0],
                    'Tarih':son_guncelleme_tarihi[1]}
            

    def tum_urunler_fiyat(self):
        url = f'http://195.175.203.62/Api/XML/A03272_PRODUCTPRICE.XML'
        response = requests.get(url)
        if response:
            #Eğer response değeri geliyorsa veya boş değil ise
            if response.status_code == 200:
                    data=[]
                    a = 0
                    root = ET.fromstring(response.content)
                    while True:
                        try:
                            row={}
                            row['stok_kod'] = root[a].find('stok_kod').text
                            row['barkod'] = root[a].find('barkod').text
                            row['kdv'] = root[a].find('kdv').text
                            row['satis_fiyat'] = root[a].find('satis_fiyat').text.replace('.',',')
                            row['Iskonto'] = root[a].find('Iskonto').text
                            row['IskFiyat'] = root[a].find('IskFiyat').text.replace('.',',')
                            row['Tedarikci'] = root[a].find('Tedarikci').text
                            data.append(row)
                            a += 1
                        except IndexError:
                            self.excell_kayit_funcation(dosya_name='Fiyatlar',liste=data)
                            self.json_guncelleme_tarih()
                            break
                        
    def tum_urunler_stok_miktarı(self):
        url = f'http://195.175.203.62/Api/XML/A03272_PRODUCTSTOCK.XML'
        response = requests.get(url)
        if response:
            if response.status_code == 200:
                data = []
                a = 0
                root = ET.fromstring(response.content)
                while True:
                    try:
                        row = {}
                        row['stok_kod'] = root[a].find('stok_kod').text
                        row['barkod'] = root[a].find('barkod').text
                        row['StokDurum'] = root[a].find('StokDurum').text
                        row['DepoStok'] = root[a].find('DepoStok').text
                        data.append(row)

                        a += 1

                    except Exception as e:
                        self.excell_kayit_funcation('Stoklar',data)
                        break

        else:
            print('Response değeri boş')


    def güncellenen_kitap_Adet(self):
        return basari_dagitim.adet
    
    def excell_kayit_funcation(self,dosya_name,liste):
        dosya_yolu = f'C:\\Users\\KULLANICI\\Desktop\\BASARI-BİLGİLERİ\\{dosya_name} {self.tarih}.xlsx'
        df = pandas.DataFrame(liste)
        df.to_excel(dosya_yolu, index=False)
        print(dosya_name,f'C:\\Users\\KULLANICI\\Desktop\\BASARI-BİLGİLERİ\\{dosya_name}.xlsx','Dosyasına kaydedildi...')

    

basari_dagitim_object=basari_dagitim()
if __name__=='__main__':
    print(basari_dagitim_object.guncellenen_kitaplar_api())
    print(basari_dagitim_object.en_cok_satan_kitaplar())
    print(basari_dagitim_object.fiyati_guncellenen_24_saat_xml())
    print(basari_dagitim_object.tum_urunler_fiyat())
    print(basari_dagitim_object.tum_urunler_stok_miktarı())


