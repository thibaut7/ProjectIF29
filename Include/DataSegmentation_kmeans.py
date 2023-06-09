
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import csv
#read kmeans.csv and delete the column of tweet
with open('./datasets/kmeans.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]
data = [row[:16] + row[17:] for row in data]
# close file
file.close()
# define header
header = [" ",'_id', 'userCreateDate', 'Maxfollowers', 'Minfollowers', 'retweet', 'reply', 'MaxAmi', 'MinAmi',
          'MaxStatuses', 'MinStatuses', 'Maxfavourites', 'Minfavourites', 'Maxmention', 'Minmention', 'nombre_tweet',
           'longTotalTweet', 'hstag', 'reference', 'Nombreurl', 'dateMax', 'dateMin', 'DateUser',
          'statuses', 'friends', 'favourites', 'mention', 'followers', 'agressivite', 'frenquenTweet',
          'frequenceAmi', 'longMoyen', 'frequenceFavourite', 'frequenceMention', 'frequenceFollowers',
          'hstagmoyenTweet', 'refermoyenTweet', 'visibilite']

# Extract data in segments and write to multiple CSV files
#creating only 50 files at a time
for i in range(50):
    data_subset = data[(0 + 1000*i):(1000 + 1000*i)]
    data_subset.insert(0,header)
    with open(f'./datasets/label{0+1000*i}-{1000+1000*i}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_subset)
    print(f"create label{0+1000*i}-{1000+1000*i}.csv successfully")
# kmeans
for i in range(50) :
    file = f'label{0+1000*i}-{1000+1000*i}.csv'
    df = pd.read_csv(f'.\\datasets\\{file}')
    # select specific columns
    plot = df[[ 'agressivite', 'visibilite',
            'hstag', 'hstagmoyenTweet','longMoyen','frequenceFollowers',
            'frequenceMention','frequenceAmi','refermoyenTweet','retweet','reply', 'Nombreurl',
            'frenquenTweet','frequenceFavourite']]
    X = plot.values
    # Standardization
    X = StandardScaler().fit_transform(X)
    # start clustering
    clustering = KMeans(n_clusters=2)
    clustering.fit(X)
    #get label
    labels = clustering.labels_
    label = pd.DataFrame(labels, columns=['labels'])
    if label["labels"].value_counts().get(0, 0) > label["labels"].value_counts().get(1, 0) :
        label["labels"] = label["labels"].replace({0: 1,1:-1})
    else :
        label["labels"]= label["labels"].replace({0: -1})
    df['label'] = label['labels']
    df.to_csv(f'.\\datasets\\{file}', index=False)
    print(f"{file} clustering DONE")
