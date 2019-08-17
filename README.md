# python_snowstorm_client > Version 0.1-alpha
Python client for use with the IHTSDO Snowstorm Terminology server

## Supported functions
- write and load to pickled cache files (loadCache / writeCache)
- get concept by ID (getConceptById)
- search for concepts by ECL or term (findConcepts)
- find children (getChildren) and descendants (getDescendants)
- find parents (getParents) - no function for ancestors as of yet
- get members from map (getMapMembers) by mapID, referenced-/targetcomponent or maptarget
- print out statistics of the cache dictionaries and number of performed queries to the server

## Use:
>snowstorm = Snowstorm(baseUrl="http://server.com:8080", defaultBranchPath="MAIN")
><br>Provide the base URL without trailing forw-slash, and provide the desired default branch

>snowstorm.debug         = True      (Boolean), standard = False

>snowstorm.activeFilter  = "True"    (String), standard = "True"

>snowstorm.loadCache()

>snowstorm.getConceptById(id="74400008")

>snowstorm.findConcepts([searchterm="testing device"], [ecl="<74400008"])

>snowstorm.getDescendants(id="74400008")

>snowstorm.getChildren(id="74400008")

>snowstorm.getParents(id="74400008")

>snowstorm.getMapMembers([id="74400008"], [referencedComponentId="74400008"], [targetComponent="74400008"], [mapTarget="P11.5"])

> snowstorm.printStatistics()

> snowstorm.writeCache()

Print statistics on number of queries and state of the cache:
> snowstorm.printStatistics()             # Prints to terminal