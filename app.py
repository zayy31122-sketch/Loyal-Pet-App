import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Loyal Pet Clinic", page_icon="🐾")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🐾 Loyal Pet Clinic</h1>", unsafe_allow_html=True)

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

menu = ["📝 လူနာသစ်သွင်းရန်", "📅 ရက်ချိန်းများကြည့်ရန်", "🔍 မှတ်တမ်းရှာရန်"]
choice = st.sidebar.radio("Menu", menu)

if choice == "📝 လူနာသစ်သွင်းရန်":
    st.subheader("📋 လူနာသစ်စာရင်းသွင်းရန်")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            owner = st.text_input("ပိုင်ရှင်အမည်")
            phone = st.text_input("ဖုန်းနံပါတ်")
            pet_type = st.selectbox("အမျိုးအစား", ["ခွေး", "ကြောင်", "ငှက်", "အခြား"])
            pet_info = st.text_input("နာမည် နှင့် အသက်")
        with col2:
            symptoms = st.text_area("ရောဂါလက္ခဏာ")
            treatment = st.text_area("ဆေးမှတ်တမ်း")
            next_visit = st.date_input("နောက်တစ်ခေါက် ရက်ချိန်း (ရှိလျှင်)", value=None)
        
        submitted = st.form_submit_button("မှတ်တမ်းသိမ်းမည်")
        
        if submitted:
            date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            next_v_str = next_visit.strftime("%d/%m/%Y") if next_visit else "မရှိပါ"
            
            new_row = pd.DataFrame([{
                "နေ့စွဲ": date_str, "ပိုင်ရှင်အမည်": owner, "ဖုန်းနံပါတ်": phone, 
                "အမျိုးအစား": pet_type, "နာမည်နှင့်အသက်": pet_info, 
                "ရောဂါလက္ခဏာ": symptoms, "ဆေးမှတ်တမ်း": treatment,
                "နောက်တစ်ခေါက်ရက်ချိန်း": next_v_str
            }])
            
            data = conn.read()
            updated_df = pd.concat([data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success(f"{pet_info} အတွက် မှတ်တမ်းသိမ်းပြီးပါပြီ။ ရက်ချိန်း - {next_v_str}")

elif choice == "📅 ရက်ချိန်းများကြည့်ရန်":
    st.subheader("📅 လာမည့်ရက်ချိန်းများ")
    data = conn.read()
    if "နောက်တစ်ခေါက်ရက်ချိန်း" in data.columns:
        # ရက်ချိန်းရှိသူများကိုသာ ပြခြင်း
        appointments = data[data['နောက်တစ်ခေါက်ရက်ချိန်း'] != "မရှိပါ"]
        st.dataframe(appointments[['နေ့စွဲ', 'ပိုင်ရှင်အမည်', 'ဖုန်းနံပါတ်', 'နာမည်နှင့်အသက်', 'နောက်တစ်ခေါက်ရက်ချိန်း']])
    else:
        st.info("ရက်ချိန်းမှတ်တမ်း မရှိသေးပါ။")

elif choice == "🔍 မှတ်တမ်းရှာရန်":
    st.subheader("🔎 မှတ်တမ်းများ ရှာဖွေခြင်း")
    data = conn.read()
    search = st.text_input("ပိုင်ရှင်အမည် သို့မဟုတ် ဖုန်းနံပါတ်ဖြင့် ရှာပါ")
    if search:
        results = data[data['ပိုင်ရှင်အမည်'].str.contains(search, na=False) | data['ဖုန်းနံပါတ်'].astype(str).str.contains(search, na=False)]
        st.dataframe(results)
    else:
        st.dataframe(data.tail(10))
