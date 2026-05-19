# Ingestion
*March 25, 2026. 2 p.m.*
This process has to request data from the Spotify API and store its raw payloads in JSON files.

![[Ingestion Diagram.png]]

The diagram is complemented with the following constraints:

1. The code must include testing
2. The code execution must be audited via logging
3. The ingestion process must be audited via logging
4. Tracked pagination is needed for the loops, possibly persistent
5. All types of fails should be handled properly

The required technologies comprehend:

1. The Python 'pathlib' and 'os'
2. Spotify Web API
3. HTTP and the Python 'requests' module
4. The Python 'json' module