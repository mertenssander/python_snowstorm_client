# Maintainer: https://github.com/mertenssander/
# v0.1-alpha
# Python 3.7, built-in requirements: urllib, json, pickle
# Tested with Snowstorm 4.1.0 (https://github.com/IHTSDO/snowstorm)

from urllib.request import urlopen, Request
from urllib.parse import quote, quote_plus
import json
import pickle

# Todo
# add descriptions for conceptid to cacheB and return these
# add refset to cache_mapmembers and return it
# picke cache write / load

# Examples https://github.com/IHTSDO/SNOMED-in-5-minutes/blob/master/python3-examples/examples.py#L11

'''
# Use of this class:

# Initialize the object:
# Provide the base URL without trailing forw-slash, and provide the desired default branch and language.
snowstorm = Snowstorm(baseUrl="http://domain.com:8080", defaultBranchPath="MAIN", preferredLanguage="nl")
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
                 baseUrl="http://domain.com:8080",
                 defaultBranchPath="MAIN",
                 preferredLanguage="nl",
                 debug=False):
        self.baseUrl = baseUrl
        self.defaultBranchPath = defaultBranchPath
        self.ecl = ""
        self.searchTerm = ""
        self.id = ""
        self.cache_concepts = {}    # Concepts (cache_concepts)
        self.cache_descendants = {}    # Descendants (cache_descendants)
        self.cache_children = {}    # Children (cache_children)
        self.cache_parents = {}    # Parents (cache_parents)
        self.cache_mapmembers = {}    # MapMembers (cache_mapmembers)
        self.cacheTemp = {}
        self.debug = debug
        self.queryCount = 0
        self.activeFilter = "True"
        self.preferredLanguage = preferredLanguage
        self.referencedComponentId = ""
        self.targetComponent = ""
        self.mapTarget = ""

        # Test network connection to baseUrl with defaultBranchPath
        if self.debug:
            try:
                url = "{}/{}/concepts/{}".format(self.baseUrl,
                                                 self.defaultBranchPath, "87717000")
                req = Request(url)
                req.add_header('Accept-Language', self.preferredLanguage)
                urlopen(req).read()
                print("DEBUG [testConnection]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]\n\t [Success]".format(
                    "87717000", self.defaultBranchPath, self.baseUrl
                ))
            except Exception as e:
                print("DEBUG [testConnection]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]\n\t [Failed]: {}".format(
                    "87717000", self.defaultBranchPath, self.baseUrl, e
                ))
                exit()

    def loadCache(self):
        try:
            pickle_in = open("cache_concepts.pickle", "rb")
            self.cache_concepts = pickle.load(pickle_in)
            if self.debug:
                print("DEBUG [loadCache]: concepts cache read")
        except Exception as e:
            if self.debug:
                print("DEBUG [loadCache]: concepts cache read error: ", e)

        try:
            pickle_in = open("cache_descendants.pickle", "rb")
            self.cache_descendants = pickle.load(pickle_in)
            if self.debug:
                print("DEBUG [loadCache]: cache descendants read")
        except Exception as e:
            if self.debug:
                print("DEBUG [loadCache]: cache descendants read error: ", e)

        try:
            pickle_in = open("cache_children.pickle", "rb")
            self.cache_children = pickle.load(pickle_in)
            if self.debug:
                print("DEBUG [loadCache]: cache children read")
        except Exception as e:
            if self.debug:
                print("DEBUG [loadCache]: cache children read error: ", e)

        try:
            pickle_in = open("cache_parents.pickle", "rb")
            self.cache_parents = pickle.load(pickle_in)
            if self.debug:
                print("DEBUG [loadCache]: cache parents read")
        except Exception as e:
            if self.debug:
                print("DEBUG [loadCache]: cache parents read error: ", e)

        try:
            pickle_in = open("cache_mapmembers.pickle", "rb")
            self.cache_mapmembers = pickle.load(pickle_in)
            if self.debug:
                print("DEBUG [loadCache]: cache mapmembers read")
        except Exception as e:
            if self.debug:
                print("DEBUG [loadCache]: cache mapmembers read error: ", e)

    def writeCache(self):
        # concepts cache
        try:
            pickle_in = open("cache_concepts.pickle", "rb")
            cache_concepts_loaded = pickle.load(pickle_in)
            self.cache_concepts = {
                **cache_concepts_loaded, **self.cache_concepts}
            if self.debug:
                print("DEBUG [writeCache]: concepts cache read")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: concepts cache read error: ", e)
        try:
            pickle_out = open("cache_concepts.pickle", "wb")
            pickle.dump(self.cache_concepts, pickle_out)
            pickle_out.close()
            if self.debug:
                print("DEBUG [writeCache]: concepts cache written")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: concepts cache write error: ", e)

        # cache descendants
        try:
            pickle_in = open("cache_descendants.pickle", "rb")
            cache_descendants_loaded = pickle.load(pickle_in)
            self.cache_descendants = {
                **cache_descendants_loaded, **self.cache_descendants}
            if self.debug:
                print("DEBUG [writeCache]: cache descendants read")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache descendants read error: ", e)
        try:
            pickle_out = open("cache_descendants.pickle", "wb")
            pickle.dump(self.cache_descendants, pickle_out)
            pickle_out.close()
            if self.debug:
                print("DEBUG [writeCache]: cache descendants written")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache descendants write error: ", e)

        # cache children
        try:
            pickle_in = open("cache_children.pickle", "rb")
            cache_children_loaded = pickle.load(pickle_in)
            self.cache_children = {
                **cache_children_loaded, **self.cache_children}
            if self.debug:
                print("DEBUG [writeCache]: cache children read")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache children read error: ", e)
        try:
            pickle_out = open("cache_children.pickle", "wb")
            pickle.dump(self.cache_children, pickle_out)
            pickle_out.close()
            if self.debug:
                print("DEBUG [writeCache]: cache children written")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache children write error: ", e)

        # cache parents
        try:
            pickle_in = open("cache_parents.pickle", "rb")
            cache_parents_loaded = pickle.load(pickle_in)
            self.cache_parents = {**cache_parents_loaded, **self.cache_parents}
            if self.debug:
                print("DEBUG [writeCache]: cache parents read")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache parents read error: ", e)
        try:
            pickle_out = open("cache_parents.pickle", "wb")
            pickle.dump(self.cache_parents, pickle_out)
            pickle_out.close()
            if self.debug:
                print("DEBUG [writeCache]: cache parents written")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache parents write error: ", e)

        # cache mapmembers
        try:
            pickle_in = open("cache_mapmembers.pickle", "rb")
            cache_mapmembers_loaded = pickle.load(pickle_in)
            self.cache_mapmembers = {
                **cache_mapmembers_loaded, **self.cache_mapmembers}
            if self.debug:
                print("DEBUG [writeCache]: cache mapmembers read")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache mapmembers read error: ", e)
        try:
            pickle_out = open("cache_mapmembers.pickle", "wb")
            pickle.dump(self.cache_mapmembers, pickle_out)
            pickle_out.close()
            if self.debug:
                print("DEBUG [writeCache]: cache mapmembers written")
        except Exception as e:
            if self.debug:
                print("DEBUG [writeCache]: cache mapmembers read error: ", e)

    def getConceptById(self, id):
        # If concept present in cache, do not request
        if id in self.cache_concepts:
            if self.debug:
                print("DEBUG [getConceptId]: Cache \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
        # If concept not present in cache, request it and add it to cache
        else:
            if self.debug:
                print("DEBUG [getConceptId]: Request \t[ID = {}] \t[BRANCH = {}] \t[SERVER = {}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
            url = "{}/{}/concepts/{}".format(self.baseUrl,
                                             self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()

            self.cache_concepts.update({
                str(id): json.loads(response.decode('utf-8'))
            })
            self.queryCount += 1

        # Clean all relevant self.variables used in this function
        output = self.cache_concepts[id]
        id = ""
        # Return requested ID from cache
        return output

    def findConcepts(self, searchTerm="", ecl=""):
        if self.debug:
            print("DEBUG [findConcepts]: Request \t[TERM={}] \t[ECL={}] \t[ACTIVEFILTER={}] \t[BRANCH={}] \t[SERVER={}]".format(
                searchTerm, ecl, self.activeFilter, self.defaultBranchPath, self.baseUrl))
        # Send request
        try:
            counter = 0
            url = "{}/{}/concepts?activeFilter={}&limit=10000&term={}&ecl={}".format(
                self.baseUrl, self.defaultBranchPath, self.activeFilter, quote(searchTerm), quote_plus(ecl))
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
                if items['total'] == 0:
                    break

                # For all results, add to cache
                for value in items['items']:
                    self.cacheTemp.update({value['conceptId']: value})
                    counter += 1

                # If there are more results than currently present in cacheTemp, run another query
                if counter < total_results:
                    # Request results
                    url = "{}/{}/concepts?activeFilter={}&limit=10000&term={}&searchAfter={}&ecl={}".format(
                        self.baseUrl, self.defaultBranchPath, self.activeFilter, quote_plus(
                            searchTerm), quote_plus(items.get('searchAfter')), quote_plus(ecl)
                    )
                    req = Request(url)
                    req.add_header('Accept-Language', self.preferredLanguage)
                    response = urlopen(req).read()
                    items = json.loads(response.decode('utf-8'))
                    # Update query count
                    self.queryCount += 1
                if self.debug:
                    print("DEBUG [findConcepts]: Lenght of cacheTemp: {} of {} total results".format(
                        len(self.cacheTemp), total_results))

            # Store temp cache in local dictionary for return
            results = self.cacheTemp

            # Add results to the concepts cache (cache_concepts)
            for index, value in results.items():
                self.cache_concepts.update({
                    str(index): value
                })
        except Exception as e:
            print(type(e))
            print(e)
            exit()

        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return results

    def getDescendants(self, id):
        if id in self.cache_descendants:
            if self.debug:
                print("DEBUG [getDescendants]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
        else:
            if self.debug:
                print("DEBUG [getDescendants]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
            # Send request
            url = "{}/{}/concepts/{}/descendants?stated=false&limit=10000".format(
                self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))

            # Update query count
            self.queryCount += 1

            # Error and exit when the result is larger than the query limit.
            if len(items['items']) > 10000:
                print(
                    "ERROR [getDescendants]: total results exceeds the query limit. Descendants endpoint has no 'searchAfter' compatibility. Use ECL query instead.")

            # Store temp cache in local dictionary for return
            results = items['items']

            # Add results to the descendants list (cache_descendants)
            descendants_list = {}
            for index in results:
                descendants_list.update({index['conceptId']: index})
            self.cache_descendants.update({id: descendants_list})

            # Add results to the concepts cache (cache_concepts)
            for value in results:
                self.cache_concepts.update({
                    str(value['conceptId']): value
                })

        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cache_descendants[id]

    def getChildren(self, id):
        if id in self.cache_children:
            if self.debug:
                print("DEBUG [getChildren]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
        else:
            if self.debug:
                print("DEBUG [getChildren]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
            # Send request
            url = "{}/browser/{}/concepts/{}/children?form=inferred".format(
                self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))
            # Update query count
            self.queryCount += 1

            # Store temp cache in local dictionary for return
            results = items

            # Add results to the children list (cache_children)
            children_list = {}
            for index in results:
                children_list.update({index['conceptId']: index})
            self.cache_children.update({id: children_list})

            # Add results to the concepts cache (cache_concepts)
            for value in results:
                self.cache_concepts.update({str(value['conceptId']): value})
        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cache_children[id]

    def getParents(self, id):
        if id in self.cache_parents:
            if self.debug:
                print("DEBUG [getParents]: Cache \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
        else:
            if self.debug:
                print("DEBUG [getParents]: Request \t[ID={}] \t[BRANCH={}] \t[SERVER={}]".format(
                    id, self.defaultBranchPath, self.baseUrl))
            # Send request
            url = "{}/browser/{}/concepts/{}/parents?form=inferred".format(
                self.baseUrl, self.defaultBranchPath, id)
            req = Request(url)
            req.add_header('Accept-Language', self.preferredLanguage)
            response = urlopen(req).read()
            items = json.loads(response.decode('utf-8'))
            # Update query count
            self.queryCount += 1

            # Store temp cache in local dictionary for return
            results = items

            # Add results to the parents list (cache_parents)
            parents_list = {}
            for index in results:
                parents_list.update({index['conceptId']: index})
            self.cache_parents.update({id: parents_list})

            # Add results to the concepts cache (cache_concepts)
            for value in results:
                self.cache_concepts.update({str(value['conceptId']): value})
        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cache_parents[id]

    def getMapMembers(self, id="", referencedComponentId="", targetComponent="", mapTarget=""):
        if self.debug:
            print("DEBUG [getMapMembers]: Request \t[ID={}] \t[REFCOMP={}] \t[TARGETCOMP={}] \t[MAPTARG={}] \t[ACTIVE={}] \t[BRANCH={}] \t[SERVER={}]".format(
                id, referencedComponentId, targetComponent, mapTarget, self.activeFilter, self.defaultBranchPath, self.baseUrl))
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

        # Add results to the member list (cache_mapmembers)
        member_list = {}
        for index in results:
            member_list.update({index['referencedComponentId']: index})
        self.cache_mapmembers.update({id: member_list})

        # Add results to the concepts cache (cache_concepts)
        for value in results:
            self.cache_concepts.update({
                str(value['referencedComponent']['conceptId']): value['referencedComponent']
            })

        # Clean all relevant self.variables used in this function
        self.cacheTemp = {}
        return self.cache_mapmembers[id]

    def printStatistics(self):
        print("Number of queries: ", self.queryCount)
        print("Number of items in cache_concepts: ", len(self.cache_concepts))
        print("Number of items in cache_descendants: ",
              len(self.cache_descendants))
        print("Number of items in cache_children: ", len(self.cache_children))
        print("Number of items in cache_parents: ", len(self.cache_parents))
        print("Number of items in cache_mapmembers: ",
              len(self.cache_mapmembers))

        print("Number of items in CacheTemp (should be 0): ", len(self.cacheTemp))


if __name__ == "__main__":
    snowstorm = Snowstorm(debug=True)
    snowstorm.activeFilter = "True"
    snowstorm.loadCache()
    print(len(snowstorm.getConceptById(id="74400008")), "<- Should be 8")

    # Fill concept cache
    # print(len(snowstorm.findConcepts(ecl="<<138875005")), "<- Should be 356350")

    print(len(snowstorm.findConcepts(
        searchTerm="test device", ecl="<63653004")), "<- Should be 8")
    print(len(snowstorm.getDescendants(id="74400008")), "<- Should be 32")
    print(len(snowstorm.getChildren(id="74400008")), "<- Should be 15")
    print(len(snowstorm.getParents(id="74400008")), "<- Should be 2")
    print(len(snowstorm.getMapMembers(id="", referencedComponentId="",
                                      targetComponent="", mapTarget="P11.5")), "<- Should be 8")
    snowstorm.printStatistics()
    snowstorm.writeCache()