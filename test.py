import streamlit as st
from st_clickable_images import clickable_images
from PIL import Image
import base64
import io

# セッション状態の初期化
if 'uploaded_images' not in st.session_state:
    st.session_state['uploaded_images'] = []
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

# アップロード機能を提供
uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# アップロードされたファイルをリストに保存
if uploaded_files:
    st.session_state['uploaded_images'] = []  # リストをリセット
    for uploaded_file in uploaded_files:
        image_bytes = uploaded_file.read()
        st.session_state['uploaded_images'].append(image_bytes)
    st.session_state['current_index'] = 0  # インデックスをリセット

# 画像をbase64エンコードする関数
def image_to_base64(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlitのインターフェース
st.title("ランダム画像表示アプリ")

if st.session_state['uploaded_images']:
    # 現在の画像をbase64エンコード
    current_image = image_to_base64(st.session_state['uploaded_images'][st.session_state['current_index']])
    
    # クリック可能な画像を表示
    clicked = clickable_images(
        [current_image],
        titles=[f"画像 {st.session_state['current_index'] + 1} / {len(st.session_state['uploaded_images'])}"],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "auto", "max-width": "100%"}
    )
    
    # クリックされたら次の画像に進む
    if clicked > -1:
        st.session_state['current_index'] = (st.session_state['current_index'] + 1) % len(st.session_state['uploaded_images'])
        st.experimental_rerun()

else:
    st.write("画像をアップロードしてください。")
