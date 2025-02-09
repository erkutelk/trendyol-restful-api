import requests
import base64
import json
from .api_password import API_KEY, API_SECRET, INTEGRATOR, MERCHANT_ID


class Trendyol:
    def __init__(self):
        self.headers = {
            'Authorization': 'Basic ' + base64.b64encode(f'{API_KEY}:{API_SECRET}'.encode()).decode(),
            'User-Agent': f'{MERCHANT_ID} - {INTEGRATOR}',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.trendyol.com/sapigw/suppliers'

    def siparisler(self, page=1, page_size=100):
        try:
            query = {
                'page': page - 1,
                'size': page_size,
                'orderByField': 'PackageLastModifiedDate',
                'orderByDirection': 'DESC'
            }
            order_list = self.call(f'{self.base_url}/{MERCHANT_ID}/orders?status=Created', query)
            
            if 'content' in order_list:  
                self.json_write(dosya_name='trendyol_api\\json_file\\siparisler.json',response=order_list)
                print('Siparişler Alındı')
                return order_list['totalElements']
            else:
                print("Siparişler alınırken bir hata oluştu")
                return None
        except Exception as e:
            print('Sipariş paketlerini alırken bir hata meydana geldi.',e)

    def sorular(self, page=1, page_size=10):
        try:
            query = {
                'page': page - 1,
                'size': page_size
            }
            sorular_urun = self.call(f'{self.base_url}/{MERCHANT_ID}/questions/filter?&status=WAITING_FOR_ANSWER', query)
            self.json_write('trendyol_api\\json_file\\sorular.json',sorular_urun)
            
            return sorular_urun['totalElements']
        except Exception as e:
            print('Sorular alınırken bir hata meydana geldi', e)

    def call(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json() 
        else:
            return {'error': f'HTTP {response.status_code}', 'message': response.text}

    def hazirlanan_siparisler(self, page=1, page_size=100):
        try:
            '''Sipariş toplamaya hazır olduğunda'''
            query = {
                'page': page - 1,
                'size': page_size,
                'orderByField': 'PackageLastModifiedDate',
                'orderByDirection': 'DESC'
            }
            order_list = self.call(f'{self.base_url}/{MERCHANT_ID}/orders?status=Picking', query)
            return order_list
        except Exception as e:
            print('Hazırlanan siparişler alınırken bir hata meydana geldi.',e)

    def tasima_durumuna_gecen_siparisler(self, page=1, page_size=100):
        try:
            '''Taşıma Durumuna geçen siparişler'''
            query = {
                'page': page - 1,
                'size': page_size,
                'orderByField': 'PackageLastModifiedDate',
                'orderByDirection': 'DESC'
            }
            order_list = self.call(f'{self.base_url}/{MERCHANT_ID}/orders?status=Shipped', query)
            return order_list
        except Exception as e:
            print('Taşıma durumuna geçen siparişler alınırken bir hata meydna geldi',e)


    def musteriye_ulasmayan_siparisler(self, page=1, page_size=100):
        try:
            '''Taşıma Durumuna geçen siparişler'''
            query = {
                'page': page - 1,
                'size': page_size,
                'orderByField': 'PackageLastModifiedDate',
                'orderByDirection': 'DESC'
            }
            order_list = self.call(f'{self.base_url}/{MERCHANT_ID}/orders?status=UnDelivered', query)
            return order_list

        except Exception as e:
            print('Taşıma durumuna geçen siparişler alınırken bir hata meydna geldi',e)


    def iadesi_olusturlulan(self, page=1, page_size=100):
        query = {
            'page': page - 1,
            'size': page_size,
            'orderByField': 'PackageLastModifiedDate',
            'orderByDirection': 'DESC'
        }
        order_list = self.call(f'{self.base_url}/{MERCHANT_ID}/claims?claimItemStatus=Created', query)
        respones = order_list.get('content', [])
        self.json_write('trendyol_api\\json_file\\iade_olusturulan.json',order_list)
        return order_list['totalElements']


    def json_write(self, dosya_name, response):
        '''''Json dosyalarını yazdırma'''
        with open(dosya_name, 'w', encoding='utf-8') as dosya:
            json.dump(response, dosya, indent=4)



ty = Trendyol()

def sorular_():
    yorum_sayisi = 0
    sorular_data = ty.sorular()
    
    if sorular_data:
        for a in sorular_data:
            yorum_sayisi += 1
            print(f'{yorum_sayisi} ) Soru:\t\t{a["text"].strip()}\nKitap İsmi:\t\t{a["productName"].strip()}\n------------------------')
    else:
        print('Müşteri yorumu mevcut değil.')
    
    print(f'{yorum_sayisi} Adet müşteri yorumu var')

def siparisler_():
    try:
        orders = ty.siparisler() 
        if not orders:
            print('Hiç siparişiniz yok.')
            return

        for index, a in enumerate(orders, start=1):  # 'orders' artık bir liste
            if a['commercial'] == True:
                print('--------------\n** Kurumsal Fatura.')
            else:
                print('--------------\n** Varsayılan Fatura')
            print(index, ') İsim:\t\t', a['shipmentAddress']['fullName'].upper())
            print('Adres Bilgileri:\t', a['shipmentAddress']['fullAddress'])
            adet_ürün_aldi = 0
            print('Oluşturulma Tarihi:\t', a['estimatedDeliveryEndDate'])
            for product in a['lines']:
                print('Aldığı Ürün:\t\t', product['productName'])
                print('Ürün Kodu:\t\t', product['productCode'])
                print('Ürün Fiyatı:\t\t', product['amount'])
                print('Ürün Miktarı:\t\t', product['quantity'])
                print('Barkod:\t\t\t', product['barcode'])
                adet_ürün_aldi += product['quantity']
                print('Miktar\t\t\t', adet_ürün_aldi)
                break  
    except Exception as e:
        print('Hata meydana geldi', e)


if __name__ == "__main__":
    sorular_()
    siparisler_()
    # print('İadesi Oluşturulan',ty.iadesi_olusturlulan())
    # print('Müşteriye Ulaşmayan Siparişler',ty.musteriye_ulasmayan_siparisler())
    # print('Taşıma durumuna geçen siparişler',ty.tasima_durumuna_gecen_siparisler())
    # print('Hazırlanan Siparişler Yapıldı',ty.hazirlanan_siparisler())
    

