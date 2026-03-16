import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN SANG TRỌNG ---
st.set_page_config(page_title="Hệ Thống SEO AI Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    /* Tổng thể nền và chữ */
    .stApp { background-color: #1e212b; color: #f8fafc; }
    h1, h2, h3, p, label { color: #f8fafc !important; }
    
    /* Box chức năng (Card) */
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); 
        backdrop-filter: blur(10px);
        padding: 25px; 
        border-radius: 16px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* Tiêu đề chính */
    .main-title { 
        background: linear-gradient(90deg, #f1c40f, #e67e22);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 38px; font-weight: 900; text-align: center; margin-bottom: 5px; 
    }

    /* Nút bấm (Button) */
    .stButton>button { 
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important; 
        color: white !important; 
        width: 100%; border-radius: 12px; height: 3.5em; font-weight: 800; border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }

    /* Thẻ Tag Bong Bóng */
    .tag-bubble { 
        background: linear-gradient(135deg, #334155, #1e293b); 
        color: #60a5fa; padding: 8px 18px; 
        border-radius: 30px; display: inline-block; margin: 6px; 
        border: 1px solid #475569; font-size: 14px; font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Tùy chỉnh Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #334155; border-radius: 8px 8px 0px 0px; 
        padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #2563eb; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG AI TỰ CHẨN ĐOÁN LỖI 404 ---
def get_best_available_model(api_key):
    """Tự động hỏi Google xem API Key này được phép dùng model nào để chặn lỗi 404"""
    genai.configure(api_key=api_key)
    try:
        # Lấy danh sách model thực tế từ server
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Thử tìm các model mạnh nhất theo thứ tự ưu tiên
        priorities = ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-3-flash']
        for p in priorities:
            if p in models:
                return p
        
        # Nếu không có trong ưu tiên, lấy bừa model đầu tiên hỗ trợ tạo text
        return models[0] if models else None
    except Exception as e:
        return None

def analyze_youtube_seo(api_key, keyword, lang, ref_link):
    try:
        model_name = get_best_available_model(api_key)
        if not model_name:
            return "Lỗi API Key không hợp lệ hoặc bị chặn."
        
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        Bạn là chuyên gia SEO Youtube hàng đầu. Phân tích từ khóa: '{keyword}' (Ngôn ngữ: {lang}).
        Link đối thủ tham khảo: {ref_link}.
        Trả về DUY NHẤT một chuỗi JSON chuẩn:
        {{
            "titles": ["10 tiêu đề giật tít, tò mò"],
            "tags": ["25 thẻ tags tối ưu SEO"],
            "description": "Đoạn mô tả 200 chữ chứa từ khóa và kêu gọi hành động",
            "script_idea": "3 gạch đầu dòng kịch bản chính cho video này",
            "thumbnail": "Gợi ý thiết kế ảnh Thumbnail (chữ, màu sắc, hình ảnh)"
        }}
        """
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return f"Lỗi xử lý AI: {str(e)}"

# --- 3. QUẢN LÝ TRẠNG THÁI (STATE) ---
if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ KẾT NỐI AI")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    st.caption("Trạng thái: Tích hợp thuật toán dò Model tự động chống lỗi 404.")

# --- 4. GIAO DIỆN NHẬP LIỆU ---
if st.session_state.step == 1:
    st.markdown('<div class="main-title">HỆ THỐNG SEO VIDEO AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #94a3b8; margin-bottom: 30px;">Tự động phân tích, tối ưu mọi từ khóa không lo báo lỗi</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("🌐 Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("🔗 Link đối thủ (Tùy chọn)")
    with col2:
        kw = st.text_input("🎯 Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: kiếm tiền online")
        channel = st.text_input("📺 Tên kênh của bạn")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH CHUYÊN SÂU"):
        if kw and api_key:
            with st.spinner("🤖 Trí tuệ nhân tạo đang phân tích đối thủ và thị trường..."):
                res = analyze_youtube_seo(api_key, kw, lang, ref)
                if isinstance(res, dict):
                    st.session_state.data = res
                    st.session_state.current_kw = kw
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error(res) # Hiện lỗi rõ ràng nếu có
        else:
            st.warning("⚠️ Vui lòng nhập Từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. GIAO DIỆN KẾT QUẢ ĐA TẦNG (TABS) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📊 KẾT QUẢ TỐI ƯU: <span style='color:#3b82f6;'>{st.session_state.current_kw.upper()}</span>", unsafe_allow_html=True)
    
    # CHỨC NĂNG TÍCH VÀO LÀ CÓ THÔNG TIN - DÙNG TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📝 10 TIÊU ĐỀ", "🏷️ 25 THẺ TAGS", "📄 MÔ TẢ & KỊCH BẢN", "🎨 THUMBNAIL"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💡 Tiêu đề khơi gợi sự tò mò (CTR Cao)")
        for t in st.session_state.data.get('titles', []):
            st.success(f"🎯 {t}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔍 Bộ từ khóa tối ưu thuật toán Youtube")
        tags_html = "".join([f'<span class="tag-bubble">{t}</span>' for t in st.session_state.data.get('tags', [])])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📝 Mô tả Video chuẩn SEO")
        st.info(st.session_state.data.get('description', ''))
        st.subheader("🎬 Ý tưởng Kịch bản (Cấu trúc Video)")
        st.warning(st.session_state.data.get('script_idea', ''))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🖼️ Thiết kế Hình ảnh thu nhỏ")
        st.write(st.session_state.data.get('thumbnail', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 KHỞI TẠO TỪ KHÓA MỚI"):
        st.session_state.step = 1
        st.rerun()
