# train_genre_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 读取数据
df = pd.read_csv("songs.csv")
# 构造文本特征：歌名 + 歌手
df["text"] = df["song_name"] + " " + df["artist"]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["genre"], test_size=0.2, random_state=42
)

# 特征提取
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 训练模型
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# 评估
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# 保存模型
joblib.dump((vectorizer, model), "genre_predictor.pkl")
print("模型已保存为 genre_predictor.pkl")