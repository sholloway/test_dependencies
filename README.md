# Salesforce Test Dependencies
This repo contains a proof of concept of identifying tests to run upon a Salesforce
org deployment. This code is not supported or endorsed by Salesforce. 
It is only intended as an example of traversing Apex class dependencies.

## Setup Instructions

1. Install [Devbox](https://www.jetpack.io/devbox/docs/quickstart/).
2. Install an isolated Python version with Devbox. This may take a little while.
   Note: This is to just install Python 3.12.x. If you're using a different 
   mechanism to manage Python locally, then you can skip steps 1 and 2.
  ```shell
  make env
  ```

3. Create a virtual environment and install Poetry to manage the Python dependencies.
  ```shell
  make setup
  ```

4. Use poetry to install the Python dependencies. 
  ```shell
  make init
  ```

## Use
The application is run by passing it two CSV files. On contains the output of 
querying the MetadataComponentDependency Salesforce object. The other, the list of 
files to find associated tests for. The application writes to STDOUT the list of 
tests to run. If the algorithm identifies Apex classes that are not in the 
dependency file (perhaps because they don't exist in the target org) then they are 
listed in STDOUT.

```shell
python -m test_dependencies \
  --dependency_list dependency_list.csv \
  --changed_list changed_files.txt \
  --degrees 2
```

Run the below query to get the dependency list. 
```sql
SELECT Id, 
  MetadataComponentId, 
  MetadataComponentName,
  MetadataComponentNamespace,
  MetadataComponentType, 
  RefMetadataComponentId, 
  RefMetadataComponentName, 
  RefMetadataComponentNamespace,
  RefMetadataComponentType 
FROM MetadataComponentDependency
WHERE RefMetadataComponentType = 'ApexClass' and MetadataComponentType='ApexClass'
```

This query can be run with the [Salesforce SOAP API](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_query.htm), the [Tooling API](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_metadatacomponentdependency.htm), and v2 of the [Bulk API](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/queries.htm).

See instructions for how to use the Tooling and Bulk API [here](https://help.salesforce.com/s/articleView?id=release-notes.rn_api_bulk_metadatacomponentdependency_beta.htm&release=226&type=5).

## How does it Work?
The Salesforce object MetadataComponentDependency contains relationship data of 
most metadata types in a Salesforce org. We can use this to identify the relationships
between Apex tests and the classes they test.

The process is:
**Bootstrap Steps**
1. Before running this app, download the dependency data using the above SOQL query. Store this in a CSV file. 
2. Get the list of changed Apex files that need their tests identified.

**Runtime Algorithm**
1. Validate commandline options. 
2. Parse the relationship CSV file (MetadataComponentDependency export) and load 
   it into memory as an [adjacency list](https://en.wikipedia.org/wiki/Adjacency_list) data structure.
3. Parse the changed file list (text file, with one class per file) and load it into 
   memory as a list of strings.
4. Find all tests by traversing the adjacency list. The __degrees__ option is used
   to specify how many graph traversals to make when searching for related tests.