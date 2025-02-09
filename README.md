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






## Lisans

Bu proje [MIT Lisansı](https://opensource.org/licenses/MIT) altında lisanslanmıştır.

---

Proje geliştiricisi: Erkut Elik
