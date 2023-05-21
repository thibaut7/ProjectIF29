#!/usr/bin/env python
# coding: utf-8

# In[19]:


import seaborn as sns
import pandas as pd
import numpy as np
df = pd.read_csv('kmeans.csv')

plot = df[ ['reference', 'statuses', 'agressivite', 'visibilite', 'friends',
           'frequenceAmi', 'hstag', 'hstagmoyenTweet']]


# In[20]:


# In[21]:


df.head(3)


# In[29]:


# plot = df[ ['reference', 'statuses', 'agressivite', 'visibilite','frequenceAmi' ,
          #  'hstag', 'hstagmoyenTweet','longMoyen','frequenceFollowers','followers']]
           ## 'frequenceMention', 'mention','frequenceAmi','friends','refermoyenTweet','retweet','reply', 'Nombreurl',
            ##'nombre_tweet']]
plot2 = df[['frequenceAmi', 'friends','frequenceMention','mention',
            'frequenceFollowers','followers','frequenceFavourite','favourites','frenquenTweet',
            'nombre_tweet','statuses']]


# In[32]:





# In[41]:


pd.plotting.scatter_matrix(plot2[0:1000])


# In[ ]:




