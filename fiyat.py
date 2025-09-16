import streamlit as st
import pandas as pd

st.set_page_config(page_title="3D Print Satış Fiyatı Hesaplayıcı", layout="wide")
st.title("🎯 3D Print Satış Fiyatı Hesaplayıcı")

st.markdown("""
Bu uygulama ile *birden fazla 3D baskı ürününün maliyetini ve önerilen satış fiyatını* hesaplayabilirsiniz.
""")

# Kullanıcıdan genel parametreler
filament_fiyat = st.number_input("Filament fiyatı (TL/kg)", value=500.0)
elektrik = st.number_input("Elektrik maliyeti (TL)", value=2.0)
iscilik = st.number_input("İşçilik / paketleme (TL)", value=5.0)
diger = st.number_input("Diğer giderler (TL)", value=0.0)
kar_orani = st.slider("Kar marjı (%)", 0, 200, 30)

st.markdown("---")

st.subheader("Ürün Bilgileri")
# Birden fazla ürün eklemek için
urunlar = st.text_area("Ürün adlarını ve gramajlarını girin (ör: Ürün1,50\nÜrün2,100)", height=150)

urun_listesi = []
if urunlar:
    satirlar = urunlar.split("\n")
    for s in satirlar:
        try:
            ad, gram = s.split(",")
            gram = float(gram)
            urun_listesi.append({"Ürün": ad.strip(), "Gram": gram})
        except:
            st.warning(f"Satır hatalı: {s}")

if urun_listesi:
    df = pd.DataFrame(urun_listesi)
    df["Filament Maliyeti (TL)"] = (filament_fiyat / 1000) * df["Gram"]
    df["Toplam Maliyet (TL)"] = df["Filament Maliyeti (TL)"] + elektrik + iscilik + diger
    df["Önerilen Satış Fiyatı (TL)"] = df["Toplam Maliyet (TL)"] * (1 + kar_orani / 100)
    
    st.markdown("### Hesaplanan Ürünler")
    st.dataframe(df.style.format("{:.2f}"))

    # Excel / CSV indirme
    st.markdown("### Dosya İndir")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 CSV olarak indir",
        data=csv,
        file_name='3dprint_fiyatlar.csv',
        mime='text/csv'
    )
