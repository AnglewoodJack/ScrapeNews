import pickle

import nltk
from deeppavlov import configs, build_model
import pandas as pd
from tqdm import tqdm

# nltk.download('punkt')


def ner_rec(dataframe):
    """

    :param dataframe:
    :return:
    """
    # build model
    ner_model = build_model(configs.ner.ner_ontonotes_bert_mult)
    # make empty list to hold all results
    res_all = []
    # iterate over each news text
    for text in tqdm(dataframe['text'], desc='entity recognition'):
        # make empty list to hold results for  each text
        res_text = []
        # iterate over each sentence in text
        for sentence in text:
            # find entities
            res = ner_model([sentence])
            # concat results with text into list of tuples
            tokenized_text = res[0][0]
            tokenized_entity = res[1][0]
            res_list = list(zip(tokenized_text, tokenized_entity))
            # add to text
            res_text += res_list
        # add processed txt to overall results
        res_all.append(res_text)

    return res_all


dataset = pd.read_csv('search_res.csv', index_col=0)

dataset = dataset.iloc[3:, :]
dataset.loc[:,'text'] = dataset.loc[:,'text'].replace('\n', ' ', regex=True)
dataset.loc[:,'text'] = dataset.loc[:,'text'].replace('\t', ' ', regex=True)
dataset = dataset.dropna(subset=['text'])


def token(row):
    return nltk.tokenize.sent_tokenize(row['text'])


dataset['text'] = dataset.apply(token, axis=1)

ner_res = ner_rec(dataset)

with open('ner_results.pickle', 'wb') as file:
    pickle.dump(ner_res, file)
