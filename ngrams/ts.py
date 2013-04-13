from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
from nltk.corpus import stopwords
WORD_RE = re.compile(r"[\w]+")
STOP_WORDS = set("a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(','))
MIN_N = 1
MAX_N = 3
MIN_COUNT = 10
WORDS_RE = re.compile(r'[\w]+', re.UNICODE)
FIND_YEAR = re.compile('\d\d\d\d')
class NGrams(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    
    
    #Map 1

        
    def extract_year(self, pub_date):

        year = FIND_YEAR.findall(pub_date)
        if year:
            return int(year[0])
        else:
            return None



    def create_wordlist(self, title):
    
        words = WORDS_RE.findall(title[0])
        words = map(unicode, words)
        words = map(unicode.lower, words)
        words = list(set(words) - set(stopwords.words('english')))
        return words

    def extract_ngrams(self, _, record):
        if 'title' in record.keys():
            words = self.create_wordlist(record['title'])
            year = self.extract_year(record['pub_date'])
            for word in words:
                yield [(word, year), 1]
                
    #Red 1
    def count_ngrams(self, ngram_year, counts):
 
        yield [ngram_year, sum(counts)]
    
    def group_by_word(self, ngram_year, count):
        word, year = ngram_year
        yield [word, (year, count)]
    
    def create_ts(self, word, year_counts):
        total = 0
        timeseries = []
        for year, count in year_counts:
            total += count
            timeseries.append("{year: "+str(year)+'", "count": "'+str(count)+'"}')
            
            yield ['{"word": "'+word+'", "total": "'+str(total)+'", "mean": "'+str(float(total)/len(timeseries))+'", "ts": {'+str(timeseries)+'}', None]
               
    
    def steps(self):
               return [ self.mr(mapper=self.extract_ngrams, reducer=self.count_ngrams),
                        self.mr(mapper=self.group_by_word,  reducer=self.create_ts)]


if __name__ == '__main__':
    NGrams.run()
