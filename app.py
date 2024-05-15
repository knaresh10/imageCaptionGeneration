#region 
from bilstm1 import style_caption
#endregion
#flask code
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, render_template, request, jsonify
import os
from image_caption import predict_captions_2
from text_to_speech import text_to_speech
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        image_path = os.path.join(app.root_path, 'static', 'images', image.filename)
        image.save(image_path)
        caption = predict_captions_2(image_path) #output of the model
        #region
        caption = style_caption(image_path, caption)
        #endregion
        #return caption
        return caption 
    return 'Error : No image uploaded'


@app.route('/play_speech', methods=['POST'])
def play_speech():
    data = request.get_json()
    text = data.get('text')
    if text : 
        text_to_speech(text)
        return jsonify({'message': 'Speech played successfully'})
    return jsonify({'error': 'No text provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)