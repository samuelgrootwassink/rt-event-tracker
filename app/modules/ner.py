import nltk, re
from nltk.corpus import stopwords
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.data.path.append('../NLTK_DATA')
# nltk.download(['stopwords', 
#                'vader_lexicon', 
#                'punkt', 
#                'averaged_perceptron_tagger',
#                'maxent_ne_chunker', 
#                'words'], 
#               download_dir='../NLTK_DATA')


class NER():
    
    
    def __init__(self):
        
        self.__english_stopwords = set(stopwords.words('english'))
        
        
    def remove_stopwords(self, sentence:str):
        """
        Tries to remove all stopwords with the help of the nltk.corpus stopwords.

        Args:
            text (str): Text from which stopwords need to be removed

        Returns:
            str: The stripped string 
        """
        if isinstance(sentence, str) is False:
            raise TypeError
        
        english_stopwords = self.__english_stopwords
        word_list = []
        tokenized_sentence =  word_tokenize(sentence)
        for word in tokenized_sentence:
            if word.lower() in english_stopwords:
                continue
            word_list.append(word)
 
        return ' '.join(word_list)            

    def common_entity_sets(self, named_entities, amount: int = 10):
        # Working on this part, getting the common ne sets 
        ne_dict = {entity:0 for entity in named_entities}
        for entity in named_entities:
            ne_dict[entity] = ne_dict.get(entity, 0) + 1
        
        common_entities = sorted(ne_dict, key = lambda key: ne_dict.get(key), reverse=True)
        
        return common_entities[:amount]
    
    def named_entities(self, sentences:str):
        """
        Uses NLTK Part of Speech tagging and chunking to determine Named Entities in a string for further use.

        Args:
            string (str): The string to take a apart

        Returns:
            set: A set containing all recognized named entities
        """
        
        sentence_list = sent_tokenize(sentences)
        cleaned_sentences = [ self.remove_stopwords(sentence) for sentence in sentence_list]
        tokenized_sentence_list = [word_tokenize(sent) for sent in cleaned_sentences]
        tagged_sentence_list =  pos_tag_sents(tokenized_sentence_list)

        ne_set = set()
        for sent in tagged_sentence_list:
            tree = nltk.ne_chunk(sent, binary=True)
            for ne in tree.subtrees(filter= lambda ne: ne.label() == 'NE'):
                named_entity = ' '.join([word[0] for word in ne])
                ne_set.add(named_entity)

        return ne_set