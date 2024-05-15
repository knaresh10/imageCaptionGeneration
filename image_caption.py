import pickle
import numpy as np
from keras.preprocessing import sequence
from keras.preprocessing import image
from IPython.display import Image, display
from bilstm1 import style_caption
from keras.applications.inception_v3 import InceptionV3
from tqdm import tqdm

def predict_caption(path):
    return path

unique = pickle.load(open('./unique.p', 'rb'))
word2idx = {val:index for index, val in enumerate(unique)}
idx2word = {index:val for index, val in enumerate(unique)}
max_len = 40

def preprocess_input(x):
    x /= 255.
    x -= 0.5
    x *= 2.
    return x

def preprocess(image_path):
    img = image.load_img(image_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

model = InceptionV3(weights='imagenet')
from keras.models import Model

new_input = model.input
hidden_layer = model.layers[-2].output
model_new = Model(new_input, hidden_layer)

def encode(image):
    image = preprocess(image)
    temp_enc = model_new.predict(image)
    temp_enc = np.reshape(temp_enc, temp_enc.shape[1])
    return temp_enc

from keras.models import load_model
t_model = load_model('./GPU_blstm_trial_model.h5')

def predict_captions_2(image):
    start_word = ["<start>"]
    e = encode(image) # this the output of cnn inceptionv3
    while True:
        par_caps = [word2idx[i] for i in start_word]
        par_caps = sequence.pad_sequences([par_caps], maxlen=max_len, padding='post')
        # print(image)
        # print(e)
        preds = t_model.predict([np.array([e]), np.array(par_caps)])
        word_pred = idx2word[np.argmax(preds[0])]
        start_word.append(word_pred)

        if word_pred == "<end>" or len(start_word) > max_len:
            break

    sentence = ' '.join(start_word[1:-1])
    
    #return sentence which contains the caption
    #output is returned
    return sentence
