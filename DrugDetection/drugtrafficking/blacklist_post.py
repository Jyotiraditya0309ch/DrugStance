from .eg import get_data
from .eg3 import get_entire_data
from .CustomLayers.inception_cell import Inception_cell
from .CustomLayers.skip_connection import SkipConnection
from .CustomLayers.cosine_annealing_scheduler import CosineAnnealingScheduler
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
import numpy as np
import json

def preprocessing_img(img_path):
    img=tf.io.read_file(img_path)
    img=tf.image.decode_jpeg(img,channels=3)
    img=tf.image.resize(img,(256,256))
    img/=255.0
    return img

def get_blacklisted_post():
    with CustomObjectScope({'Inception_cell':Inception_cell,'SkipConnection':SkipConnection,'CosineAnnealingScheduler':CosineAnnealingScheduler}):
        model=load_model(r'drugtrafficking\Models\drug_sentiment_img.h5')
        
    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\susp_user.json','r') as file:
        blacklist_user_checker=json.load(file)
    
    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\safe_post.json','r') as file:
        safe_post_checker=json.load(file) 
        
    data=get_data()
    user_id=[]
    img_src=[]
    post_id=[]
    for inst in data:
        user_id.append(inst['user'])
        img_src.append(inst['imgSrc'])
        post_id.append(inst['post_id'])
    
    entire_data=get_entire_data()
    # print(blacklist_user_checker)
    
   
    for inst in entire_data:
        if inst['user'] in blacklist_user_checker:
            user_id.append(inst['user'])
            img_src.append(inst['imgSrc'])
            post_id.append(inst['post_id'])
    
    

    
    # with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\seen_post.json','r') as file:
    #     seen_post_checker=json.load(file)

  
    for uid,pid,src in zip(user_id,post_id,img_src):
        if pid in safe_post_checker:
            user_id.remove(uid)
            img_src.remove(src)
            post_id.remove(pid)
            
    
    
    input_img=[preprocessing_img(img_path) for img_path in img_src]
    input_img=np.array(input_img)
    pred=model.predict(input_img)
    pred=tf.cast(tf.round(pred),tf.int32)
    pred=pred.numpy()
    pred=[p[0] for p in pred]
    
    
    
    blacklist_user=[]
    blacklist_post=[]
    seen_post=[]
    safe_post=[]
    
    for uid,pid,img_sentiment in zip(user_id,post_id,pred):
        if img_sentiment==0:
            blacklist_user.append(uid)
            blacklist_post.append(pid)
        else:
            safe_post.append(pid)

            
    blacklist_user=list(set(blacklist_user))
    blacklist_user_info=[]
    for inst in data:
        if (inst['post_id'] in blacklist_post) :
            blacklist_user_info.append(inst)

    # seen_post_checker.extend(seen_post)
    blacklist_user_checker.extend(blacklist_user)
    safe_post_checker.extend(safe_post)
    
    
    blacklist_user_checker=list(set(blacklist_user_checker))
    safe_post_checker=list(set(safe_post_checker))
    
    

    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\susp_user.json','w') as file:
        json.dump(blacklist_user_checker,file)
    
    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\safe_post.json','w') as file:
        json.dump(safe_post_checker,file)
    
    blacklist_user_info.reverse()
    
    return blacklist_user_info




    