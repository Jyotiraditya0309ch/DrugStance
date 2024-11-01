from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import BatchNormalization,Conv2D,Concatenate
class SkipConnection(Layer):
    def __init__(self,num_filters,kernel_size,activation='relu',padding='same',kernel_initializer='he_normal',**kwargs):
        super().__init__(**kwargs)
        self.num_filters=num_filters
        self.activation=activation
        self.padding=padding
        self.kernel_size=kernel_size
        self.kernel_initializer=kernel_initializer
        self.conv=Conv2D(self.num_filters,(7,7),activation=self.activation,padding=self.padding,kernel_initializer=self.kernel_initializer)
        self.batch_normalization=BatchNormalization()
        
    def call(self,input):
        x=self.conv(input)
        x=self.batch_normalization(x)
        x=Concatenate(axis=-1)([x,input])
        return x
        
    def get_config(self):
        config=super().get_config()
        config.update({
            'num_filters':self.num_filters,
            'activation':self.activation,
            'padding':self.padding,
            'kernel_size':self.kernel_size,
            'kernel_initializer':self.kernel_initializer
        })
        return config
        
        