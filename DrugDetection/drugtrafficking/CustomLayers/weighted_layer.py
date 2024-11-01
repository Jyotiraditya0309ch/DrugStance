from tensorflow.keras.layers import Layer
import tensorflow as tf
from .fraction_constraint import FractionConstraint
from tensorflow.keras.layers import Add
class WeightedLayer(Layer):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.lstm_weight=self.add_weight(
            name='lstm_model_weightage',
            initializer=tf.constant_initializer(0.7),
            trainable=True,
            constraint=FractionConstraint()
        )
        self.cnn_weight=1-self.lstm_weight
        
    def call(self,lstm,cnn):
        lstm_out=self.lstm_weight*lstm
        cnn_out=self.cnn_weight*cnn
        out=Add()([lstm_out,cnn_out])
        return out
        
        