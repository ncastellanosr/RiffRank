# Data Pipeline
*March 16, 2026. 12 a.m.*
## Ingestion
The Spotify API offers the possibility to perform multiple GET requests. To build a Snapshot of raw data, we actually need to perform multiple of them and synthesize them into either the same JSON file, or the same set of JSON files. Synthesizing would drift our raw data a bit apart from the original payload, so perhaps the best option is to keep a set of JSON files per snapshot.

So, for the ingestion, we need to know which artist or artists we want to pull data from. For that, we first manually compile artist ID's into a plain text file that we will loop through to automatize pulling the data. To escalate this, we just need to build a text file with metal music artist Spotify ID's, which is still manual.

The first API call we will need is:

```
curl --request GET \
  --url https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
```

Then, we need to retrieve the discography:

```
curl --request GET \
  --url https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg/albums \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
```

And finally, we pull the songs:

```
curl --request GET \
  --url https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy/tracks \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
```
## Normalization
This is the actual process where we will choose said parts of the JSON files. As a summary:

First API call:

- name - Maps to artists.name
- images > URL - Maps to artists.picture

Second API call:

- name - Maps to albums.name
- images > URL - Maps to albums.cover
- release_date - Maps to albums.release_date

Third API call:

- items > name - Maps to songs.name
- items > track_number - Maps to songs.track

We cannot actually build the relational database yet, but we can already get close to a primitive. In this part of the process it is extremely important to be careful to build and preserve information that links the albums to their artist and the songs to their album.
## Enrichment
This part involves manually completing the data with the information that Spotify does not provide. An option is to use MusicBrainz, which is a free and very complete database with cross references to Spotify song ID's, but for now, we will only list what data is needed to complete this part of the process. As a summary, we need to fill the tables:

- subgenres
- styles
- tags
- songs_subgenres
- songs_styles
- user (abstract, for testing of the pipeline)

Now we can actually implement the database schema we designed. Since the pipeline is the focus, we will implement users as an abstract interface, well enough for it to work. Tags are by default offered by the system, and custom tags created by users are not required for the minimum viable product. This means that, at least during development, both the users table and the tags table will be manually populated since the schema creation. The scoring and tag markings are populated via use of the system.

After we have this base schema, and it is populated we can allow the dynamic further population via dashboard. During development, this will probably be done manually from code, since the dashboard will likely be the last feature to be implemented. A minimal CLI interface might be implemented
## Recommendation System
This is actually the complicated part, not because of the algorithm itself, but because of how the flow of the pipeline should behave in this point. To be clear, an event should trigger the execution of the algorithm. In the minimum viable product, it will likely be the event where the user loads their main dashboard. But there should also be a flag, in case the data that feeds the algorithm didn't change between sessions, which could optimize by saving unnecessary executions. This already involves server programming for the final deployment, but during local testing, we can just implement the logic on the local scripts and perform manual executions.

The input of the recommendation system will consist on the user ratings,  tag marks and advanced metadata (song mood, genre, sub genre and style in this draft) from the relational database, and in the future (not for minimal viable product), the extended metadata, and the output should (at least as far as I have planned) a set or various sets of songs. For that, an intermediary cluster map, which will be built through the k-means algorithm, is necessary, and the sets will be grouped starting from the center of each cluster.

By the way, it is important to mark that the results of the algorithm will not be stored in the database, rather just temporarily in the RAM per execution. This is because, since the flow is already different here (this is the part that loops instead of doing linear movements of data), separating it should be good, at least for now.
## Serving
This is an easy one. Once the information exists in the abstract space that is the rest of the pipeline, the front end is the one who must pull it via requests to the server. In local testing, this can just be queries to the database. The specific design of the front end is not clear yet, but it can be clearly designed in the future using the requirements as guide.

It is wise that the dashboard itself doesn't do direct queries and requests to the server and database. Those should be responsibilities of the back end, which will act as an API for the front end. The requirement is that the front end must only see data and serve it. The one who has to gather that data and manage the work involved in such tasks is the back end.