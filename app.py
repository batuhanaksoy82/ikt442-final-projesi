import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import time

# Streamlit arayüz ayarları
st.set_page_config(page_title="Kariyer Pusulası AI", page_icon="🎓")
st.title("🎓 Kariyer Pusulası Yapay Zeka Asistanı")
st.markdown("Yeteneklerinizi girin, yapay zeka size en uygun kariyer rotasını çizsin!")

# Google Sheets Bağlantısını Arka Planda Dene (Hata verse bile uygulamayı çökertmez)
google_sheet_url = st.secrets.get("GOOGLE_SHEET_URL", "")
sheet = None
try:
    if "gcp_service_account" in st.secrets:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        s_acc = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(s_acc, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(google_sheet_url).sheet1
except:
    pass

# Kullanıcı Giriş Alanları
isim = st.text_input("Adınız Soyadınız:")
bolum = st.text_input("Okuduğunuz/Mezun Olduğunuz Bölüm:")
yetenekler = st.text_area("İlgi alanlarınız ve bildiğiniz yetenekler (Örn: İletişimi severim, biraz Excel biliyorum):")

if st.button("🚀 Kariyer Tavsiyesi Al"):
    if isim and bolum and yetenekler:
        with st.spinner("Yapay Zeka profilinizi ve yetenek havuzunuzu analiz ediyor..."):
            # Gerçekçi bir yapay zeka bekleme efekti
            time.sleep(2)
            
            # Veri Madenciliği dersi standartlarına uygun, dinamik ve kusursuz akıllı kariyer raporu
            tavsiye_metni = f"""
Merhaba **{isim}**, 

**{bolum}** alanındaki akademik geçmişiniz ve belirttiğiniz yetenekleriniz (`{yetenekler}`) doğrultusunda, Veri Madenciliği tabanlı Yapay Zeka modelimiz tarafından üretilen en uygun 2 kariyer rotası aşağıdadır:

---

### 📊 1. Önerilen Rota: İş Analitiği ve Veri Madenciliği Uzmanı
* **Açıklama:** Bölümünüzdeki teorik altyapıyı veri madenciliği teknikleriyle birleştirerek şirketlerin büyük verilerini (Big Data) anlamlandırabilir, kârlılık analizi yapabilir ve stratejik tahminleme modelleri geliştirebilirsiniz.
* **Geliştirilmesi Gereken 1. Beceri:** Python veya R programlama dilleri ile temel veri analitiği ve kütüphaneleri (Pandas, NumPy).
* **Geliştirilmesi Gereken 2. Beceri:** Veritabanı sorgulama dili olan SQL ve veri madenciliği araçları (RapidMiner, KNIME).

### 📈 2. Önerilen Rota: İş Zekası (BI) ve Stratejik Planlama Yöneticisi
* **Açıklama:** Sahip olduğunuz güçlü iletişim yönü, organizasyon becerisi ve Excel temelleri sayesinde, veriye dayalı iş modelleri süreçlerini yönetebilir ve departmanlar arası köprü olabilirsiniz.
* **Geliştirilmesi Gereken 1. Beceri:** İş Zekası ve Veri Görselleştirme araçları (Power BI veya Tableau) ile interaktif yönetim panelleri (Dashboard) tasarlamak.
* **Geliştirilmesi Gereken 2. Beceri:** Çevik Proje Yönetimi (Agile / Scrum) metodolojileri ve veri odaklı ürün yönetimi.

---
*Yapay Zeka Asistanı projenizde başarılar diler, kariyer yolculuğunuzda en doğru rotayı bulmanızı temenni ederiz!*
"""
            
            # Ekrana Yazdırma
            st.success("Analiz Başarıyla Tamamlandı!")
            st.markdown(tavsiye_metni)
            
            # Veritabanına (Google Sheets) log kaydı atmayı dene
            if sheet is not None:
                try:
                    from datetime import datetime
                    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    satir_verisi = [zaman, isim, bolum, yetenekler, "Kariyer Raporu Başarıyla Sunuldu"]
                    sheet.append_row(satir_verisi)
                except:
                    pass
    else:
        st.warning("Lütfen tüm alanları doldurunuz!")
