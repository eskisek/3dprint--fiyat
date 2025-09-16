import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

st.set_page_config(page_title="3D Print Satış Fiyatı Hesaplayıcı", layout="wide")
st.title("🎯 3D Print Satış Fiyatı Hesaplayıcı")

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
st.subheader("Ürün Bilgileri (Tablo)")

# Başlangıç için boş DataFrame
if 'urunler_df' not in st.session_state:
    st.session_state.urunler_df = pd.DataFrame({
        "Ürün": ["Ürün1", "Ürün2"],
        "Gram": [50.0, 100.0]
    })

df_input = st.data_editor(st.session_state.urunler_df, num_rows="dynamic")
st.session_state.urunler_df = df_input

if not df_input.empty:
    df = df_input.copy()
    df["Filament Maliyeti (TL)"] = (filament_fiyat / 1000) * df["Gram"]
    df["Toplam Maliyet (TL)"] = df["Filament Maliyeti (TL)"] + elektrik + iscilik + diger
    df["Önerilen Satış Fiyatı (TL)"] = df["Toplam Maliyet (TL)"] * (1 + kar_orani / 100)

    # Sayıları 2 ondalık olarak formatla
    df_display = df.copy()
    for col in ["Gram", "Filament Maliyeti (TL)", "Toplam Maliyet (TL)", "Önerilen Satış Fiyatı (TL)"]:
        df_display[col] = df_display[col].map(lambda x: f"{x:.2f}")

    st.markdown("### Hesaplanan Ürünler")
    st.dataframe(df_display)

    # PDF oluşturma fonksiyonu
    def convert_df_to_pdf(df):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        title = Paragraph("3D Print Satış Fiyatları", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M")
        elements.append(Paragraph(f"Tarih: {date_str}", styles['Normal']))
        elements.append(Spacer(1, 12))

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
