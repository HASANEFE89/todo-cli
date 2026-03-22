# Todo CLI

Bu proje Python ile yazılmış basit bir komut satırı (CLI) todo uygulamasıdır.
Kullanıcıların görev eklemesine, listelemesine, tamamlamasına ve silmesine imkan veriyor.

## programın özellikleri

* Görev ekleme
* Görevleri listeleme
* Görev tamamlama
* Görev silme
* Görevlere öncelik verme
* Son tarih (deadline) ekleme
* Etiket ekleme
* Verileri JSON dosyasında saklama

## kurulum

Projeyi bilgisayarına indirdikten sonra gerekli kütüphaneleri yükle:

```bash
pip install -r requirements.txt
```

## kullanım

Programı çalıştırmak için:

```bash
python main.py
```

Programın açıldığında gelen menüde istenillen seçenek seçilebilir.

## proje Yapısı

 main.py: programın başlangıç noktası
 ui.py: kullanıcı ile etkileşimi sağlayan menü
 models.py: task veri yapısı
 storage.py: verilerin kaydedilmesi ve okunması
 tasks.json: görevlerin saklandığı dosya

## öenmli notlar

* Her görev otomatik olarak bir ID alır
* Görevler tasks.json dosyasında tutulur
* Deadline geçmişse görev listesinde bu durum gösterilir
