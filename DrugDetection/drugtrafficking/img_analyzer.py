import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
from CustomLayers.inception_cell import Inception_cell
from CustomLayers.skip_connection import SkipConnection
from CustomLayers.cosine_annealing_scheduler import CosineAnnealingScheduler

with CustomObjectScope({'Inception_cell':Inception_cell,'SkipConnection':SkipConnection,'CosineAnnealingScheduler':CosineAnnealingScheduler}):
    model=load_model(r'Models\drug_sentiment_img.h5')

    
img_path=r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Images\im4.jpg'
img=tf.io.read_file(img_path)
img=tf.image.decode_jpeg(img,channels=3)
img=tf.image.resize(img,(256,256))
img/=255.0
img=tf.expand_dims(img,axis=0)
pred=model.predict(img)
print(pred)
pred=pred[0]
pred=tf.cast(tf.round(pred),tf.int32)
print(pred.numpy())