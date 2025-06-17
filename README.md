# Trendyol Restful Api Uygulaması

Bu proje, bir adet genel RESTful API ve Trendyol'un sağladığı RESTful API kullanarak veri toplama ve işlem yapma işlemlerini gerçekleştiren bir masaüstü uygulamasıdır. Uygulama, verileri XML formatından Excel dosyasına dönüştürmek ve kullanıcıya bildirim göndermek gibi işlevleri içerir.

## Özellikler

- 220.000 çeşit veri XML formatında alınır ve Excel dosyasına dönüştürülür.
- Butona basarak verileri Excel dosyasına çevirme işlemi yapılabilir.
- Programda belirli aralıklarla çalışan zamanlayıcı özelliği bulunmaktadır.
- Bildirim (Notification) sistemi ile sağ altta bildirim gönderimi yapılır.
- Trendyol API üzerinden siparişler, müşteri soruları ve paketlenecek ürünler gibi bilgiler alınır.
- Genel RESTful API kullanılarak veri çekme ve işlem yapma işlemleri gerçekleştirilir.

## Kullanılan API'ler

### 1. Genel RESTful API
- **Açıklama**: Bu API, uygulamanın temel verilerini sağlamak için kullanılır. API üzerinden alınan veriler XML formatında olup, Excel dosyasına dönüştürülmek üzere işlenir.
- **Veri Formatı**: XML
- **İşlevsellik**: Verileri alır ve işleyerek uygulamaya aktarır.

### 2. Trendyol RESTful API
- **Açıklama**: Trendyol'un sağladığı API, siparişler, müşteri soruları, paketlenecek ürünler gibi verileri almak için kullanılır. Bu API, Trendyol ile entegrasyon sağlar.
- **Veri Formatı**: JSON
- **İşlevsellik**: Kullanıcıların Trendyol hesaplarına dair işlemler yapar ve gerekli verileri çeker.

Proje, bir genel RESTful API ve Trendyol'un sağladığı RESTful API bağlantılarını kullanarak verileri alır. Bu API'lere erişebilmek için gerekli API anahtarlarını ve bağlantı bilgilerini yapılandırma dosyasına eklemeniz gerekmektedir.



![ (1)](https://github.com/user-attachments/assets/46dbc232-d1d9-4ec2-902f-db76511f1384)
![ (8)](https://github.com/user-attachments/assets/71e95bcb-177b-4c84-8bf9-83edcb6def6e)
![ (7)](https://github.com/user-attachments/assets/040f1966-0f2c-42ea-8aae-baf3799543ca)
![ (6)](https://github.com/user-attachments/assets/fd3d2b73-9810-435a-8367-9e0eb93c229f)
![ (5)](https://github.com/user-attachments/assets/314b3b5b-19ce-4c09-8270-031659849305)
![ (4)](https://github.com/user-attachments/assets/5fed0366-46b6-44cf-ae95-cb3337d12e6a)
![ (3)](https://github.com/user-attachments/assets/fa8f72bf-682f-4db5-8a19-e6615b9b416c)
![ (2)](https://github.com/user-attachments/assets/8554f1d3-5849-4e67-ab79-b782beb22d96)



## Lisans

Bu proje [MIT Lisansı](https://opensource.org/licenses/MIT) altında lisanslanmıştır.

---

Proje geliştiricisi: Erkut Elik
