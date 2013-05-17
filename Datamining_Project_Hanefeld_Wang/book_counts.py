from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re

FIND_YEAR = re.compile('\d\d\d\d')
class Bookcounts(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    
    #Map 1

        
    def extract_year(self, pub_date):

        year = FIND_YEAR.findall(pub_date)
        if year:
            return int(year[0])
        else:
            return None



    def get_years(self, _, record):
        if 'title' in record.keys():
            year = self.extract_year(record['pub_date'])
            yield [year, 1]
        
    #Red 1
 
    def count_years(self, year, counts):
 
        yield [year, sum(counts)]
    
    
    def steps(self):
        return [ self.mr(mapper=self.get_years,
                 reducer=self.count_years)]

if __name__ == '__main__':
    Bookcounts.run()
