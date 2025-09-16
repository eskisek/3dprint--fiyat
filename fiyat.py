import streamlit as st

st.title("3D Print Satış Fiyatı Hesaplayıcı")

filament_fiyat = st.number_input("Filament fiyatı (TL/kg)", value=500.0)
gram = st.number_input("Ürün gramajı (g)", value=50.0)
elektrik = st.number_input("Elektrik maliyeti (TL)", value=2.0)
iscilik = st.number_input("İşçilik / paketleme (TL)", value=5.0)
diger = st.number_input("Diğer giderler (TL)", value=0.0)
kar_orani = st.slider("Kar marjı (%)", 0, 200, 30)

filament_maliyet = (filament_fiyat / 1000) * gram
toplam_maliyet = filament_maliyet + elektrik + iscilik + diger
satis_fiyati = toplam_maliyet * (1 + kar_orani / 100)

st.write(f"### Filament maliyeti: {filament_maliyet:.2f} TL")
st.write(f"### Toplam maliyet: {toplam_maliyet:.2f} TL")
st.success(f"Önerilen satış fiyatı: {satis_fiyati:.2f} TL")