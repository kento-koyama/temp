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
        st.session_state['uploaded_images'].append(uploaded_file)
    st.session_state['current_index'] = 0  # インデックスをリセット

# 画像をbase64エンコードする関数
def image_to_base64(image_file):
    try:
        img = Image.open(image_file)
        img = img.convert('RGB')  # PNGなどの透過画像をRGBに変換
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"画像の処理中にエラーが発生しました: {str(e)}")
        return None

# Streamlitのインターフェース
st.title("ランダム画像表示アプリ")

if st.session_state['uploaded_images']:
    try:
        # 現在の画像ファイルを取得
        current_image_file = st.session_state['uploaded_images'][st.session_state['current_index']]
        
        # ファイルポインタをリセット
        current_image_file.seek(0)
        
        # 画像をbase64エンコード
        current_image_base64 = image_to_base64(current_image_file)
        
        if current_image_base64:
            # クリック可能な画像を表示
            clicked = clickable_images(
                [f"data:image/jpeg;base64,{current_image_base64}"],
                titles=[f"画像 {st.session_state['current_index'] + 1} / {len(st.session_state['uploaded_images'])}"],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "auto", "max-width": "100%"}
            )
            
            # クリックされたら次の画像に進む
            if clicked > -1:
                st.session_state['current_index'] = (st.session_state['current_index'] + 1) % len(st.session_state['uploaded_images'])
                st.experimental_rerun()
        else:
            st.error("画像の処理中にエラーが発生しました。")
    
    except Exception as e:
        st.error(f"予期せぬエラーが発生しました: {str(e)}")

    # デバッグ情報の表示
    st.write(f"アップロードされた画像の数: {len(st.session_state['uploaded_images'])}")
    st.write(f"現在のインデックス: {st.session_state['current_index']}")

else:
    st.write("画像をアップロードしてください。")
