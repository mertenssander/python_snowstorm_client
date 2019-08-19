# Maintainer: https://github.com/mertenssander/
# v0.1-alpha
# Python 3.7, built-in requirements: urllib, json, pickle
# Tested with Snowstorm 4.1.0 (https://github.com/IHTSDO/snowstorm)

from urllib.request import *
from urllib.parse import *
import json, pickle

# Todo
# add descriptions for conceptid to cacheB and return these
# add refset to cacheH and return it
# picke cache write / load

# Examples https://github.com/IHTSDO/SNOMED-in-5-minutes/blob/master/python3-examples/examples.py#L11

'''
# Use of this class:

# Initialize the object:
snowstorm = Snowstorm(baseUrl="http://termservice.test-nictiz.nl:8080", defaultBranchPath="MAIN")
                                        # Provide the base URL without trailing forw-slash, and provide the desired default branch
snowstorm.debug         = True      (Boolean), standard = False
snowstorm.activeFilter  = "True"    (String), standard = "True"
snowstorm.loadCache()
snowstorm.getConceptById(id="74400008")
snowstorm.findConcepts([searchterm="testing device"], [ecl="<74400008"])
snowstorm.getDescendants(id="74400008")
snowstorm.getChildren(id="74400008")
snowstorm.getParents(id="74400008")
snowstorm.getMapMembers([id="74400008"], [referencedComponentId="74400008"], [targetComponent="74400008"], [mapTarget="P11.5"])
snowstorm.printStatistics()
snowstorm.writeCache()

# Print statistics on number of queries and state of the cache:
snowstorm.printStatistics()             # Prints to terminal
'''


class Snowstorm():
    def __init__(self, 
            baseUrl="http://termservice.test-nictiz.nl:8080", 
            defaultBranchPath="MAIN", 
            preferredLanguage="nl",
            debug=False):
        self.baseUrl            = baseUrl
        self.defaultBranchPath  = defaultBranchPath
        self.ecl                = ""
        self.searchTerm         = ""
        self.id                 = ""
        self.cacheA             = {}
        self.cacheB             = {}
        self.cacheC             = {}
        self.cacheD             = {}
        self.cacheE             = {}
        self.cacheF             = {}
        self.cacheG             = {}
        self.cacheH             = {}
        self.cacheTemp          = {}
        self.debug              = debug
        self.queryCount         = 0
        self.activeFilter       = "True"
        self.preferredLanguage  = preferredLanguage
        self.referencedComponentId  = ""
        self.targetComponent    = ""
        self.mapTarget          = ""

        # Test network connection to baseUrl with defaultBranchPath
        if self.debug: 
            try:
                url = "{}/{}/concepts/{}".format(self.baseUrl, self.defaultBranchPath, "87717000")
                req = Request(url)
                req.add_header('Accept-Language', self.preferredLanguage)
                response = urlopen(req).read()
                print("DEBUG [testConnection]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]\n\t [Success]".format(
                    "87717000", self.defaultBranchPath, self.baseUrl
                    ))
            except Exception as e:
                print("DEBUG [testConnection]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]\n\t [Failed]: {}".format(
                    "87717000", self.defaultBranchPath, self.baseUrl, e
                    ))
                exit()


    def test(self, arg1):
        print(arg1)


    def loadCache(self):
        try:
            pickle_in = open("cacheA.pickle","rb")
            self.cacheA = pickle.load(pickle_in)
        except Exception as e:
            print(e)

        try:
            pickle_in = open("cacheB.pickle","rb")
            self.cacheB = pickle.load(pickle_in)
        except Exception as e:
            print(e)
        
        try:
            pickle_in = open("cacheC.pickle","rb")
            self.cacheC = pickle.load(pickle_in)
        except Exception as e:
            print(e)

        try:
            pickle_in = open("cacheD.pickle","rb")
            self.cacheD = pickle.load(pickle_in)
        except Exception as e:
            print(e)

        try:            
            pickle_in = open("cacheE.pickle","rb")
            self.cacheE = pickle.load(pickle_in)
        except Exception as e:
            print(e)
            
        try:
            pickle_in = open("cacheF.pickle","rb")
            self.cacheF = pickle.load(pickle_in)
        except Exception as e:
            print(e)
        
        try:
            pickle_in = open("cacheG.pickle","rb")
            self.cacheG = pickle.load(pickle_in)
        except Exception as e:
            print(e)
        
        try:
            pickle_in = open("cacheH.pickle","rb")
            self.cacheH = pickle.load(pickle_in)
        except Exception as e:
            print(e)


    def writeCache(self):
        # Cache A
        try:
            pickle_in = open("cacheA.pickle","rb")
            cacheA_loaded = pickle.load(pickle_in)
            self.cacheA = {**cacheA_loaded, **self.cacheA}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheA.pickle","wb")
            pickle.dump(self.cacheA, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)
            
        # Cache B
        try:
            pickle_in = open("cacheB.pickle","rb")
            cacheB_loaded = pickle.load(pickle_in)
            self.cacheB = {**cacheB_loaded, **self.cacheB}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheB.pickle","wb")
            pickle.dump(self.cacheB, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)

        # Cache C
        try:
            pickle_in = open("cacheC.pickle","rb")
            cacheC_loaded = pickle.load(pickle_in)
            self.cacheC = {**cacheC_loaded, **self.cacheC}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheC.pickle","wb")
            pickle.dump(self.cacheC, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)

        # Cache D
        try:
            pickle_in = open("cacheD.pickle","rb")
            cacheD_loaded = pickle.load(pickle_in)
            self.cacheD = {**cacheD_loaded, **self.cacheD}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheD.pickle","wb")
            pickle.dump(self.cacheD, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)

        # Cache E
        try:
            pickle_in = open("cacheE.pickle","rb")
            cacheE_loaded = pickle.load(pickle_in)
            self.cacheE = {**cacheE_loaded, **self.cacheE}
        except Exception as e:
            print(e)
        pickle_out = open("cacheE.pickle","wb")
        pickle.dump(self.cacheE, pickle_out)
        pickle_out.close()

        # Cache F
        try:
            pickle_in = open("cacheF.pickle","rb")
            cacheF_loaded = pickle.load(pickle_in)
            self.cacheF = {**cacheF_loaded, **self.cacheF}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheF.pickle","wb")
            pickle.dump(self.cacheF, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)
        
        # Cache G
        try:
            pickle_in = open("cacheG.pickle","rb")
            cacheG_loaded = pickle.load(pickle_in)
            self.cacheG = {**cacheG_loaded, **self.cacheG}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheG.pickle","wb")
            pickle.dump(self.cacheG, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)

        # Cache H
        try:        
            pickle_in = open("cacheH.pickle","rb")
            cacheH_loaded = pickle.load(pickle_in)
            self.cacheH = {**cacheH_loaded, **self.cacheH}
        except Exception as e:
            print(e)
        try:
            pickle_out = open("cacheH.pickle","wb")
            pickle.dump(self.cacheH, pickle_out)
            pickle_out.close()
        except Exception as e:
            print(e)


    def getConceptById(self, id):
        # If concept present in cache, do not request
        if id in self.cacheA:
            if self.debug: print("DEBUG [getConceptId]: Cache \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]".format(id, self.defaultBranchPath, self.baseUrl))
        # If concept not present in cache, request it and add it to cache
        else:
            if self.debug: print("DEBUG [getConceptId]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]".format(id, self.defaultBranchPath, self.baseUrl))
            url = "{}/{}/concepts/{}".format(self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()

            self.cacheA.update({
                str(id) : json.loads(response.decode('utf-8'))
                })
            self.queryCount += 1
        
        # Clean all relevant self.variables used in this function
        output = self.cacheA[id]
        id     = ""
        # Return requested ID from cache
        return output


    def findConcepts(self, searchTerm="", ecl=""):
        if self.debug: print("DEBUG [findConcepts]: Request \t[TERM={}] \t[ECL={}] \t[ACTIVEFILTER={}] \t[BRANCH={}] \t[SERVER={}]".format(searchTerm, ecl, self.activeFilter, self.defaultBranchPath, self.baseUrl))
        # Send request
        try:
            counter = 0
            url = "{}/{}/concepts?activeFilter={}&limit=10000&term={}&ecl={}".format(self.baseUrl, self.defaultBranchPath, self.activeFilter, quote(searchTerm), quote_plus(ecl))
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))

            total_results = items['total']
            # Update query count
            self.queryCount += 1

            # Loop while the cacheTemp is smaller than the total results
            while counter < total_results:
                # If no results, break while loop - Probably redundant
                if items['total'] == 0: break

                # For all results, add to cache
                for value in items['items']:
                    self.cacheTemp.update({value['conceptId'] : value})
                    counter += 1
                
                # If there are more results than currently present in cacheTemp, run another query
                if counter < total_results:
                    # Request results
                    url = "{}/{}/concepts?activeFilter={}&limit=10000&term={}&searchAfter={}&ecl={}".format(
                        self.baseUrl, self.defaultBranchPath, self.activeFilter, quote_plus(searchTerm), quote_plus(items.get('searchAfter')), quote_plus(ecl)
                        )        
                    req = Request(url)
                    req.add_header('Accept-Language', self.preferredLanguage)
                    response = urlopen(req).read()
                    items = json.loads(response.decode('utf-8'))
                    # Update query count
                    self.queryCount += 1
                if self.debug:  print("DEBUG [findConcepts]: Lenght of cacheTemp: {} of {} total results".format(len(self.cacheTemp), total_results))    

            # Store temp cache in local dictionary for return
            results = self.cacheTemp
            
            # Add results to the concepts cache (CacheA)
            for index, value in results.items():
                self.cacheA.update({
                    str(index) : value
                    })
        except Exception as e:
            print(type(e))
            print(e)
            exit()
                
        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return results


    def getDescendants(self, id):
        if id in self.cacheD:
            if self.debug: print("DEBUG [getDescendants]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(self.id, self.defaultBranchPath, self.baseUrl))
        else:
            if self.debug: print("DEBUG [getDescendants]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(self.id, self.defaultBranchPath, self.baseUrl))
            # Send request
            url = "{}/{}/concepts/{}/descendants?stated=false&limit=10000".format(self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))
            total_results = items['total']
            
            # Update query count
            self.queryCount += 1

            # Error and exit when the result is larger than the query limit.
            if len(items['items']) > 10000:   
                print("ERROR [getDescendants]: total results exceeds the query limit. Descendants endpoint has no 'searchAfter' compatibility. Use ECL query instead.")

            # Store temp cache in local dictionary for return
            results = items['items']
            
            # Add results to the descendants list (CacheD)
            descendants_list = {}
            for index in results:
                descendants_list.update({ index['conceptId'] : index })
            self.cacheD.update({id : descendants_list})

            # Add results to the concepts cache (CacheA)
            for value in results:
                self.cacheA.update({
                    str(value['conceptId']) : value
                    })

        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cacheD[id]


    def getChildren(self, id):
        if id in self.cacheF:
            if self.debug: print("DEBUG [getChildren]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(id, self.defaultBranchPath, self.baseUrl))
        else:
            if self.debug: print("DEBUG [getChildren]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(id, self.defaultBranchPath, self.baseUrl))
            # Send request
            url = "{}/browser/{}/concepts/{}/children?form=inferred".format(self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))        
            # Update query count
            self.queryCount += 1

            # Store temp cache in local dictionary for return
            results = items
            
            # Add results to the children list (cacheF)
            children_list = {}
            for index in results:
                children_list.update({ index['conceptId'] : index })
            self.cacheF.update({id : children_list})

            # Add results to the concepts cache (CacheA)
            for value in results:
                self.cacheA.update({str(value['conceptId']) : value})
        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cacheF[id]


    def getParents(self, id):
        if id in self.cacheG:
            if self.debug: print("DEBUG [getParents]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(id, self.defaultBranchPath, self.baseUrl))
        else:    
            if self.debug: print("DEBUG [getParents]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(id, self.defaultBranchPath, self.baseUrl))        
            # Send request
            url = "{}/browser/{}/concepts/{}/parents?form=inferred".format(self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))        
            # Update query count
            self.queryCount += 1

            # Store temp cache in local dictionary for return
            results = items
            
            # Add results to the parents list (cacheG)
            parents_list = {}
            for index in results:
                parents_list.update({ index['conceptId'] : index })
            self.cacheG.update({id : parents_list})

            # Add results to the concepts cache (CacheA)
            for value in results:
                self.cacheA.update({str(value['conceptId']) : value})
        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cacheG[id]


    def getMapMembers(self, id="", referencedComponentId="", targetComponent="", mapTarget=""):
        if self.debug: 
            print("DEBUG [getMapMembers]: Request \t[ID={}] \t[REFCOMP={}] \t[TARGETCOMP={}] \t[MAPTARG={}] \t[ACTIVE={}] \t[BRANCH={}] \t[SERVER={}]".format(id, referencedComponentId, targetComponent, mapTarget, self.activeFilter, self.defaultBranchPath, self.baseUrl))
        # Send request
        url = "{}/{}/members?limit=10000&referenceset={}&referencedComponentId={}&active={}&targetComponent={}&mapTarget={}".format(
            self.baseUrl, self.defaultBranchPath, id, referencedComponentId, self.activeFilter, targetComponent, mapTarget
            )
        req = Request(url)
        req.add_header('Accept-Language', self.preferredLanguage)
        response = urlopen(req).read()
        items = json.loads(response.decode('utf-8'))
        # Update query count
        self.queryCount += 1

        # Error and exit when the result is larger than the query limit.
        if len(items['items']) > 10000:   
            print("ERROR [getDescendants]: total results exceeds the query limit. Descendants endpoint has no 'searchAfter' compatibility. Use ECL query instead.")

        # Store temp cache in local dictionary for return
        results = items['items']
        
        # Add results to the member list (cacheH)
        member_list = {}
        for index in results:
            member_list.update({ index['referencedComponentId'] : index })
        self.cacheH.update({id : member_list})

        # Add results to the concepts cache (CacheA)
        for value in results:
            self.cacheA.update({
                str(value['referencedComponent']['conceptId']) : value['referencedComponent']
                })

        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cacheH[id]


    def printStatistics(self):
        print("Number of queries: ", self.queryCount)
        print("Number of items in CacheA: ",len(self.cacheA))
        print("Number of items in CacheB: ",len(self.cacheB))
        print("Number of items in CacheC: ",len(self.cacheC))
        print("Number of items in CacheD: ",len(self.cacheD))
        print("Number of items in CacheE: ",len(self.cacheE))
        print("Number of items in CacheF: ",len(self.cacheF))
        print("Number of items in CacheG: ",len(self.cacheG))
        print("Number of items in CacheH: ",len(self.cacheH))
        
        print("Number of items in CacheTemp (should be 0): ",len(self.cacheTemp))

if __name__ == "__main__":
    snowstorm = Snowstorm(
        baseUrl="http://termservice.test-nictiz.nl:8080", 
        defaultBranchPath="MAIN", 
        debug=True)
    snowstorm.activeFilter  = "True"
    snowstorm.loadCache()
    print(len(snowstorm.getConceptById(id="74400008")), "<- Should be 8")

    # Fill concept cache
    # print(len(snowstorm.findConcepts(ecl="<<138875005")), "<- Should be 356350")

    print(len(snowstorm.findConcepts(searchTerm="test device", ecl="<63653004")), "<- Should be 8")
    print(len(snowstorm.getDescendants(id="74400008")), "<- Should be 32")
    print(len(snowstorm.getChildren(id="74400008")), "<- Should be 15")
    print(len(snowstorm.getParents(id="74400008")), "<- Should be 2")
    print(len(snowstorm.getMapMembers(id="", referencedComponentId="", targetComponent="", mapTarget="P11.5")), "<- Should be 8")
    snowstorm.printStatistics()
    snowstorm.writeCache()