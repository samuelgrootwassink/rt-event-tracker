import nltk, re
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag

nltk.data.path.append('../NLTK_DATA')
nltk.download(['stopwords', 
               'vader_lexicon', 
               'punkt', 
               'averaged_perceptron_tagger',
               'maxent_ne_chunker', 
               'words'], 
              download_dir='../NLTK_DATA')


class NER():
    
    def _remove_stopwords(self, string:str):
        """
        Tries to remove all stopwords with the help of the nltk.corpus stopwords.

        Args:
            text (str): Text from which stopwords need to be removed

        Returns:
            str: The stripped string 
        """
        if isinstance(string, str) is False:
            raise TypeError
        
        english_stopwords = set(stopwords.words('english'))
        word_list = []
        tokenized_string =  word_tokenize(string)
        for word in tokenized_string:
            if word.lower() in english_stopwords:
                continue
            word_list.append(word)
        stripped_text = ' '.join(word_list)
        return stripped_text            

    
    def named_entities(self, string:str):
        """
        Uses NLTK Part of Speech tagging and chunking to determine Named Entities in a string for further use.

        Args:
            string (str): The string to take a apart

        Returns:
            set: A set containing all recognized named entities
        """
        tokenized_string = word_tokenize(string)
        tagged_string =  pos_tag(tokenized_string)
        ne_tree = nltk.ne_chunk(tagged_string, binary=True)
        named_entities = set()
        
        for ne in ne_tree.subtrees(filter= lambda ne: ne.label() == 'NE'):
            named_entity = ' '.join([word[0] for word in ne])
            named_entities.add(named_entity)

        return named_entities

# text = "NASA awarded Elon Musk’s SpaceX a $2.9 billion contract to build the lunar lander."
# tokens = word_tokenize(text)
# tag=pos_tag(tokens)
# print(tag)

# ne_tree = nltk.ne_chunk(tag)
# print(ne_tree)