import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN (THEO MẪU ẢNH 843, 861) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện rõ label nhập liệu (Sửa lỗi ảnh 860) */
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }

    /* Card bao quanh nội dung chuyên nghiệp */
    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 15px; border: 1px solid #4a5568; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #cbd5e0; text-align: center; margin-bottom: 30px; font-style: italic; }

    /* Nút bấm hành động (Ảnh 843) */
    .stButton>button { 
        background-color: #2563eb !important; color: white !important; 
        width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; border: none;
    }

    /* Thẻ tag bong bóng (Ảnh 846, 9e1976) */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 8px 16px; 
        border-radius: 20px; display: inline-block; margin: 5px; 
        border: 1px solid #718096; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC AI - SỬ DỤNG GEMINI 3 FLASH (SỬA LỖI 404) ---
def call_seo_ai(api_key, keyword, lang, ref_link):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model Gemini 3 Flash mới nhất theo cập nhật của bạn
        model = genai.GenerativeModel('gemini-3-flash')
        
        prompt = f"""
        Bạn là chuyên gia SEO Youtube. Hãy phân tích từ khóa '{keyword}' (Ngôn ngữ: {lang}).
        Dựa trên link đối thủ: {ref_link} (nếu có).
        Trả về JSON thuần túy:
        {{
            "titles": ["10 tiêu đề thu hút"],
            "tags": ["25 thẻ tags phổ biến"],
            "description": "Mô tả chuẩn SEO chứa từ khóa",
            "thumbnail_prompt": "Mô tả hình ảnh cho AI tạo Thumbnail"
        }}
        """
        response = model.generate_content(prompt)
        # Bóc tách JSON từ phản hồi của AI
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return str(e)

# --- 3. QUẢN LÝ TRẠNG THÁI ---
if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("🔑 Cài đặt API")
    # Lấy key từ bảng điều khiển bạn đã chụp
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    st.divider()
    st.write("Phiên bản: 2026.3.17 (Gemini 3 Optimized)")

# --- 4. GIAO DIỆN BƯỚC 1: NHẬP LIỆU (Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">HỆ THỐNG SEO VIDEO AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Phân tích từ khóa và đối thủ chuyên sâu</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
            ref = st.text_input("Link đối thủ", placeholder="Dán link video đối thủ...")
        with col2:
            kw = st.text_input("Từ khóa chính", placeholder="Ví dụ: Cách kiếm tiền online")
            channel = st.text_input("Tên kênh của bạn", placeholder="Văn Thế Official")
        
        if st.button("🚀 BẮT ĐẦU PHÂN TÍCH"):
            if kw and api_key:
                with st.spinner("🤖 AI đang làm việc..."):
                    res = call_seo_ai(api_key, kw, lang, ref)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error(f"Lỗi: {res}")
            else:
                st.warning("Vui lòng nhập Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. GIAO DIỆN BƯỚC 2: KẾT QUẢ (Ảnh 844, 845, 846) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📊 KẾT QUẢ SEO: `{st.session_state.current_kw.upper()}`")
    
    # Các nút chức năng hỗ trợ (Ảnh 844)
    c1, c2, c3 = st.columns(3)
    c1.button("🔵 Phân tích đối thủ", use_container_width=True)
    c2.button("🟢 Từ khóa liên quan", use_container_width=True)
    c3.button("🟣 Kịch bản Video", use_container_width=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ THU HÚT CLICK**")
    for t in st.session_state.data.get('titles', []):
        st.info(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags (Ảnh 846, 9e1976)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 THẺ TAGS SEO XU HƯỚNG**")
    tags_html = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Mô tả & Thumbnail
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Mô tả Video & Thumbnail")
    st.write(st.session_state.data.get('description', ''))
    st.divider()
    st.success(f"🎨 **Ý tưởng Thumbnail:** {st.session_state.data.get('thumbnail_prompt', '')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Quay lại"):
        st.session_state.step = 1
        st.rerun()
