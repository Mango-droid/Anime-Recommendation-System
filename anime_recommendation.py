# importing all the necessaary libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import Levenshtein
#reading the anime dataframe
df = pd.read_csv("anime.csv")


#function to replace NaN with empty string in description
def replaceNull(df):
    return df.fillna("")

df = replaceNull(df)

#function to remove /xa0 from description string (not necessary)
def removexa0(column):
    try:
        return column['description'].replace('\xa0', ' ')
    except:
        print(column[8])
#The columns studios, tags and content are all strings(not lists), so we have to remove "[", "'", "," and "]" 
#from these strings. cleaningStrings function will do that for us.

def cleaningStrings(df, column):
    return df[column].apply(lambda x: x.replace("[","")).apply(lambda x: x.replace("'",""))\
    .apply(lambda x: x.replace(",","")).apply(lambda x: x.replace("]",""))



#function to join all the strings of studios, tags and contentWarn in a single string
def keywords(column):
    try:
        return column["studios"]+" "+column["tags"]+" "+column["contentWarn"]
    except:
        print(column)


pd.options.mode.chained_assignment = None


#list of all the titles in with index in the form of a tuple
def getTitlesList(Df):
    return list(enumerate(Df['title'].tolist()))



#Following two helper functions can help us to get the index of a title from dataframe and vice versa.
def get_title_from_index(df,index):
    return df[df.index == index]["title"].values[0]
def get_index_from_title(df,title):
    return df.index[df['title'] == title].values[0]

#if you dont input the exact name of an anime with correct spellings, following function will allow you to
#pick the anime that has the closest name to it. For example, if you search for the title 
#'code geass lelouch of rebellion', it will be changed to the correct title i.e. 'Code Geass: Lelouch of the Rebellion?'
def actualTitle(my_title):
    title_similarities = []
    i = 0
    titles_list = getTitlesList(mainDf)
    for i in range(len(titles_list)):
        title_similarities.append(Levenshtein.ratio(my_title,titles_list[i][1]))
    title_similarities = list(enumerate(title_similarities))
    sorted_title_similarities = sorted(title_similarities,key = lambda x:x[1],reverse=True)
    actual_title = get_title_from_index(mainDf,sorted_title_similarities[0][0])
    return actual_title



#main function
if __name__=='__main__':

    anime_you_like = input("Enter the name of the anime you like: ")
    #reading the anime dataframe
    df = pd.read_csv("anime.csv")

    #handling missing values
    df = replaceNull(df)

    #applying the removexa0 function on the dataframe.
    df['description'] = df.apply(removexa0,axis=1)
    
    #columns studios, tags and contentWarn are all in string format so we have to clean them.
    df["studios"] = cleaningStrings(df,"studios")
    df["tags"] = cleaningStrings(df,"tags")
    df["contentWarn"] = cleaningStrings(df,"contentWarn")

    #mainDf contains the columns which we require for running the recommendation algorithm. 
    mainDf = df [["title","description","studios","tags","contentWarn"]]

    #applying the keywords function and making a new column of a string that will be used for measuring the similarity matrix
    #and building our recommendation system
    mainDf['keywords'] = mainDf.apply(keywords,axis = 1)
    
    #getting the actual title (ignoring spelling mistakes)
    actual_title = actualTitle(anime_you_like)
    print("\n")
    if (anime_you_like!=actual_title):
        print(f"Did you mean {actual_title}?")
    
    print("\n")
    print(f"Searching for anime like {actual_title}...")
    
    #making a countVectorizer object and finding the word count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(mainDf["keywords"])

    #measuring the similarity scores in the fom of a matrix
    similarity_scores = cosine_similarity(count_matrix)

    
    
    
    try:
        anime_index = get_index_from_title(mainDf, actual_title)
    except:
        print("an error occured")
    #adding index in similarity scores and converting in the form of a list of tuples with
    #dataframe index at [0] and similarity score at [1]
    similar_anime = list(enumerate(similarity_scores[anime_index]))

    #sorting the list of tuples by similarity score in descending order
    sorted_similar_anime = sorted(similar_anime,key = lambda x: x[1], reverse=True)
    
    
    print("\n")
    print(f"Top 10 anime like {actual_title} are as follows: ")
    print(".................")
    i=0
    for anime in sorted_similar_anime:
        if i>=1:
            print (get_title_from_index(mainDf, anime[0]))
        i+=1
        if i>10:
            break
    print(".................")


#list of all the titles in with index in the form of a tuple
titles_list = list(enumerate(mainDf['title'].tolist()))




