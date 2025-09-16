import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

st.set_page_config(page_title="3D Print Urun Fiyat Hesapla", layout="wide")
st.title("🎯 3D Print Urun Fiyat Hesapla")

st.markdown("""
Bu uygulama ile birden fazla 3D baskı ürününün maliyetini ve önerilen satış fiyatını hesaplayabilirsiniz.
""")

# Genel parametreler
filament_fiyat = st.number_input("Filament fiyatı (TL/kg)", value=500.0)
elektrik = st.number_input("Elektrik maliyeti (TL)", value=2.0)
iscilik = st.number_input("İşçilik / paketleme (TL)", value=5.0)
diger = st.number_input("Diğer giderler (TL)", value=0.0)
kar_orani = st.slider("Kar marjı (%)", 0, 200, 30)

st.markdown("---")
st.subheader("Ürün Bilgileri")

urunlar = st.text_area(
    "Ürün adlarını ve gramajlarını girin (ör: Ürün1,50 veya Ürün2 100).\nBoş satırlar göz ardı edilir.",
    height=150
)

urun_listesi = []
if urunlar:
    satirlar = urunlar.split("\n")
    for s in satirlar:
        s = s.strip()
        if not s:
            continue
        # Esnek ayırıcı: virgül veya boşluk
        if "," in s:
            ad, gram = s.split(",", 1)
        else:
            parts = s.split()
            if len(parts) < 2:
                st.warning(f"Satır hatalı: {s}")
                continue
            ad, gram = parts[0], parts[1]
        try:
            gram = float(gram.strip())
            ad = ad.strip()
            urun_listesi.append({"Ürün": ad, "Gram": gram})
        except:
            st.warning(f"Gramaj hatalı: {s}")

if urun_listesi:
    df = pd.DataFrame(urun_listesi)
    df["Filament Maliyeti (TL)"] = (filament_fiyat / 1000) * df["Gram"]
    df["Toplam Maliyet (TL)"] = df["Filament Maliyeti (TL)"] + elektrik + iscilik + diger
    df["Önerilen Satış Fiyatı (TL)"] = df["Toplam Maliyet (TL)"] * (1 + kar_orani / 100)

    st.markdown("### Hesaplanan Ürünler")
    st.dataframe(df.style.format({
        "Filament Maliyeti (TL)": "{:.2f}",
        "Toplam Maliyet (TL)": "{:.2f}",
        "Önerilen Satış Fiyatı (TL)": "{:.2f}"
    }))

    # PDF oluşturma fonksiyonu (şık tablo)
    def convert_df_to_pdf(df):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Başlık
        title = Paragraph("3D Print Satis Fiyatlari", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Tarih
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M")
        elements.append(Paragraph(f"Tarih: {date_str}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Tablo verisi
        data = [df.columns.tolist()] + df.round(2).values.tolist()
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    pdf_buffer = convert_df_to_pdf(df)
    st.download_button(
        label="📥 PDF olarak indir",
        data=pdf_buffer,
        file_name="3dprint_fiyatlar.pdf",
        mime="application/pdf"
    )




