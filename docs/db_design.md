# Database Design
*March 15, 2026. 11 p.m.*
The central piece is the relational database scheme, the gold layer. This is because the required transformation steps will become clear once we know the start point (raw data) and end point (this database scheme we are about to design).

First, lay out the individual columns we might need:

Primary Ingestion (including enrichment):

- Artist Name
- Artist Profile Photo
- Album Name
- Album Cover (as a link to the Spotify CDN)
- Album Release Year (or full date)
- Song Name
- Track Number (in the Album)
- Song Sub Genre
- Song Style
- Manually Entered Advanced Metadata

The last pieces of information are the ones that will feed the clustering algorithm for the recommendation system.

Eventually, information such as the credits will become necessary, but for now that will suffice.

To define the secondary ingestion columns, we need to define first how the rating system will work. This is a very complex part, so we need to keep it as minimal as possible for now.

Big sets of values make scoring difficult for humans. Visualizing a gradient instead of an input box should allow for easier scoring. I believe the existence of the neutral value is important.

The rating can be applied to an individual song (which is actually the main feature), and the user can either apply it to the album as well, or let the system generate it in base to the ratings of individual songs.

Also, advanced rating should be handy. Rating individual features of a song and then have a global score generated would be great for many people.

Additionally to the base rating system, there is an additional tier system. Two songs can be both perfect, so they both have the maximum grading value, and yet be on whole different levels. This often pushes people into switching from absolute to relative grading, degrading songs that are considered perfect and adding more chaos. Thus, a way to further honor a song without pushing the others away is necessary. And of course this also includes different degrees of honoring.

The definitive honoring tier should be present two, which is marking a song as favorite. Though this might become diffuse, so it is still up to consideration.

But that is not everything. Songs can be average but stand out for a specific feature that pushes it potentially into tiers. So, for the user to filter data, and for the recommendation system to build very specific playlists, a tagging system is also necessary.

Other oddly specific data such as listen date and time (since it is a tracking system), times listened, etc, even if less used and more difficult to gather the information for, might be useful int he future too.

Secondary Ingestion:

- Global Artist Score
- Artist Tier
- Artist Favorite
- Global Album Score
- Album Tier
- Album Favorite
- Global Song Score
- Advanced Song Score
- Song Tier
- Song Favorite

That data derives into the necessity for additional data:

- User

Even though many more pieces of data might be needed, we already have what we need to build a schema that can be expanded easily.

An ER diagram would be as follows:

![[Database Schema.png]]

That schema design is already solid, and more than enough to build the minimum viable product.