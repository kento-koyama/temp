import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# アップロードされた画像のリスト
if 'uploaded_images' not in st.session_state:
    st.session_state['uploaded_images'] = []

# 現在の画像インデックス
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

# アップロード機能を提供
uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# アップロードされたファイルをリストに保存
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file not in st.session_state['uploaded_images']:
            st.session_state['uploaded_images'].append(uploaded_file)

# 画像をHTMLとして表示してクリック可能にする関数
def get_clickable_image(image_file):
    img = Image.open(image_file)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img_str}" style="max-width:100%;cursor:pointer;" onclick="nextImage()">'

# JavaScriptを使用して画像をクリックしたときの動作を定義
js = """
<script>
function nextImage() {
    window.parent.postMessage({type: 'next_image'}, '*');
}
</script>
"""

# Streamlitのインターフェース
st.title("ランダム画像表示アプリ")

if st.session_state['uploaded_images']:
    # JavaScriptを挿入
    st.markdown(js, unsafe_allow_html=True)

    # 現在の画像を表示
    current_image = st.session_state['uploaded_images'][st.session_state['current_index']]
    st.markdown(get_clickable_image(current_image), unsafe_allow_html=True)

    # JavaScriptからのメッセージを受け取る
    if st.session_state.get('next_image', False):
        st.session_state['current_index'] = (st.session_state['current_index'] + 1) % len(st.session_state['uploaded_images'])
        st.session_state['next_image'] = False
        st.experimental_rerun()

    # JavaScriptからのメッセージをキャッチするためのコンポーネント
    st.markdown("""
        <script>
        window.addEventListener('message', function(e) {
            if (e.data.type === 'next_image') {
                window.parent.postMessage({
                    type: 'streamlit:set_component_value',
                    key: 'next_image',
                    value: true
                }, '*');
            }
        });
        </script>
    """, unsafe_allow_html=True)
else:
    st.write("画像をアップロードしてください。")