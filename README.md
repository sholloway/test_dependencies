# Salesforce Test Dependencies

This repo contains a proof of concept for identifying tests to run upon a Salesforce
org deployment. This code is NOT SUPPORT or endorsed by Salesforce.
It is only intended as an example of traversing Apex class dependencies using the
MetadataComponentDependency object.

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

The application is run by passing it two CSV files. One contains the output of
querying the MetadataComponentDependency Salesforce object. The other is a list of
files to find associated tests for.

The application writes to STDOUT the list of tests to run. If the algorithm identifies Apex classes that are not in the
dependency file (perhaps because they don't exist in the target org) then they are
listed in STDOUT.

```shell
python -m test_dependencies \
  --dependency_list dependency_list.csv \
  --changed_list changed_files.txt \
  --degrees 2
```

## Examples

The proof of concept has two examples. These can be run with a make target or
manually.

### 2000 member Dependency File

The first example uses just 2000 items exported from a Salesforce org using the
Tooling API. It demonstrates why you should use the Bulk API to export all dependencies.
Notice in the output the highlighted missing items.

Run `make run_2k' which is just a shortcut for the below shell snippet.

```shell
python -O test_dependencies \
		--dependency_list ./examples/2k.csv \
		--changed_list ./examples/2k_changed_list.txt \
		--degrees 3
```

This should output the below.

```shell
|------------------------|-------------------------------------------
| Metric                 | Value                                    |
|------------------------|-------------------------------------------
| Changed Files          | 3                                        |
| Tests in DAG           | 73                                       |
| Apex Classes in DAG    | 708                                      |
| Tests to Run           | 9                                        |
| Missing Items in DAG   | 5                                        |
|------------------------|-------------------------------------------

Identified 12.33 percent of all tests.

Tests to Run
CSC_NotificationPostTest
CSC_AdditionalFieldsUtilsTest
CSC_ViewAllRecommendationsControllerTest
CSC_NotificationsControllerTest
CSC_PSM_MyCustomersFilterTest
CSC_UserUtilsTest
CSC_RenewalAmountFilterTest
CSC_CompassCloneControllerTest
CSC_NewCompassControllerTest

Missing Items
PubQuoteAttachmentController
SfdcPublishedQuoteCleanup
CSC_ListServiceWave
PubQuotePrintController
PubQuoteUnPublishController
```

### 100k member Dependency File

The second example uses fake data. A generated dependency file with over 100k
rows is used to demonstrate what a realistic file is like. This is just to
test the memory consumption and speed of the proof of concept code.

Run `make run_100k' which is just a shortcut for the below shell snippet.

```shell
python -O test_dependencies \
		--dependency_list ./examples/100k.csv \
		--changed_list ./examples/100k_changed_list.txt \
		--degrees 5
```

This should output the below.

```shell
|------------------------|-------------------------------------------
| Metric                 | Value                                    |
|------------------------|-------------------------------------------
| Changed Files          | 20                                       |
| Tests in DAG           | 40,000                                   |
| Apex Classes in DAG    | 119,775                                  |
| Tests to Run           | 19                                       |
| Missing Items in DAG   | 0                                        |
|------------------------|-------------------------------------------

Identified 0.05 percent of all tests.

Tests to Run
ColdSheRecentlySingleWhereTest
StandardLandBlueTest
TownTest
MissionTest
WeightTest
NatureFillTest
WhichExactlyUponMyExecutiveTest
FinalAndStandMemberTest
SurfaceLetTreatTest
KnowledgeTest
BestAlsoReachSeaTest
FriendStayDreamOfferTest
SpeechFullEventCheckGroupTest
ActivityUseLifeMagazineInvolveTest
RoadBuyTest
FiveFamilyHimTest
MainRadioTest
AnimalOfficerNetworkStoreTest
SeekBitQuestionCloseStandTest
```

## Creating a Dependency File

Run the below query in a Salesforce org to create a dependency list.

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
4. Find all tests by traversing the adjacency list. The **degrees** option is used
   to specify how many graph traversals to make when searching for related tests.
