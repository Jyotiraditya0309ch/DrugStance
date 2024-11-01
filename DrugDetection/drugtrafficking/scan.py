import numpy as np
import tensorflow as tf
import pandas as pd
import json
from tensorflow.keras.preprocessing.text import Tokenizer,tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from .CustomLayers.weighted_layer import WeightedLayer
from .CustomLayers.fraction_constraint import FractionConstraint
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.models import load_model

with CustomObjectScope({'WeightedLayer':WeightedLayer,'FractionConstraint':FractionConstraint}):
    model=load_model('drugtrafficking/Models/drug_sentiment_model.h5')
    
with open('drugtrafficking\Models\drug_sentiment_tokenizer.json','r') as file:
    tokenizer_json=file.read()

""" tokenizer=tokenizer_from_json(tokenizer_json)
text=input("Enter the text:")
text=[text]
seq=tokenizer.texts_to_sequences(text)
seq=pad_sequences(seq,maxlen=12,padding='post',truncating='post')
pred=model.predict(seq)
print(pred)         """



