# Kaza Namazı Hesaplama V1

Statik, Cloudflare Pages/Workers uyumlu hesaplama ve SEO içerik sitesi.

## Build

```bash
python build.py
```

Çıktı `dist/` klasörüne oluşturulur.

## Yayın

Cloudflare build command: `python build.py`
Build output directory: `dist`

## İçerik Yönetimi

Yayın sonrasında `https://kazanamazihesapla.com/admin/` adresinden giriş yapılır.
Panel, `demirrtasfurkan/kaza-namazi-hesaplama` reposundaki içerik dosyalarını günceller.
Ana sayfanın temel SEO/metin alanları `src/data/homepage.json`, rehber yazıları ise
`src/data/pages.json` üzerinden yönetilir. Panelde yayımlanan değişiklik GitHub'a
commit edilir ve mevcut Cloudflare Git entegrasyonu otomatik build/deploy başlatır.

İlk girişte yalnızca bu repository'ye erişimi olan fine-grained GitHub token kullanın.
Token'ı dosyalara, commit'lere veya başkalarıyla paylaşılan ekran görüntülerine eklemeyin.
