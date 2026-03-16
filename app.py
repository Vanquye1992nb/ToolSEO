import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (CHUẨN 5 ẢNH MẪU) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    label { color: #ffffff !important; font-weight: bold !important; }
    .card { background-color: #363d4a; padding: 25px; border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px; }
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; }
    .stButton>button { background-color: #2563eb !important; color: white !important; width: 100%; border-radius: 8px; font-weight: bold; border: none; }
    .tag-chip { background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #718096; }
    </style>
    """, unsafe_allow_html=True)

# Hàm thông minh để tránh lỗi 404
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Lấy danh sách model thực tế mà API Key của bạn được phép dùng
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Thử các model theo thứ tự ưu tiên
        for model_name in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if model_name in available_models:
                return model_name
        return available_models[0] if available_models else None
    except:
        return None

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập API Key:", type="password")

if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm giàu")
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                selected_model = get_working_model(api_key)
                if selected_model:
                    try:
                        model = genai.GenerativeModel(selected_model)
                        response = model.generate_content(f"SEO Youtube cho từ khóa '{kw}'. Trả về JSON: 'titles' (list 10), 'tags' (list 25).")
                        match = re.search(r'\{.*\}', response.text, re.DOTALL)
                        if match:
                            st.session_state.data = json.loads(match.group())
                            st.session_state.current_kw = kw
                            st.session_state.step = 2
                            st.rerun()
                    except Exception as e: st.error(f"Lỗi gọi AI: {e}")
                else: st.error("API Key này không có quyền truy cập model nào!")
            else: st.warning("Hãy nhập đủ thông tin!")
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ SEO: {st.session_state.current_kw.upper()}")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.data.get('titles', []): st.write(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 THẺ TAGS SEO**")
    tags = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    
    if st.button("🔄 Quay lại"):
        st.session_state.step = 1
        st.rerun()
