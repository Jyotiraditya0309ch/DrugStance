
import tensorflow as tf
from .CustomLayers.fraction_constraint import FractionConstraint
from .CustomLayers.weighted_layer import WeightedLayer
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string


def preprocessing_text(text):
    table=str.maketrans('','',string.punctuation)
    pre_text=[]
    for inst in text:
        sent=""
        words=inst.split(" ")
        for word in words:
            word=word.translate(table)
            if word.isalpha():
                word=word.lower()
                sent+=word
                sent+=" "
                
        pre_text.append(sent.strip())
        
    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\drug_sentiment_tokenizer.json','r')as file:
        tokenizer_json=file.read()
        
    tokenizer=tokenizer_from_json(tokenizer_json)
    inp=tokenizer.texts_to_sequences(pre_text)
    inp_seq=pad_sequences(inp,maxlen=12,padding='post',truncating='post')
    return inp_seq

def get_user_data_from_id(id,keyword):
    from .eg1 import get_data
    user_data=get_data()
    data={}
    for inst in user_data:
        if inst['id']==id:
            data[keyword+'_id']=inst['id']
            data[keyword+'_username']=inst['username']
            data[keyword+'_name']=inst['firstname']+' '+inst['surname']
            data[keyword+'_location']=inst['location']
            data[keyword+'_ip_address']=inst['ipaddress']
    return data


def get_drug_dealer_customer_data():
    from .eg import get_data
    data=get_data()
    
    comments=[]
    comment_user_id=[]
    post_user_id=[]
    for inst in data:
        if inst['comments']:
            comments.extend(inst['comments'])
            comment_user_id.extend(inst['comment_authors'])
            post_user_id.extend(len(inst['comments'])*[inst['user']])
            
    comment_user_id=[int(x) for x in comment_user_id]
    with CustomObjectScope({'FractionConstraint':FractionConstraint,'WeightedLayer':WeightedLayer}):
        model=load_model(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\drug_sentiment_model.h5')
        
    inp_seq=preprocessing_text(comments)   
    pred=model.predict(inp_seq)
    pred=tf.cast(tf.round(pred),tf.int32).numpy()
    predictions=[p[0] for p in pred]
    
    drug_dealer=[]
    drug_customer=[]
    drug_comment=[]
    for uid,cid,comm,pred in zip(post_user_id,comment_user_id,comments,predictions):
        if pred==1:
            drug_dealer.append(uid)
            drug_customer.append(cid)
            drug_comment.append(comm)
            
    drug_dealer_customer_info=[]
    for did,cid,com in zip(drug_dealer,drug_customer,drug_comment):
        data={}
        data['dealer_data']=get_user_data_from_id(did,'drug_dealer')
        data['customer_data']=get_user_data_from_id(cid,'drug_customer')
        data['comments']=com
        drug_dealer_customer_info.append(data)
    
    return drug_dealer_customer_info

# print(get_drug_dealer_customer_data())
        
                
    