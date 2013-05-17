from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
#Stopwords from nltk.corpus.stopwords('english')
STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

WORDS_RE = re.compile(r'[\w]+', re.UNICODE)
FIND_YEAR = re.compile('\d\d\d\d')
class WordTS(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol


    
    
    #Map 1

        
    def extract_year(self, pub_date):

        year = FIND_YEAR.findall(pub_date)
        if year:
            return int(year[0])
        else:
            return 9999



    def create_wordlist(self, title):
    
        words = WORDS_RE.findall(title[0])
        words = map(unicode, words)
        words = map(unicode.lower, words)
        words = list(set(words) - STOPWORDS)
        return words
    
    def extract_1grams(self, _, record):
        if 'title' in record.keys():
            words = self.create_wordlist(record['title'])
            year = self.extract_year(record['pub_date'])
            for word in words:
                yield [(word, year), 1]
        
    #Red 1
 
    def count_1grams(self, ngram_year, counts):
 
        yield [ngram_year, sum(counts)]
    
    def group_by_word(self, ngram_year, count):
        word, year = ngram_year
        yield [word, (year, count)]
    
    def create_ts(self, word, year_counts):
        total = 0
        maximum = 0
        num_years = 0
        timeseries = []
        ts_string = ''
        for year, count in year_counts:
            maximum = max(maximum, count)
            total += count
            num_years += 1
            timeseries.append((year, count))

        yield [word, [maximum, total, num_years, timeseries]]

    
    def steps(self):
        return [ self.mr(mapper=self.extract_1grams,
                 reducer=self.count_1grams),
                 self.mr(mapper=self.group_by_word,
                         reducer=self.create_ts)]


if __name__ == '__main__':
    WordTS.run()
