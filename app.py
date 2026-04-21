import streamlit as st
import joblib

# 加载模型
vectorizer, model = joblib.load("genre_predictor.pkl")

st.set_page_config(page_title="音乐风格预测器", page_icon="🎵")
st.title("🎤 音乐风格预测器")
st.write("输入歌名和歌手，模型会预测歌曲风格（流行、摇滚、电子、民谣、说唱、古典、爵士等）")

# 输入框
song_input = st.text_input("歌曲信息", placeholder="例如：晴天 周杰伦")

if song_input:
    # 预测
    X = vectorizer.transform([song_input])
    genre = model.predict(X)[0]
    st.success(f"预测风格：**{genre}**")
    st.balloons()  # 撒花效果