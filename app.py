import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN (Ảnh 843, 861) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện rõ tiêu đề nhãn (Fix lỗi ảnh 860) */
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }

    /* Card bao quanh nội dung (Ảnh 861) */
    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 15px; border: 1px solid #4a5568; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .title-gold { color: #f1c40f; font-size: 32px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .subtitle { color: #cbd5e0; text-align: center; margin-bottom: 30px; font-style: italic; }

    /* Nút Tạo nội dung (Ảnh 843) */
    .stButton>button { 
        background-color: #2563eb !important; color: white !important; 
        width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1d4ed8 !important; transform: scale(1.02); }

    /* Thẻ tag bong bóng (Ảnh 846) */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 8px 16px; 
        border-radius: 20px; display: inline-block; margin: 5px; 
        border: 1px solid #718096; font-size: 14px; font-weight: 500;
    }
    
    /* Styling cho các hộp thông báo */
    .stInfo, .stSuccess { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM GỌI AI CHUYÊN SÂU ---
def call_seo_expert(api_key, keyword, lang, ref_link):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng Gemini 3 Flash mới nhất để tránh 404
        model = genai.GenerativeModel('gemini-3-flash')
        
        prompt = f"""
        Bạn là một chuyên gia SEO Youtube hàng đầu. Phân tích từ khóa: '{keyword}'.
        Ngôn ngữ: {lang}. Tham khảo đối thủ: {ref_link}.
        
        Hãy trả về kết quả dưới dạng JSON thuần túy (không kèm chữ khác) với cấu trúc:
        {{
            "titles": ["10 tiêu đề thu hút click cao, chứa từ khóa chính"],
            "tags": ["25 thẻ tags phổ biến nhất, sắp xếp từ ngắn đến dài"],
            "description": "Một đoạn mô tả video chuẩn SEO (khoảng 200 chữ) chứa từ khóa và lời kêu gọi hành động",
            "thumbnail_idea": "Mô tả chi tiết 1 ý tưởng hình ảnh Thumbnail để AI tạo ảnh có thể hiểu được"
        }}
        """
        response = model.generate_content(prompt)
        # Bóc tách JSON an toàn
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return str(e)

# --- QUẢN LÝ TRẠNG THÁI ---
if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình API")
    api_key = st.text_input("Dán Gemini API Key:", type="password", help="Lấy từ Google AI Studio")
    st.divider()
    st.info("Phiên bản v3.1 - Tối ưu Gemini 3")

# --- BƯỚC 1: FORM NHẬP LIỆU (Thiết kế theo Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">HỆ THỐNG SEO VIDEO AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tối ưu hóa nội dung Youtube trong 30 giây</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Ngôn ngữ mục tiêu", ["Tiếng Việt", "English", "日本語"])
            ref = st.text_input("Link video đối thủ (Nếu có)", placeholder="https://youtube.com/watch?v=...")
        with col2:
            kw = st.text_input("Từ khóa chính cần SEO", placeholder="Ví dụ: Cách làm SEO Youtube 2026")
            channel = st.text_input("Tên kênh của bạn", placeholder="Văn Thế Official")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PHÂN TÍCH & TẠO NỘI DUNG"):
            if kw and api_key:
                with st.spinner("🤖 AI đang nghiên cứu từ khóa và đối thủ..."):
                    res = call_seo_expert(api_key, kw, lang, ref)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error(f"Lỗi API: {res}")
            else:
                st.warning("Vui lòng điền Từ khóa và API Key để bắt đầu!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ CHI TIẾT (Thiết kế theo Ảnh 844, 845, 846, 847) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📊 KẾT QUẢ TỐI ƯU CHO: `{st.session_state.current_kw.upper()}`")
    
    # 3 Nút chức năng giả lập (Ảnh 844)
    c1, c2, c3 = st.columns(3)
    c1.button("🔵 Phân tích đối thủ", use_container_width=True)
    c2.button("🟢 Từ khóa liên quan", use_container_width=True)
    c3.button("🟣 Kịch bản Video", use_container_width=True)

    # Phần 1: 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏅 10 Tiêu đề Gợi ý (CTR Cao)")
    for i, title in enumerate(st.session_state.data.get('titles', []), 1):
        st.info(f"**{i}.** {title}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Phần 2: 25 Thẻ Tags (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 25 Thẻ Tags SEO Xu hướng")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Phần 3: Mô tả & Thumbnail (Ảnh 847)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Mô tả chuẩn SEO", "🎨 Ý tưởng Thumbnail"])
    with tab1:
        st.write(st.session_state.data.get('description', 'Chưa có mô tả.'))
    with tab2:
        st.success(f"**Gợi ý Prompt tạo ảnh:** {st.session_state.data.get('thumbnail_idea', '')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Thực hiện từ khóa mới"):
        st.session_state.step = 1
        st.rerun()
