from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
WORD_RE = re.compile(r"[\w]+")
STOP_WORDS = set("a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(','))
MIN_N = 1
MAX_N = 3
MIN_COUNT = 10
class NGrams(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    
    
    #Map 1
    def extract_ngrams(self, _, record):
        
        if 'title' in record.keys() and record['type'] == 'book' and record['lang'] == 'English':
            title = record['title'] 
            year = record['pub_date'][:4]
            words =  WORD_RE.findall(str(title))
            words = map(str.lower, words)
            n = len(words)
            for i in xrange(n):
                for j in xrange(i+MIN_N, min(n, i+MAX_N)+1):
                    ngram = words[i:j]
                    #Check for pure stopword ngrams
                    stopwords = set(ngram) <= STOP_WORDS
                    if not stopwords:
                        yield [(ngram,year), 1]
                
    #Red 1
    def count_ngrams(self, ngram_year, counts):
        yield [ngram_year, sum(counts)]
        
    
    def steps(self):
               return [ self.mr(mapper=self.extract_ngrams,
                        reducer=self.count_ngrams)]


if __name__ == '__main__':
    NGrams.run()