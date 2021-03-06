from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
WORD_RE = re.compile(r"[\w]+")
STOP_WORDS = set("a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,the,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,the,would,yet,you,your".split(','))
class WordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    
    
    #Map 1
    def extract_words(self, _, record):
        
        if 'title' in record.keys() and record['type'] == 'book' and record['lang'] == 'English':
            title = record['title'] 
            for word in WORD_RE.findall(str(title)):
                if word not in STOP_WORDS:
 
                    yield [word.lower(), 1]
    #Red 1
    def count_words(self, word, counts):
        yield [word, sum(counts)]
        

    
    def steps(self):
               return [ self.mr(mapper=self.extract_words,
                        reducer=self.count_words)]


if __name__ == '__main__':
    WordCount.run()
