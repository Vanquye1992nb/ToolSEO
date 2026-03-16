import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }
    .card { 
        background-color: #363d4a; padding: 20px; 
        border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px; 
    }
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; }
    .stButton>button { 
        background-color: #2563eb !important; color: white !important; 
        width: 100%; border-radius: 8px; font-weight: bold; border: none;
    }
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM TỰ DÒ MODEL TRÁNH 404 ---
def get_best_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Quét danh sách model được phép
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Thứ tự ưu tiên để không bị 404
        for target in ['models/gemini-3-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if target in available: return target
        return available[0] if available else None
    except: return None

def call_seo_ai(api_key, keyword):
    try:
        model_name = get_best_model(api_key)
        if not model_name: return "Không tìm thấy model khả dụng."
        
        model = genai.GenerativeModel(model_name)
        prompt = f"Phân tích SEO Youtube cho '{keyword}'. Trả về JSON: 'titles' (10), 'tags' (25), 'desc'."
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e: return str(e)

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cài đặt")
    api_key = st.text_input("Gemini API Key:", type="password")

if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Hệ Thống SEO Video AI</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Ngôn ngữ", ["Tiếng Việt"], key="lang")
            st.text_input("Link đối thủ", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính", key="kw")
            st.text_input("Kênh của bạn", key="chan")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang xử lý..."):
                    res = call_seo_ai(api_key, kw)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else: st.error(f"Lỗi: {res}")
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ SEO: {st.session_state.current_kw.upper()}")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.data.get('titles', []): st.info(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 THẺ TAGS SEO**")
    tags = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Làm lại"):
        st.session_state.step = 1
        st.rerun()
