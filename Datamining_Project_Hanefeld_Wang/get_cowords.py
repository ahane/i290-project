from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
WORD_RE = re.compile(r"[\w]+")
STOP_WORDS = set("a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(','))

QWORDS = {u'abraham': 1865,
 u'bulletin': 1975,
 u'centennial': 1876,
 u'defense': 1941,
 u'grant': 1868,
 u'inclosing': 1994,
 u'interior': 1887,
 u'intervention': 1852,
 u'lincoln': 1865,
 u'nebraska': 1854,
 u'post': 1944,
 u'prices': 1919,
 u'quarterly': 1975,
 u'roosevelt': 1919,
 u'sixteenth': 1943,
 u'spain': 1937,
 u'turkey': 1854,
 u'union': 1861,
 u'victory': 1942}

class Cowords(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    
    
    #Map 1
    def extract_cowords(self, _, record):
        
        if 'title' in record.keys() and record['type'] == 'book' and record['lang'] == 'English':
            title = record['title'] 
            year = record['pub_date'][:4]
            words =  WORD_RE.findall(str(title))
            words = set(map(str.lower, words))
            words = words.difference(STOP_WORDS)
            try:
                year = int(year)
            except:
                year = 0
            for word in words:
                if word in QWORDS.keys() and year == QWORDS[word]:
                    for commonword in words:
                        if word != commonword:
                            yield [word, commonword]
                
    
    #Red 1
    def count_cowords(self, word, commonwords):
        c = {}
        for cword in commonwords:
            if cword in c.keys():
                c[cword] +=1
            else:
                c[cword] = 1
        counttuples = c.items()
        yield [word, counttuples]
        

    def steps(self):
               return [ self.mr(mapper=self.extract_cowords,
                                reducer=self.count_cowords)]
#                        self.mr(mapper=self.filter_by_count,
#                                reducer=self.identity_sort)]


if __name__ == '__main__':
    Cowords.run()
