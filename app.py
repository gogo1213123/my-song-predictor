# import streamlit as st
# import joblib
# import requests
#
# # 加载模型
# vectorizer, model = joblib.load("genre_predictor.pkl")
#
# # 网易云本地API地址
# API_BASE = "http://localhost:3000"
#
# def get_artist_intro(artist_name):
#     """通过网易云API获取歌手简介"""
#     try:
#         # 1. 搜索歌手
#         search_url = f"{API_BASE}/search?keywords={artist_name}&type=100&limit=1"
#         resp = requests.get(search_url, timeout=5)
#         data = resp.json()
#         if data.get('result', {}).get('artists'):
#             artist = data['result']['artists'][0]
#             artist_id = artist['id']
#             # 2. 获取歌手详情
#             detail_url = f"{API_BASE}/artist/detail?id={artist_id}"
#             detail_resp = requests.get(detail_url, timeout=5)
#             detail = detail_resp.json()
#             intro = detail.get('data', {}).get('artist', {}).get('briefDesc', '')
#             if not intro:
#                 # 如果没有简介，尝试获取描述
#                 desc_url = f"{API_BASE}/artist/desc?id={artist_id}"
#                 desc_resp = requests.get(desc_url, timeout=5)
#                 desc_data = desc_resp.json()
#                 intro = desc_data.get('introduction', [{}])[0].get('ti', '暂无简介')
#             return intro
#         else:
#             return f"未找到歌手“{artist_name}”的相关信息"
#     except Exception as e:
#         return f"获取简介失败：{e}"
#
# st.set_page_config(page_title="音乐风格预测器", page_icon="🎵")
# st.title("🎤 音乐风格预测器")
# st.write("输入歌名和歌手，模型会预测歌曲风格；单独输入歌手名可查看简介")
# st.caption("⚠️ 只输入歌名可能导致预测不准确，建议同时输入歌手名")
# # 输入框
# user_input = st.text_input("查询内容", placeholder="例如：晴天 周杰伦  或  周杰伦")
#
# if user_input:
#     # 判断是歌名+歌手（包含空格）还是纯歌手
#     if " " in user_input:
#         # 歌名+歌手模式
#         X = vectorizer.transform([user_input])
#         genre = model.predict(X)[0]
#         st.success(f"预测风格：**{genre}**")
#         st.balloons()
#     else:
#         # 纯歌手模式，获取简介
#         with st.spinner("正在获取歌手简介..."):
#             intro = get_artist_intro(user_input)
#         st.info(f"🎤 歌手《{user_input}》简介：\n\n{intro}")


import streamlit as st
import joblib
import requests
import re

# ========== 页面配置 ==========
st.set_page_config(
    page_title="音乐风格预测器",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ========== 加载模型 ==========
@st.cache_resource
def load_model():
    vectorizer, model = joblib.load("genre_predictor.pkl")
    return vectorizer, model


vectorizer, model = load_model()

# 网易云本地API地址（需保持服务运行）
API_BASE = "http://localhost:3000"


def get_artist_intro(artist_name):
    """通过网易云API获取歌手简介"""
    try:
        search_url = f"{API_BASE}/search?keywords={artist_name}&type=100&limit=1"
        resp = requests.get(search_url, timeout=5)
        data = resp.json()
        if data.get('result', {}).get('artists'):
            artist = data['result']['artists'][0]
            artist_id = artist['id']
            detail_url = f"{API_BASE}/artist/detail?id={artist_id}"
            detail_resp = requests.get(detail_url, timeout=5)
            detail = detail_resp.json()
            intro = detail.get('data', {}).get('artist', {}).get('briefDesc', '')
            if not intro:
                desc_url = f"{API_BASE}/artist/desc?id={artist_id}"
                desc_resp = requests.get(desc_url, timeout=5)
                desc_data = desc_resp.json()
                intro = desc_data.get('introduction', [{}])[0].get('ti', '暂无简介')
            return intro
        else:
            return f"未找到歌手“{artist_name}”的相关信息"
    except Exception as e:
        return f"获取简介失败：{e}"


def get_song_lyrics(song_name, artist_name):
    """通过网易云API获取歌曲歌词"""
    try:
        # 搜索歌曲（歌名+歌手）
        search_url = f"{API_BASE}/search?keywords={song_name} {artist_name}&limit=1"
        resp = requests.get(search_url, timeout=5)
        data = resp.json()
        if not data.get('result', {}).get('songs'):
            return "未找到该歌曲的歌词"
        song_id = data['result']['songs'][0]['id']
        lyric_url = f"{API_BASE}/lyric?id={song_id}"
        lyric_resp = requests.get(lyric_url, timeout=5)
        lyric_data = lyric_resp.json()
        lyric = lyric_data.get('lrc', {}).get('lyric', '')
        if not lyric:
            return "该歌曲暂无歌词"
        lyric = re.sub(r'\[.*?\]', '', lyric).strip()
        if len(lyric) > 1500:
            lyric = lyric[:1500] + "\n...（歌词过长，已截断）"
        return lyric
    except Exception as e:
        return f"获取歌词失败：{e}"


# ========== 自定义CSS样式 ==========
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #f6f9fc 0%, #eef2f7 100%);
}
.main-title {
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(120deg, #2c3e66, #1a2a4f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.sub-desc {
    text-align: center;
    color: #527a9b;
    font-size: 1rem;
    margin-bottom: 1.8rem;
    font-weight: 400;
}
.input-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border-radius: 28px;
    padding: 1.5rem 1.8rem;
    box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.5);
    margin-bottom: 1.5rem;
}
.result-card {
    background: linear-gradient(135deg, #ffffff, #fafcfd);
    border-radius: 24px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    border-left: 6px solid #ff7a4a;
    margin-top: 1rem;
}
.genre-badge {
    font-size: 1.9rem;
    font-weight: 700;
    background: #ff7a4a;
    color: white;
    padding: 0.2rem 1.2rem;
    border-radius: 60px;
    display: inline-block;
    margin-top: 0.5rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.lyrics-card {
    background: #fffaf0;
    border-radius: 20px;
    padding: 1rem 1.5rem;
    border-left: 5px solid #ffaa44;
    margin-top: 1rem;
    font-family: monospace;
    white-space: pre-wrap;
    font-size: 0.9rem;
}
.info-card {
    background: #eef3fc;
    border-radius: 20px;
    padding: 1rem 1.5rem;
    border-left: 5px solid #3b82f6;
    margin-top: 1rem;
}
.stTextInput > div > div > input {
    border-radius: 40px;
    border: 1px solid #cfdfed;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    background-color: white;
    transition: all 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #ff7a4a;
    box-shadow: 0 0 0 2px rgba(255,122,74,0.2);
}
hr {
    margin-top: 2rem;
    margin-bottom: 1rem;
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ccc, transparent);
}
</style>
""", unsafe_allow_html=True)

# ========== 页面布局 ==========
st.markdown('<div class="main-title">🎵 音乐风格预测器</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-desc">基于歌名（+歌手）的AI风格分类 | 同时可显示歌词</div>', unsafe_allow_html=True)

# 主输入区：风格预测（支持歌名或歌名+歌手）
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    user_input = st.text_input(
        "查询内容",
        placeholder="例如：晴天 或 晴天 周杰伦",
        label_visibility="collapsed"
    )
    st.caption("💡 输入歌名（可选歌手）预测风格；若输入“歌名 歌手”还会额外显示歌词")
    st.markdown('</div>', unsafe_allow_html=True)

# 处理主输入（风格预测）
if user_input:
    with st.spinner("🎧 分析中..."):
        # 直接使用用户输入作为预测文本（模型已经习惯“歌名 歌手”格式，即使只有歌名也能工作）
        X = vectorizer.transform([user_input])
        genre = model.predict(X)[0]

    # 显示风格结果
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1rem; color:#5a6e8a;">🏷️ 预测风格</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="genre-badge">{genre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.balloons()

    # 如果输入包含空格，尝试获取歌词（视为“歌名 歌手”格式）
    if " " in user_input:
        parts = user_input.split(maxsplit=1)
        song = parts[0]
        artist = parts[1] if len(parts) > 1 else ""
        if artist:
            with st.spinner("🎶 正在获取歌词..."):
                lyrics = get_song_lyrics(song, artist)
            st.markdown('<div class="lyrics-card">', unsafe_allow_html=True)
            st.markdown("**📃 歌词**")
            st.text(lyrics)
            st.markdown('</div>', unsafe_allow_html=True)

# ========== 侧边栏：歌手简介查询 ==========
with st.sidebar:
    st.markdown("## 📖 查歌手简介")
    singer_input = st.text_input("输入歌手名", placeholder="例如：周杰伦", key="singer_input")
    if singer_input:
        with st.spinner("查询中..."):
            intro = get_artist_intro(singer_input)
        st.markdown('---')
        st.markdown(f"**{singer_input}**")
        st.write(intro)

# 页脚
st.markdown("---")
st.caption("✨ 模型基于真实歌单训练 · 支持流行/摇滚/电子/说唱/古典等11种风格")