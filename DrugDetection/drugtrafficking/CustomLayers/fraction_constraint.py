import tensorflow as tf
from tensorflow.keras.constraints import Constraint
class FractionConstraint(Constraint):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __call__(self,w):
        return tf.clip_by_value(w,0.0,1.0)