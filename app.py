import streamlit as st
import openai
import gspread
from google.oauth2.service_account import Credentials

# Streamlit arayüz ayarları
st.set_page_config(page_title="Kariyer Pusulası AI", page_icon="🎓")
st.title("🎓 Kariyer Pusulası Yapay Zeka Asistanı")
st.markdown("Yeteneklerinizi girin, yapay zeka size en uygun kariyer rotasını çizsin!")

# API ve Gizli Bilgilerin Streamlit Secrets'tan Çekilmesi
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    google_sheet_url = st.secrets["GOOGLE_SHEET_URL"]
    
    # Google Sheets Kimlik Doğrulaması
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    s_acc = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(s_acc, scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(google_sheet_url).sheet1
except Exception as e:
    st.error("Sistem ayarları (API veya Google Sheets) henüz yapılmadı. Lütfen Ayarları kontrol edin.")
    st.stop()

# Kullanıcı Giriş Alanları
isim = st.text_input("Adınız Soyadınız:")
bolum = st.text_input("Okuduğunuz/Mezun Olduğunuz Bölüm:")
yetenekler = st.text_area("İlgi alanlarınız ve bildiğiniz yetenekler (Örn: İletişimi severim, biraz Excel biliyorum):")

if st.button("🚀 Kariyer Tavsiyesi Al"):
    if isim and bolum and yetenekler:
        with st.spinner("Yapay Zeka profilinizi analiz ediyor..."):
            
            # OpenAI Prompt'u
            prompt = f"Ben {isim}. {bolum} bölümü öğrencisi/mezunuyum. Yeteneklerim ve ilgi alanlarım şunlar: {yetenekler}. Bana uygun 2 meslek tavsiyesi ve bu meslekler için öğrenmem gereken 2 önemli beceriyi kısa và öz şekilde açıkla."
            
            try:
                # OpenAI API Çağrısı
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Sen uzman bir kariyer danışmanısın. Yanıtların motive edici, net và kısa olmalı."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                tavsiye_metni = response.choices[0].message["content"]
                
                # Ekrana Yazdırma
                st.success("Analiz Tamamlandı!")
                st.write("### Yapay Zeka Kariyer Raporunuz:")
                st.info(tavsiye_metni)
                
                # Google Sheets'e Kaydetme
                from datetime import datetime
                zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                satir_verisi = [zaman, isim, bolum, yetenekler, tavsiye_metni]
                sheet.append_row(satir_verisi)
                
                st.toast('Verileriniz başarıyla veritabanına (Google Sheets) kaydedildi!', icon='✅')

            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen tüm alanları doldurunuz!")
