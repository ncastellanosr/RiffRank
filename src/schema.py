import strawberry
from typing import List
import backend_data
from strawberry.flask.views import GraphQLView as BaseGraphQLView
from flask import Request

@strawberry.type
class ArtistResult:
    id: str
    name: str
    picture: str

@strawberry.type
class AlbumResult:
    id: str
    artist_id: str
    name: str
    cover: str
    release: str

@strawberry.type
class TrackResult:
    id: str
    album_id: str
    artist_name: str
    album_name: str
    name: str

@strawberry.type
class SearchResults:
    artists: List[ArtistResult]
    albums: List[AlbumResult]
    tracks: List[TrackResult]

@strawberry.type
class Query:
    @strawberry.field
    def search(self, info: strawberry.types.Info, query: str) -> SearchResults:
        engine = info.context['engine']

        with engine.connect() as connection:
            raw_artists = backend_data.search_artists(connection, query)
            raw_albums = backend_data.search_albums(connection, query)
            raw_tracks = backend_data.search_tracks(connection, query)

        return SearchResults(
            artists = [ArtistResult(id=r[0], name=r[1], picture=r[2]) for r in raw_artists],
            albums = [AlbumResult(id=r[1], artist_id=r[0], name=r[2], cover=r[3], release=r[4]) for r in raw_albums],
            tracks = [TrackResult(id=r[5], album_id=r[2], artist_name=r[1], album_name=r[3], name=r[6]) for r in raw_tracks]
        )

    @strawberry.field
    def artists(self, info: strawberry.types.Info) -> List[ArtistResult]:
        engine = info.context['engine']

        with engine.connect() as connection:
            raw = backend_data.list_artists(connection)

        return [ArtistResult(id=r[0], name=r[1], picture=r[2]) for r in raw]

    @strawberry.field
    def artist(self, info: strawberry.types.Info, id: str) -> List[AlbumResult]:
        engine = info.context['engine']

        with engine.connect() as connection:
            _, albums = backend_data.list_artist(connection, id)

        return [AlbumResult(id=r[1], artist_id=r[0], name=r[2], cover=r[3], release=r[4]) for r in albums]

    @strawberry.field
    def album(self, info: strawberry.types.Info, id: str) -> List[TrackResult]:
        engine = info.context['engine']

        with engine.connect() as connection:
            _, tracks = backend_data.list_album(connection, id)

        return [TrackResult(id=r[1], album_id=r[0], artist_name='', album_name='', name=r[3]) for r in tracks]

schema = strawberry.Schema(query=Query)

class CustomGraphQLView(BaseGraphQLView):
    def get_context(self, request: Request, response) -> dict:
        from backend_feed import session
        return {'engine': session.engine}
