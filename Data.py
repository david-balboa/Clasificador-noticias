from Tools import clean_word
import pandas as pd

# To get the entire dataframe and be able to do queries on it
def get_data(data_url:str, index_col:str):
    return pd.read_csv(data_url, index_col=index_col)

# To get the total amount of news inside the DataFrame given
def get_news_count(data):
    return len(data)

# To get the total amoun of news for each topic "topic_col" inside the DataFrame given
def get_topic_news_count(data, topic_col:str):
    return data.groupby(topic_col).size()

# To get a sample of the data based on the percentage 'pct' given
def get_data_sample(data, pct:float):
    return data.sample(frac = pct)

'''
To get for each (valid) word in the news, a count of:
    1) how many times they appear: "n_occur"
    2) in how many news they appear: "n_news"
Output format: {word : {n_occur: value; n_news: value} }
'''
# Auxiliary function to update the count of the words
def update_word_count_result(result, article_words):
    already_appeared = []
    for word in article_words.split():
        word = clean_word(word)
        # filter 1-character words
        if len(word) < 2:
            continue
        # try to update counts for the word, else create new word object
        try:
            result[word]["n_occur"] += 1
            if word not in already_appeared:
                already_appeared.append(word)
                result[word]["n_news"] += 1
        except:
            result[word] = {"n_occur": 1, "n_news": 1}
            already_appeared.append(word)
    return

def get_word_count(data):
    result = dict()
    for n_id in data.index:
        article = data.loc[n_id]
        article_words = article["Title"].strip() + ' ' + article["Summary"].strip()
        update_word_count_result(result, article_words)
    return result

'''
To get for each (valid) word in the news and each topic, a count of:
    1) how many times they appear in the topic: "n_occuer"
    2) in how many news of the topic they appear: "n_newes"
Output format: {topic : {word : {n_occur: valor; n_news: valor} } }
'''
# Auxiliary function to update the count of words by topic
def update_word_topic_count_result(result, article_words, topic):  
    # build/update word object result using previous function: 'update_word_count_result'
    if topic not in result.keys():
        word_result = dict()  
    else:
        word_result = result[topic]

    update_word_count_result(word_result, article_words)
    result[topic] = word_result
    return


def get_word_topic_count(data):
    result = dict()
    for n_id in data.index:
        article = data.loc[n_id]
        article_words = article["Title"].strip() + ' ' + article["Summary"].strip()
        topic = article["Topic_2digit"]
        update_word_topic_count_result(result, article_words, topic)
    return result