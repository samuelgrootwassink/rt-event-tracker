import nltk, re
from nltk.corpus import stopwords
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem import WordNetLemmatizer
nltk.data.path.append('../NLTK_DATA')
# nltk.download(['stopwords', 
#                'vader_lexicon', 
#                'punkt', 
#                'averaged_perceptron_tagger',
#                'maxent_ne_chunker', 
#                'words',
#                 'wordnet'], 
#               download_dir='../NLTK_DATA')


class NER():
    
    
    def __init__(self):
        
        self.__english_stopwords = set(stopwords.words('english'))
        
        
    def clean_sentence(self, sentence:list):
        """
        Tries to remove all stopwords with the help of the nltk.corpus stopwords.

        Args:
            text (str): Text from which stopwords need to be removed

        Returns:
            str: The stripped string 
        """
        if isinstance(sentence, str) is False:
            raise TypeError
        
        tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+")
        lemmatizer = WordNetLemmatizer()
        tokenized_sentence = tokenizer.tokenize(sentence)
        english_stopwords = self.__english_stopwords
        token_list = []
        for token in tokenized_sentence:
            if token.lower() in english_stopwords:
                continue
            token = lemmatizer.lemmatize(token)
            token_list.append(token)
            
        return token_list          


    def common_entity_sets(self, named_entities:list):

        common_entities_dict = {named_entity_set : 0 for named_entity_set in named_entities}
        
        for nes in common_entities_dict:
            if not nes or len(nes) <= 1:
                continue
            for ne in named_entities:
                if nes == ne :
                    common_entities_dict[nes] += 1
                elif max(len(ne.intersection(nes)), 1) / len(nes) >= 0.7:
                    common_entities_dict[nes] += 0.5
        
        return common_entities_dict

    
    def named_entities(self, sentences:str):
        """
        Uses NLTK Part of Speech tagging and chunking to determine Named Entities in a string for further use.

        Args:
            string (str): The string to take a apart

        Returns:
            set: A set containing all recognized named entities
        """
        
        sentence_list = sent_tokenize(sentences)
        cleaned_sents = list(self.clean_sentence(sent) for sent in sentence_list)
        tagged_sentence_list =  pos_tag_sents(cleaned_sents)
        ne_set = set()
        for sent in tagged_sentence_list:
            tree = nltk.ne_chunk(sent, binary=False)
            for ne in tree.subtrees(filter= lambda ne: ne.label() in {'PERSON','ORGANIZATION', 'GSP', 'GPE'}):
                named_entity = ' '.join([word[0] for word in ne])
                ne_set.add(named_entity)

        return frozenset(ne_set)
    
    