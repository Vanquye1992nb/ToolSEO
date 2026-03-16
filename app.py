import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (THEO ẢNH MẪU 843, 861) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }
    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 15px; border: 1px solid #4a5568; margin-bottom: 20px;
    }
    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; }
    .stButton>button { 
        background-color: #2563eb !important; color: white !important; 
        width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; border: none;
    }
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 8px 16px; 
        border-radius: 20px; display: inline-block; margin: 5px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC AI THÔNG MINH (TRÁNH 404) ---
def call_seo_ai(api_key, keyword, lang, ref_link):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng Gemini 3 Flash theo cập nhật tháng 3/2026 của bạn
        model = genai.GenerativeModel('gemini-3-flash')
        
        prompt = f"Phân tích SEO Youtube cho từ khóa '{keyword}' ({lang}). Link đối thủ: {ref_link}. Trả về JSON: titles(10), tags(25), desc."
        response = model.generate_content(prompt)
        
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        # Nếu Gemini 3 chưa bật, tự động thử Gemini Pro
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            return json.loads(match.group())
        except:
            return str(e)

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Dán API Key từ AI Studio:", type="password")

# --- BƯỚC 1: NHẬP LIỆU ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">HỆ THỐNG SEO VIDEO AI</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
            ref = st.text_input("Link đối thủ")
        with col2:
            kw = st.text_input("Từ khóa chính")
            channel = st.text_input("Tên kênh")
        
        if st.button("🚀 BẮT ĐẦU PHÂN TÍCH"):
            if kw and api_key:
                with st.spinner("🤖 Đang phân tích..."):
                    res = call_seo_ai(api_key, kw, lang, ref)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else: st.error(f"Lỗi: {res}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (THEO ẢNH MẪU 846, 9e1976) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📊 KẾT QUẢ SEO: `{st.session_state.current_kw.upper()}`")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.info(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 THẺ TAGS SEO XU HƯỚNG**")
    tags_html = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Làm từ khóa mới"):
        st.session_state.step = 1
        st.rerun()
