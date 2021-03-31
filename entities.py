import pickle

with open('ner_results.pickle', 'rb') as handle:
    b = pickle.load(handle)

# print()

for text in b:
    for sent in text:
        if sent[1].endswith('ORG'):
            print(sent[0])
