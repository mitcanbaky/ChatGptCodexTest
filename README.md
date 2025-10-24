# ChatGptCodexTest

Basit bir ilişkilendirme uygulaması örneği içerir. Komut satırından öğeler
oluşturabilir, aralarında bağlantılar kurabilir ve ortak ilişkileri
sorgulayabilirsiniz.

## Kurulum

Proje Python 3.10+ ile çalışacak şekilde tasarlanmıştır. Geliştirme ve testler
için önerilen adımlar:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (yalnızca pytest kullanıyorsanız gerekebilir)
```

Testleri çalıştırmak için:

```bash
pytest
```

## Kullanım

CLI komutu `python -m association_app` ile çağrılabilir.

```bash
python -m association_app add "İstanbul"
python -m association_app add "Türkiye"
python -m association_app associate "İstanbul" "Türkiye"
python -m association_app show "İstanbul"
python -m association_app common "İstanbul" "Ankara"
```

Varsayılan olarak veriler çalışma dizininde `associations.json` dosyasına
kaydedilir. Farklı bir dosya kullanmak için `--storage` seçeneğini
kullanabilirsiniz.
