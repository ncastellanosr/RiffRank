# Data Life cycle
*March 15, 2026. 8 p.m.*
As a data engineer, I will center the development of the project around the data pipeline. This means the maximum design and implementation focus will be precisely the pipeline itself. That doesn't mean the other features circling around (such as the front end) will be weak or not work properly, it rather means they will just not be so feature-rich and complex as the data pipeline.

The fundamental parts of a data pipeline in general are as follows.

1. **Ingestion:** Retrieving the data from one or multiple data sources
2. **Data Lake:** A place where raw data is stored and preserved
3. **Data Transformation:** One or multiple processes where the data is cleaned and normalized
4. **Data Warehouse:** Normally, a relational database where the transformed data is stored
5. **Serving:** Process where the data is delivered to an end, which can be a dashboard, an application, an end user in general, and even BI tools

There are two primary architectures to design or perform data transformations: ETL and ELT.

- **ETL or Extract-Transform-Load:** The data is transformed before being loaded into a warehouse
- **ELT or Extract-Load-Transform:** The data is transformed inside of the warehouse

Recommendation systems add a new section into the data life cycle. To be specific, a recommendation system requires feedback, as it feeds with data from the user, which changes through time, therefore, the output of the recommendation system changes through time as well. This means that the recommendation system operates as a loop in the data life cycle, specifically, between the warehouse and serving steps, where the data is constantly processed under its algorithms while it keeps changing.

From a data engineering standpoint, the user data is actually a second ingestion point that bypasses steps 2 and 3, and instead merges directly with the base data of the system in step 4, to then be fed into the recommendation system as an intermediary step before the serving.

So, for our specific use of case, which is of a very reduced scope, the steps would be performed as follows:

1. Data Ingestion from Spotify via API
2. Storage of raw data into local JSON files
3. Clean, normalize and enrich the data
4. Store the transformed data in a PostgreSQL database
5. Data Ingestion from the user via Dashboard
6. Run the recommendation system
7. Deliver the data to a dashboard

From the above defined steps, it is to note that the dashboard is not a proper part of the pipeline, rather one of the ends it connects to, since the pipeline is *delivering* to the dashboard. Also, step 6 will most likely be skipped very often, as it is only needed if the data is different, which means different results since the last runtime.

The transformation step is more complex in comparison to the others as it involves intermediary layers of transformation, and subsequently, multiple degrees of transformed data. The Medallion architecture actually fits extremely well for this specific case:

1. **Bronze Layer:** The raw JSON files directly retrieved from the API. Reachable by ingesting from the Spotify API and storing the raw payloads
2. **Silver Layer:** The data is cleaned and normalized. Reachable by selecting, cleaning and normalizing the relevant data
3. **Gold Layer:** The data is ready to be stored in the warehouse. Reachable by the enrichment of the data

Below is the full data life cycle diagram, which reflects everything discussed in this section:

![[Data Cycle.png]]