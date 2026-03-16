import streamlit as st
import google.generativeai as genai
import json
import re

# --- 1. CẤU HÌNH GIAO DIỆN SANG TRỌNG ---
st.set_page_config(page_title="Hệ Thống SEO AI Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #1e212b; color: #f8fafc; }
    h1, h2, h3, p, label { color: #f8fafc !important; }
    .glass-card { 
        background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px);
        padding: 25px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); 
        margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-title { 
        background: linear-gradient(90deg, #f1c40f, #e67e22);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 38px; font-weight: 900; text-align: center; margin-bottom: 5px; 
    }
    .stButton>button { 
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important; color: white !important; 
        width: 100%; border-radius: 12px; height: 3.5em; font-weight: 800; border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }
    .tag-bubble { 
        background: linear-gradient(135deg, #334155, #1e293b); color: #60a5fa; padding: 6px 14px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #475569; font-size: 13px;
    }
    .score-badge { color: #10b981; font-weight: bold; font-size: 14px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #334155; border-radius: 8px 8px 0px 0px; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #2563eb; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HỆ THỐNG AI TỰ CHẨN ĐOÁN & PROMPT NÂNG CẤP ---
def get_best_available_model(api_key):
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for p in ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-3-flash']:
            if p in models: return p
        return models[0] if models else None
    except: return None

def analyze_youtube_seo(api_key, keyword, lang, ref_link):
    model_name = get_best_available_model(api_key)
    if not model_name: return "Lỗi: API Key không hợp lệ."
    
    model = genai.GenerativeModel(model_name)
    # PROMPT MỚI: Yêu cầu chi tiết hơn, trả về điểm số và Prompt tiếng Anh
    prompt = f"""
    Bạn là chuyên gia SEO Youtube. Phân tích từ khóa: '{keyword}' (Ngôn ngữ: {lang}). Link tham khảo: {ref_link}.
    Trả về DUY NHẤT mã JSON với cấu trúc chính xác như sau:
    {{
        "titles": [
            {{"text": "Tiêu đề 1", "score": 98}},
            {{"text": "Tiêu đề 2", "score": 95}}
        ],
        "tags": ["tag1", "tag2", "tag3"],
        "hashtags": ["#hashtag1", "#hashtag2"],
        "description": "Mô tả chuẩn SEO (khoảng 150 chữ)",
        "script_idea": "3 gạch đầu dòng kịch bản",
        "thumbnail_advice": "Lời khuyên bằng {lang} về màu sắc, bố cục",
        "image_prompt": "An English prompt for Midjourney/DALL-E to generate this thumbnail, cinematic lighting, 8k resolution, photorealistic..."
    }}
    (Lưu ý mảng titles có 10 phần tử, tags có 25 phần tử).
    """
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return f"Lỗi AI: {str(e)}"

# --- 3. QUẢN LÝ TRẠNG THÁI ---
if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ KẾT NỐI AI")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    st.caption("v4.0 - Tích hợp AI Image Prompt & SEO Scoring")

# --- 4. GIAO DIỆN BƯỚC 1 ---
if st.session_state.step == 1:
    st.markdown('<div class="main-title">HỆ THỐNG SEO VIDEO AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #94a3b8; margin-bottom: 30px;">Tự động phân tích & Tối ưu mọi từ khóa</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("🌐 Ngôn ngữ", ["Tiếng Việt", "English"])
        ref = st.text_input("🔗 Link đối thủ (Tùy chọn)")
    with col2:
        kw = st.text_input("🎯 Từ khóa chính (Bắt buộc)")
        channel = st.text_input("📺 Tên kênh của bạn")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH CHUYÊN SÂU"):
        if kw and api_key:
            with st.spinner("🤖 Trí tuệ nhân tạo đang cào dữ liệu và phân tích..."):
                res = analyze_youtube_seo(api_key, kw, lang, ref)
                if isinstance(res, dict):
                    st.session_state.data = res
                    st.session_state.current_kw = kw
                    st.session_state.step = 2
                    st.rerun()
                else: st.error(res)
        else: st.warning("⚠️ Vui lòng nhập Từ khóa và API Key!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. GIAO DIỆN KẾT QUẢ ĐA TẦNG (TABS) ---
if st.session_state.step >= 2:
    st.markdown(f"### 📊 KẾT QUẢ TỐI ƯU: <span style='color:#3b82f6;'>{st.session_state.current_kw.upper()}</span>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 TIÊU ĐỀ", "🏷️ THẺ TAGS & HASHTAGS", "📄 KỊCH BẢN", "🎨 THUMBNAIL PROMPT"])
    data = st.session_state.data

    # TAB 1: TIÊU ĐỀ CHẤM ĐIỂM
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💡 10 Tiêu đề Tối ưu CTR (Click-through rate)")
        
        # Cho phép người dùng chọn tiêu đề yêu thích
        selected_titles = []
        for item in data.get('titles', []):
            title_text = item.get('text', '')
            score = item.get('score', 0)
            # Hiển thị Checkbox với điểm số
            if st.checkbox(f"{title_text} (Điểm SEO: {score}/100)", value=False, key=title_text):
                selected_titles.append(title_text)
                
        if selected_titles:
            st.divider()
            st.caption("Các tiêu đề bạn đã chọn (Copy bên dưới):")
            st.code("\n".join(selected_titles))
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 2: THẺ TAGS DỄ DÀNG COPY
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔍 Bộ Thẻ Tags chuẩn thuật toán")
        tags_list = data.get('tags', [])
        # Hiển thị dạng bong bóng cho đẹp
        tags_html = "".join([f'<span class="tag-bubble">{t}</span>' for t in tags_list])
        st.markdown(tags_html, unsafe_allow_html=True)
        # Hộp copy nhanh
        st.text_area("Copy toàn bộ Tags (dán thẳng vào Youtube):", ", ".join(tags_list), height=100)
        
        st.divider()
        st.subheader("#️⃣ Hashtags (Dành cho Tiêu đề & Mô tả)")
        st.code(" ".join(data.get('hashtags', [])))
        st.markdown('</div>', unsafe_allow_html=True)
        
    # TAB 3: MÔ TẢ & KỊCH BẢN
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📝 Mô tả Video chuẩn SEO")
        st.text_area("Nội dung mô tả (Copy):", data.get('description', ''), height=150)
        st.divider()
        st.subheader("🎬 Ý tưởng Kịch bản Video")
        st.info(data.get('script_idea', ''))
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 4: TẠO ẢNH BẰNG AI
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎨 Ý tưởng thiết kế (Tiếng Việt)")
        st.write(data.get('thumbnail_advice', ''))
        
        st.divider()
        st.subheader("🤖 Mã Lệnh Tạo Ảnh (AI Prompt)")
        st.caption("Copy đoạn mã Tiếng Anh dưới đây dán vào Midjourney, DALL-E hoặc ChatGPT để tạo ảnh tự động:")
        # Code block để copy nhanh bằng 1 click
        st.code(data.get('image_prompt', 'Generating prompt...'), language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 LÀM MỚI (TÌM TỪ KHÓA KHÁC)"):
        st.session_state.step = 1
        st.rerun()
