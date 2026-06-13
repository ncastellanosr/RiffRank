# Backend
*June 12, 2026. 11:15 a.m.*
The backend consists on a script that runs constantly on a server to provide functionalities to the frontend on-demand. Each user has its own connection to the backend with its own authentication, which means that the backend functionalities should run in multiple isolated instances, one for each user. Since our minimum viable product doesn't include multi-user support, we are skipping that architecture for now, but it can't do bad to design it ahead of time.

![[Backend Diagram.png]]

As of the current goals of the project, moderator access is obtained by using the master orchestrator, and the user access is provided by default through a local instance of the backend script.

The backend cannot be designed without thinking on the information that the frontend needs to work. As we discussed somewhere else in this document, the frontend for this sprint has the following functionalities:

1. Allow to access the information for artists and each of its albums
2. Allow to rate artists, albums and songs

The frontend would consist on the following screens:

1. **Artist Search:** No actual search implemented for now. Instead, a full list with all the artists.
2. **Artist Info:** A general overview of the artist with links to each album and rating options.
3. **Album Info:** A general overview of the album with rating options.

From the database, the following entities would feed those screens:

1. **Artists Table:** Feeds the Artist Search screen.
2. **Artist View:** Feeds the Artist Info screen.
3. **Album View:** Feeds the Album Info screen.

The backend should provide functions to access those entities, plus functions to write the scorings to the appropriate tables.