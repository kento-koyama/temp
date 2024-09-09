import streamlit as st
import base64
import streamlit.components.v1 as components

# 画像アップロード
uploaded_files = st.file_uploader("画像を選択してください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# アップロードされた画像が存在するかチェック
if uploaded_files:
    # アップロードされた画像のリストをbase64エンコードしてJavaScriptで利用可能にする
    image_list = []
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        base64_encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        image_list.append(f"data:image/jpeg;base64,{base64_encoded_image}")

    # HTMLとJavaScriptで画像のクリックイベントを処理する
    html_code = f"""
        <div id="image-container" style="text-align:center;">
            <img id="main-image" src="{image_list[0]}" style="max-width:100%; cursor: pointer;" onclick="nextImage()"/>
        </div>

        <script type="text/javascript">
            var images = {image_list};
            var currentIndex = 0;

            function updateImage() {{
                var imgElement = document.getElementById("main-image");
                imgElement.src = images[currentIndex];
            }}

            function nextImage() {{
                currentIndex = (currentIndex + 1) % images.length;
                updateImage();
            }}
        </script>
    """

    # HTMLを埋め込む
    components.html(html_code, height=400)
else:
    st.write("画像をアップロードしてください。")
