# RiffRank. Pipeline - First Preview
## Introduction
This first preview consists on a fully functional and complete pipeline. The process begins when the data is obtained from the Spotify servers, and is designed to complete all necessary stages until a complete relational database schema is created and ready to feed a backend application.
## Used Technologies
1) Python
2) PostgreSQL
3) Docker
4) SpotiPy
5) SQLAlchemy
6) Pandas
## Warnings
THe pipeline is functional, but it has a lot of gaps and quirks, specially in resumability. A serious pipeline that is fault-tolerant and resilient should work in a distributed and parallel system. However, this pipeline works entirely in a linear way, and skipping steps or running from a middlepoint causes unthinkable amounts of weird errors that compromise the execution.

A main reason for this relies on the enrichment stage. It relies on CLI's, which by the way, are very rustical and basic on purpose, to feed the additional data onto the pipeline. Ideally, something like that would be a system external to the pipeline that is connected to it through an stable and controlled interface. But that would mean doing a frontend, which in the final product would likely be used by human moderators to feed the system
with the additional information. Clearly, the priority in this first development phase was to get a functional pipeline.

I consider this vulnerable state to be necessary and temporal. The final product would involve all stages running simultaneously, and instead of a CLI that exist in the middle of the process, a human moderator would be able to access a web application to feed data in real time, at any time.

As said, that is extremelly complex and not sane to do in early development.
## Installation
1) Clone the project repository in a project folder.
2) Use the docker-compose.yml file to create a PostgreSQL Docker container. *docker compose up -d*
3) Create a virtual Python environment. *python -m venv riffrank one level up*
4) Activate the virtual environment. *source bin/activate*
5) Execute the command *pip install -r requirements.txt* to set up the virtual environment.
6) Rename *.env.example* to *.env* and fill in the blanks. The first three fields are obtained from a Spotify Web API application, created in the Spotify Developer Dashboard. The rest of the fields come from the PostgreSQL docker-compose.yml.
## How To Use
First, execute *python master.py*.
Once inside, the first thing you will see is a prompt asking you if you want to execute the automatic mode. Enter only and only a lowercase y, and press ENTER. As discussed before, this code is fragile if you don't follow the rules.

Then you will see a prompt where it asks you to follow a link. You have to open that link, and once inside, you will see a Spotify login page. Once you authenticate with your Spotify Account, the web browser will redirect you to an empty page. Copy the link you were redirected to, and paste it in the terminal, then press ENTER.

Now you will see that the program will connect to the Spotify API and will start ingesting data from your followed artists. If you have too many followed artists, I recommend to press Ctrl + C after some have completed (watch the log carefully to know for sure). One artist will be broken, partially ingested. Review the log to know which it was, and delete its folder, just to be safe. In any case, you should ingest only two or three artists.

Then restart the program, and this time choose not to follow the auto mode, by entering anything different to a lowercase y. Then choose not to do preload, neither the ingestion, and press y for all upcoming stages.

The enrichment step requires human interaction, and the CLI can be fragile if you are reckless, so just be careful and follow the rules. Fill in the data however you want. When you are prompted to choose which subgenre and style each artist has, remember:

You just have to write the full string for the subgenre or style, as entered in the previous step. For this reason, I recommend to enter just a short lowercase keyword that doesn't take long to type. This is backend data anyways.

At the end, you will be able to use the PostgreSQL console (PSQL) to navigate your schemas. If you connect to the riffrank database, you will be able to see the populated data, ready to be used in a web application.
## Explaination
To be brief, this is a summary of what each stage does:

1) The preload phase loads the internal Spotify IDs for the artists you follow on your account, into a JSON file.
2) The ingestion phase does requests to the Spotify Web API to load the info for each artists, its albums, and the tracks for those albums.
3) The normalization phase extracts the meaningful data from those raw payloads, and arranges it in tabular data (dataframes) that is then stored in Parquet files. As a note, I'd like to mention that the disk usage can be more efficient if an incremental writting method is used, which is offered by libraries like PyArrow.
4) The enrichment phase is the phase that is not strictly part of the pipeline, but the data it provides is important, so it had to be implemented somehow. It just completes the data required to build the full relational database schema.
5) The database phase manages the database connection, existence of the database, and populates it. Things like updating an existing database are not supported yet.