# Transformation Layers
*April 26, 2026. 3:00 p. m.*
## Normalization
This is the first phase of the transformation layer. It consists on selecting the relevant data in the raw JSON payloads and building a primitive tabular format to store it. It consists just on iterating through the data lake to parse all JSON files in a selective order controlled according to the artists -> albums -> tracks hierarchy, similar to the ingestion flow. The resulting data structure is:

![[Normalized.png]]

## Enrichment
The data obtained from the previoius phase is not complete, and the missing data has to be filled manually, since it is not provided by the Spotify API, and overall, the target audience of the platform tends to be really strict about the values of this missing data. Some data is easy to fill by reading from plain text files, that is the subgenres and styles. Other data has to be filled through a CLI utility, since it involves IDs that are not readable by humans, that is precisely the relation entity between subgenres / styles and tracks.

## Relational Database
The result of joining the tabular data from phase 1 with the new data obtained in phase 2, is a set of tabular data that is enough to build the minimal relational database schema. So the last phase consists on connecting to and managing a PostgreSQL database. Once the database exists, we will possess the required data to build and feed the recommendation system, the backend and the frontend. SQLAlchemy will be used to implement this.

## Flow
The overall flow of the whole transformation layer can be seen as:

![[Transformation Diagram.png]]
