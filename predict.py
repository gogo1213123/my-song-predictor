import joblib
vectorizer, model = joblib.load("genre_predictor.pkl")
new_song = input("晴天 周杰伦")#输入歌名和歌手
X = vectorizer.transform([new_song])
print(f"预测风格: {model.predict(X)[0]}")

