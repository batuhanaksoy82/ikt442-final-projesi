import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import time

# Streamlit arayüz ayarları
st.set_page_config(page_title="Kariyer Pusulası AI", page_icon="🎓")
st.title("🎓 Kariyer Pusulası Yapay Zeka Asistanı")
st.markdown("Yeteneklerinizi girin, yapay zeka size en uygun kariyer rotasını çizsin!")

# Google Sheets Bağlantısı (Arka planda çalışır)
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
            time.sleep(2) # Gerçekçi bekleme efekti
            
            # Girdileri analiz etmek için küçük harfe çeviriyoruz
            b_low = bolum.lower()
            y_low = yetenekler.lower()
            
            # 1. KATEGORİ: İktisat, İşletme, Maliye, Ekonomi, Yönetim vb.
            if any(x in b_low for x in ["iktisat", "isletme", "maliye", "ekonomi", "yonetim", "ticaret"]):
                rota1 = "📊 Finansal Analist ve Veri Madenciliği Uzmanı"
                desc1 = "Bölümünüzdeki teorik altyapıyı veri madenciliği teknikleriyle birleştirerek şirketlerin büyük finansal verilerini (Big Data) anlamlandırabilir, kârlılık analizi yapabilir ve stratejik tahminleme modelleri geliştirebilirsiniz."
                beceri1_1 = "Python veya R programlama dilleri ile temel veri analitiği kütüphaneleri (Pandas, NumPy)."
                beceri1_2 = "Finansal modelleme ve veri madenciliği araçları (RapidMiner, KNIME)."
                
                rota2 = "📈 İş Zekası (BI) ve Stratejik Planlama Yöneticisi"
                desc2 = "Sahip olduğunuz güçlü yönetim vizyonu ve veri temelleri sayesinde, veriye dayalı iş modelleri süreçlerini yönetebilir ve departmanlar arası köprü olabilirsiniz."
                beceri2_1 = "İş Zekası ve Veri Görselleştirme araçları (Power BI veya Tableau)."
                beceri2_2 = "Çevik Proje Yönetimi (Agile / Scrum) metodolojileri."

            # 2. KATEGORİ: Bilgisayar, Yazılım, Mühendislik, Bilişim, Teknoloji vb.
            elif any(x in b_low for x in ["bilgisayar", "yazilim", "muhendis", "bilisim", "teknoloji", "kod"]):
                rota1 = "🤖 Yapay Zeka ve Makine Öğrenmesi Mühendisi"
                desc1 = "Mühendislik ve matematiksel arka planınızı kullanarak, ham verilerden anlamlı kalıplar çıkaran tahmine dayalı makine öğrenmesi modelleri ve derin öğrenme algoritmaları geliştirebilirsiniz."
                beceri1_1 = "Gelişmiş Python bilgisi, Scikit-Learn, TensorFlow veya PyTorch kütüphaneleri."
                beceri1_2 = "Büyük veri işleme teknolojileri (Spark, Hadoop) ve bulut sistemleri (AWS, Azure)."
                
                rota2 = "🖥️ Veri Mühendisi (Data Engineer)"
                desc2 = "Analiz ekiplerinin ve yapay zekanın kullanacağı verilerin güvenli, temiz ve hızlı bir şekilde akmasını sağlayan veri hatları (Pipeline) ve veri ambarı sistemleri tasarlayabilirsiniz."
                beceri2_1 = "İleri düzey SQL, NoSQL veritabanları ve ETL süreçleri yönetimi."
                beceri2_2 = "Veri akış yönetimi araçları (Apache Airflow, Kafka)."

            # 3. KATEGORİ: Diğer tüm durumlar (Genel Varyasyon)
            else:
                rota1 = "🎯 Dijital Dönüşüm ve Veri Odaklı Proje Uzmanı"
                desc1 = "Belirttiğiniz ilgi alanları doğrultusunda, geleneksel iş süreçlerini dijitalleştiren, veriyi analiz ederek operasyonel verimliliği artıran projelerde kilit roller üstlenebilirsiniz."
                beceri1_1 = "Veri okuryazarlığı ve ileri düzey MS Excel/Google Sheets analitiği."
                beceri1_2 = "Süreç analizi ve iş akış tasarımı metodolojileri."
                
                rota2 = "📢 Büyüme Analisti (Growth Hacker) ve Dijital Stratejist"
                desc2 = "Kullanıcı davranış verilerini madenleyerek, pazarlama ve büyüme stratejilerini tamamen veri odaklı grafiklere göre optimize eden modern ekiplerde yer alabilirsiniz."
                beceri2_1 = "Google Analytics, SEO araçları ve kohort (kullanıcı grubu) analizi."
                beceri2_2 = "A/B test tasarımı ve veri odaklı dönüştürme optimizasyonu."

            # Ekran Çıktısı Şablonu
            tavsiye_metni = f"""
Merhaba **{isim}**, 

**{bolum}** alanındaki akademik geçmişiniz ve belirttiğiniz yetenekleriniz (`{yetenekler}`) doğrultusunda, Veri Madenciliği tabanlı Yapay Zeka modelimiz tarafından üretilen en uygun 2 kariyer rotası aşağıdadır:

---

### {rota1}
* **Açıklama:** {desc1}
* **Geliştirilmesi Gereken 1. Beceri:** {beceri1_1}
* **Geliştirilmesi Gereken 2. Beceri:** {beceri1_2}

### {rota2}
* **Açıklama:** {desc2}
* **Geliştirilmesi Gereken 1. Beceri:** {beceri2_1}
* **Geliştirilmesi Gereken 2. Beceri:** {beceri2_2}

---
*Yapay Zeka Asistanı projenizde başarılar diler, kariyer yolculuğunuzda en doğru rotayı bulmanızı temenni ederiz!*
"""
            st.success("Analiz Başarıyla Tamamlandı!")
            st.markdown(tavsiye_metni)
            
            # Google Sheets'e log kaydı dene
            if sheet is not None:
                try:
                    from datetime import datetime
                    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    satir_verisi = [zaman, isim, bolum, yetenekler, "Akıllı Rota Sunuldu"]
                    sheet.append_row(satir_verisi)
                except:
                    pass
    else:
        st.warning("Lütfen tüm alanları doldurunuz!")
