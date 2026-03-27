import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Loyal Pet Clinic", page_icon="🐾")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🐾 Loyal Pet Clinic</h1>", unsafe_allow_html=True)

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

menu = ["📝 လူနာသစ်သွင်းရန်", "🔍 မှတ်တမ်းရှာရန်"]
choice = st.sidebar.radio("Menu", menu)

if choice == "📝 လူနာသစ်သွင်းရန်":
    st.subheader("📋 လူနာသစ်စာရင်းသွင်းရန်")
    with st.form("entry_form", clear_on_submit=True):
        owner = st.text_input("ပိုင်ရှင်အမည်")
        phone = st.text_input("ဖုန်းနံပါတ်")
        pet_type = st.selectbox("အမျိုးအစား", ["ခွေး", "ကြောင်", "ငှက်", "အခြား"])
        pet_info = st.text_input("နာမည် နှင့် အသက်")
        symptoms = st.text_area("ရောဂါလက္ခဏာ")
        treatment = st.text_area("ပေးလိုက်သောဆေး / ကုသမှု")
        submitted = st.form_submit_button("မှတ်တမ်းသိမ်းမည်")
        
        if submitted:
            new_row = pd.DataFrame([{"နေ့စွဲ": datetime.now().strftime("%d/%m/%Y %H:%M"), "ပိုင်ရှင်အမည်": owner, "ဖုန်းနံပါတ်": phone, "အမျိုးအစား": pet_type, "နာမည်နှင့်အသက်": pet_info, "ရောဂါလက္ခဏာ": symptoms, "ဆေးမှတ်တမ်း": treatment}])
            data = conn.read()
            updated_df = pd.concat([data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("သိမ်းဆည်းပြီးပါပြီ!")

elif choice == "🔍 မှတ်တမ်းရှာရန်":
    st.subheader("🔎 မှတ်တမ်းများ ရှာဖွေခြင်း")
    data = conn.read()
    search = st.text_input("ပိုင်ရှင်အမည် သို့မဟုတ် ဖုန်းနံပါတ်ဖြင့် ရှာပါ")
    if search:
        results = data[data['ပိုင်ရှင်အမည်'].str.contains(search, na=False) | data['ဖုန်းနံပါတ်'].astype(str).str.contains(search, na=False)]
        st.dataframe(results)
    else:
        st.dataframe(data.tail(10))
