# Salesforce Test Dependencies
This repo is a proof of concept. 

## Setup Instructions

1. Install [Devbox](https://www.jetpack.io/devbox/docs/quickstart/).
2. Install an isolated Python version with Devbox. This may take a little while.
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
files to find associated tests for.

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

