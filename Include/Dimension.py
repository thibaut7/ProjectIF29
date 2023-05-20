#!/usr/bin/env python
# coding: utf-8

# In[43]:


from pymongo import MongoClient
import csv
import time
import pandas as pd
import re


# In[75]:


myclient = MongoClient("mongodb://localhost:27017/")
db = myclient.ProjectIF29
collection = db['Tweets']


# ### Generer les attributs du graphe social 

# **_id**: id du user\
# **friends_count** : nombre de profils suivis\
# **followers_count**: nombre de followers ou d'abonnees\
# **listed_count**: le nombre de mention publique pour cet utilisateur\
# **statuses_count**: le nombre de tweet et retweet emis par le user\
# **favourites_count**: nombre de favoris ou nombre de tweets likés depuis la creation du compte \
# **accounted_created_time**: jour et heure de la creation du compte\
# **tweet_created_time** : jour et heure de la creation du tweet\
# **Age du profil**: du premier tweet au dernier tweet\
# **agressivite**\
# **visibilite**\
# **nombre d'url**\
# **longueur moyen des tweets**\
# **nombre de reponses**\
# **retweet_count**: Nombre de fois que ce tweet a ete retweete\
# **reply_count**: Nombre de fois que ce tweet a ete repondu\
# **favorite_count**: Nombre de fois que ce tweet a ete like

# ### Chercher le nombre d'utilisateur dans la base

# In[3]:


Nombre_utilisateur = []
for user in collection.aggregate([
    {
        "$group": {"_id": "$user.id"}
    }]):
    Nombre_utilisateur.append(user)
len(Nombre_utilisateur)


# In[57]:


collection.create_index([("user,id", 1)])


# In[76]:


from bson.code import Code
debut = time.time()
#-------fonction pour calculer la longueur moyen d'un tweet---------------

longtweet = Code('''
function(tweets) {
        return tweets.length;}
''')

#------------fonction pour calculer le nombre moyen de hshtag et de reference
hsref = Code('''
function(tweets) {
        var total = 0;
        total += tweets.split('#').length - 1;
        return total;
}''')

ref = Code('''
function(tweets) {
        var total = 0;
        total += tweets.split('@').length - 1;
        return total;
}''')
#--------nombre url------- 
NombreUrl = Code('''function (text) {
  // Expression régulière pour trouver les URL
  var urlRegex = /https?:\/\/[^\s/$.?#].[^\s]*/gi;
  
  // Trouver toutes les correspondances avec la regex
  var matches = text.match(urlRegex);
  
  // Renvoyer le nombre total d'URL trouvées
  return matches ? matches.length : 0;
}
''')
dateMin = Code('''
function(created_at){
        var total = Date.parse("Sun May 15 12:34:56 +0000 2023");
        for (var doc of created_at) {
            total = Math.min(total, Date.parse(doc));
        };
        return total;}
''')
dateMax = Code('''
function(created_at){
        return  Date.parse(created_at);}
''')    
  
age = collection.aggregate([
    {
        '$group': {
            '_id': '$user.id',
            'userCreateDate':{'$first': '$user.created_at'},
            'Maxfollowers': {'$max': '$user.followers_count'},
            'Minfollowers': {'$min': '$user.followers_count'},
            'retweet':{'$sum': '$retweet_count'},
            'reply':{'$sum':'$reply_count'},
            'MaxAmi':{'$max':'$user.friends_count'},
            'MinAmi':{'$min': '$user.friends_count'},
            'MaxStatuses':{'$max':'$user.statuses_count'},
            'MinStatuses':{'$min':'$user.statuses_count'},
            'Maxfavourites':{'$max':'$user.favourites_count'},
            'Minfavourites':{'$min':'$user.favourites_count'},
            'Maxmention': {'$max':'$user.listed_count'},
            'Minmention':{'$min':'$user.listed_count'},
            'tweets':{'$push': '$text'},
             'nombre_tweet':{'$count':{}},
            'longTotalTweet':{'$sum':{'$function':{'body':longtweet, 'args':['$text'],'lang':'js'}}},
            'hstag':{'$sum':{'$function':{'body':hsref, 'args':['$text'], 'lang':'js'}}},
            'reference':{'$sum':{'$function':{'body':ref, 'args':['$text'], 'lang':'js'}}},
            'Nombreurl':{'$sum':{'$function':{'body': NombreUrl, 'args':['$text'], 'lang':'js'}}},
            'dateMax':{'$max':{'$function':{'body': dateMax, 'args':['$created_at'], 'lang':'js'}}},
            'dateMin':{'$min':{'$function':{'body': dateMax, 'args':['$created_at'], 'lang':'js'}}},
            'DateUser':{'$min':{'$function':{'body': dateMax, 'args':['$user.created_at'], 'lang':'js'}}}
        }
    }
])
        
entetes=['_id', 'userCreateDate', 'Maxfollowers', 'Minfollowers', 'retweet', 'reply','MaxAmi','MinAmi','MaxStatuses','MinStatuses','Maxfavourites','Minfavourites'
        ,'Maxmention','Minmention', 'nombre_tweet', 'tweets','longTotalTweet', 'hstag', 'reference','Nombreurl', 'dateMax', 'dateMin','DateUser']
with open('User.csv', 'w', newline='', encoding ='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=entetes)
    writer.writeheader()
    writer.writerows(age)
print('---------------------------Temps execution')
print(time.time()-debut)


# In[77]:


df = pd.read_csv('User.csv')
##----------Affichons les 5 premiers elements--------
df.head(5)


# ### Age de l'univers- Age des profils
# Par l'age du profil, nous entendons la difference entre le premier tweet et le dernier tweet
# 

# In[78]:


start = time.time()
debut_univers = df['dateMin'].min()
fin_univers = df['dateMax'].max()
print('-----Temps execution-------')
print(time.time()-start)


# In[79]:


print(debut_univers)


# In[80]:


print(fin_univers)


# ### Calcul des attributs suivants dans l'univers

# **statuses_count**\
# **friends_count**\
# **favourite_count**\
# **listed_count**\
# **followers_count**\
# **nombre_url**\
# **longueur total d'un tweet**\
# **frequencetweet**\
# **longueumoyen**
# 

# In[81]:


start = time.time()
def statuses(df):
    return df['MaxStatuses']-df['MinStatuses']
#----------nombre de tweets dans univers----------------------
df['statuses'] = df.apply(statuses, axis =1)
#------------nombre friend----------------
def friend(df):
    return df['MaxAmi'] - df['MinAmi']
df['friends'] = df.apply(friend, axis = 1)
#------------nombre favourite-------------------------------
def favourite(df):
    return df['Maxfavourites'] - df['Minfavourites']
df['favourites'] = df.apply(favourite, axis =1)
#---------------nombre de mention-----------------------
def mention(df):
    return df['Maxmention']-df['Minmention']
df['mention'] = df.apply(mention, axis =1)
#------------nombre de followers----------------
def followers(df):
    return df['Maxfollowers'] - df['Minfollowers']
df['followers'] = df.apply(followers, axis = 1)
#---------Compiler l'agressivite -----
def agressivite(df):
    return (df['statuses'] + df['friends'])/350
df['agressivite'] = df.apply(agressivite, axis = 1)
print('---------------------------Temps execution')
print(time.time() - start)


# In[ ]:


#---------frequence de tweet------------------------
start = time.time()
def frequencetweet(df):
    return df["statuses"]/(df['dateMin'] - fin_univers)
df['frenquenTweet'] = df.apply(frequencetweet, axis = 1)
#-------------frenquence friends-------------------------
def frequenceAmi(df):
    return df['MaxAmi']/(df['dateMin'] - fin_univers)
df['frequenceAmi'] = df.apply(frequenceAmi, axis =1)
#----------longueur moyen de tweet-----------------------
def longueurmoyen(df):
    return df['longTotalTweet']/df['nombre_tweet']
df['longMoyen'] = df.apply(longueurmoyen, axis = 1)
print('----------------Temps execution:')
print(start - time.time())


# La determination dans la cellule precendente des frequences dans l'univers pose probleme, car l'age du dernier tweet serait 0 et ses frequence seraient difficiles à calculer à cause du zéro au denominateur. 
# Pour celà nous reprenons le calcul en se basant sur la durée l'age du user depuis la création de son compte

# In[85]:


#-------------frequence de tweet------------------------
start = time.time()
def frequencetweet(df):
    return df["MaxStatuses"]/(df['dateMax']-df['DateUser'] )
df['frenquenTweet'] = df.apply(frequencetweet, axis = 1)
#-------------frenquence friends-------------------------
def frequenceAmi(df):
    return df['MaxAmi']/(df['dateMax']-df['DateUser'] )
df['frequenceAmi'] = df.apply(frequenceAmi, axis =1)
#-------------frequence favorites-----------------------
def frequencefavorite(df):
    return df['Maxfavourites']/(df['dateMax']-df['DateUser'] )
df['frequenceFavourite'] = df.apply(frequencefavorite, axis = 1)
#------------frequence mention-------------------------
def frequenceMention(df):
    return df['Maxmention']/(df['dateMax']-df['DateUser'] )
df['frequenceMention'] = df.apply(frequenceMention, axis =1)
#-----------frequence followers------------------------
def frequenceFollowers(df):
    return df['Maxfollowers']/(df['dateMax']-df['DateUser'] )
df['frequenceFollowers'] = df.apply(frequenceFollowers, axis =1)
#-------------longueur moyen de tweet--------------------
def longueurmoyen(df):
    return df['longTotalTweet']/df['nombre_tweet']
df['longMoyen'] = df.apply(longueurmoyen, axis = 1)
#-------------
print('----------------Temps execution:')
print(time.time()-start)


# In[86]:


df.shape


# ### Calcul des nouveaux champs

# Dans le but de déterminer l'age d'un utilisateur dans l'Univers, nous allons chercher la date du commencement de l'univers
# (date du premier twitter recueillie dans l'univers) et la date de fin de l'univers(la date du dernier tweet)\
# Pour ce faire nous allons d'abord :
# 

# #### - Convertir les dates et les mettre dans un nouveau champs Tmin(date premier tweet en seconde) et Tmax(date dernier tweet en seconde) et sortir le min et le max

# **longueur moyen tweet**\
# **frequence_statuses**\
# **frequence_friends**

# In[87]:


df.head(5)


# In[90]:


df.describe()


# In[99]:


def hstagmoyenTweet(df):
    return df['hstag']/df['nombre_tweet']
df['hstagmoyenTweet'] = df.apply(hstagmoyenTweet, axis = 1)
#--------------------------------------------------------------
def refermoyenTweet(df):
    return df['reference']/df['nombre_tweet']
df['refermoyenTweet'] = df.apply(refermoyenTweet, axis = 1)
print('----------------------------')


# ### Determination des couts du hastag(#) et du tag(@)
# Pour calculer le nombre les couts du hashtag(#) et de tag(@). Nous allons baser sur le fait que ces actions attirent la visibilité; c'est à dire le nombre de **friends**,**followers**,**mention**, **favourites** et que la moyenne hashtag provoque la somme des moyennes de ces elements. Par regle de 3 nous estimons que la valeurs ou le cout est le nombre moyen de ces elements que produirait 1 hashtag ou 1 reference

# In[112]:


df['hstag'].mean()/((df['friends']/df['nombre_tweet']).mean()+(df['favourites']/df['nombre_tweet']).mean()+
(df['mention']/df['nombre_tweet']).mean()+ (df['followers']/df['nombre_tweet']).mean())
                             


# In[101]:


df['refermoyenTweet'].mean()/(df['friends'].mean()+df['favourites'].mean()+df['mention'].mean()+df['followers'].mean())


# ### Calcul de la visibilite

# In[113]:


start = time.time()
def visibilite(df):
    return (df['hstagmoyenTweet']*11.6 + df['reference']*11.4)/140
df['visibilite'] = df.apply(visibilite, axis=1)
print(time.time()-start)


# In[114]:


df.to_csv('kmeans.csv', sep=',')
print('fin')


# ### Creer la base de donnees Mongodb des Users

# In[ ]:


##Transformer la dataframe en dictionnaire
start = time.time()
df_dict = df.to_dict('records')
print('-------------------------------Temps execution')
print(time.time() - start)


# In[ ]:


##Inserer le dictionnaire 
user = db['utilisateur']
start = time.time()
collection.insert_many(df_dict)
print('-----------------------------Temps execution')
print(time.time() - start)


# In[39]:


df.head(5)

