import cv2
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.layers import GlobalAveragePooling2D 

def model_initalize():
    # include_top = False means that we doesnt include fully connected top layer we will add them accordingly
    mobilenetV2 = MobileNetV2(include_top = False, input_shape = (224,224,3), weights = 'imagenet')

    # training of all the convolution is set to false
    for layer in mobilenetV2.layers:
        layer.trainable = False

    x = GlobalAveragePooling2D()(mobilenetV2.output)    
    predictions = Dense(3, activation='softmax')(x)
    model_mobilenetV2 = Model(inputs = mobilenetV2.input, outputs = predictions)
    model_mobilenetV2.load_weights('model_mobilenetV2.h5')
    return model_mobilenetV2

model = model_initalize()

def getPrediction(image):
    image = img_to_array(image)
    image = cv2.resize(image, (224,224))
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)

    doctor = False

    if yhat[0][0] > 0.75 or yhat[0][1] > 0.75 or yhat[0][2] > 0.75:
        doctor = True 

    return 'FMD', str(yhat[0][0]), 'IBK', str(yhat[0][1]), 'LSD', str(yhat[0][2]), doctor

