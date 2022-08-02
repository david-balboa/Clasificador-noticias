from Data import *
from Tools import *
import random as rnd
import numpy as np
import math as mt

# auxiliary function to decide if a given word should be discarded from the topNword value or not
def should_be_discarded(data, words_dictionary, word):
    n_news = get_news_count(data)
    return (words_dictionary[word]["n_occur"] / n_news > 0.03) or (words_dictionary[word]["n_news"] / n_news > 0.03)

# to obtian a dictionary where the topic will be the keys and an sorted array of top words will be the values
def get_top_N_words(data, words_dictionary, words_topic_dictionary, news_per_topic, N):
    top_words = dict()
    for topic in words_topic_dictionary.keys():
        word_freq = dict()
        for word in words_topic_dictionary[topic].keys():
            if (not should_be_filtered(word)) and (not should_be_discarded(data, words_dictionary, word)):
                word_freq[word] = 1 - words_topic_dictionary[topic][word]["n_news"] / news_per_topic[topic]
    
        top_words[topic]  = [item[0] for item in sorted(word_freq.items(), key=lambda l: l[1], reverse=False)][:N]
            
    return top_words

# To get a list of all the representative words (without repetition)
def get_selected_words(top_words):
    selected_words = []
    for topic in top_words.keys():
        selected_words += [word for word in top_words[topic] if word not in selected_words]
    return selected_words

# To create the features vector for a given list of words ('article_words') based on the representative words given ('selected_words')
def create_features_vector(selected_words, article_words):
    # initialize features vector
    features = np.array([False for index in range(len(selected_words))])
    for word in article_words:
        word = clean_word(word)
        if not should_be_filtered(word):
            for i,w in enumerate(selected_words):
                if (w == word):
                    features[i] = True
                    break
    return features

# To obtain for each news ID the features vector related
def create_features(data, selected_words):
    dict_features = dict()
    for n_id in data.index:
        # get words from article
        article = data.loc[n_id]
        article_words = article["Title"].strip() + ' ' + article["Summary"].strip()
        # get features vector
        dict_features[n_id] = create_features_vector(selected_words, article_words.split())
        
    return dict_features

# To calculate the conditional probability of 'word' by 'topic'
def get_topic_probability(words_topic_dictionary, selected_words, M, B, features, topic):
    probability = 0
    for index,word in enumerate(selected_words):
        if features[index]: # A = nº of news from 'topic' where 'word' appears
            if word in words_topic_dictionary[topic].keys():
                A = words_topic_dictionary[topic][word]["n_news"] 
            else:
                A = 0
        else: # A = nº of news from 'topic' where 'word' does NOT appear
            if word in words_topic_dictionary[topic].keys():
                A = B - words_topic_dictionary[topic][word]["n_news"]
            else:
                A = B
        probability += mt.log(float(A+1)/(B+M))
    
    return probability

# To get the topic with highest probability using Naïve-Bayes model
def get_naive_bayes_topic(news_per_topic, words_topic_dictionary, selected_words, features):
    M = len(news_per_topic) # nº total of topics
    prob_max = -float('inf') # highest probability found
    result_topic = '' # topic linked to the highest probability found (prob_max)
    ties = []
    
    for topic in words_topic_dictionary.keys():
        B = news_per_topic[topic] # nº total of news from 'topic'
        prob_topic = get_topic_probability(words_topic_dictionary, selected_words, M, B, features, topic)
        
        # to update highest probability and linked topic if necessary
        if prob_topic > prob_max:
            prob_max, result_topic = prob_topic, topic
            ties = []
        elif prob_topic == prob_max:
            ties.append(topic)
    
    # if more than one topic is linked to the highest probability, let's take one of them randomly
    if len(ties) > 0:
        result_topic = rnd.choice(ties)
    
    return result_topic