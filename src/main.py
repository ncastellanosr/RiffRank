# June 12, 2026. 1:50 p.m.

from flask import Flask
from backend_feed import riffrank, session
from schema import schema, CustomGraphQLView
import strawberry
from strawberry.flask.views import GraphQLView

index = Flask(__name__)
index.register_blueprint(riffrank, url_prefix = '/')

index.add_url_rule(
    '/graphql',
    view_func = CustomGraphQLView.as_view('graphql_view', schema = schema)
)

if __name__ == '__main__':
    index.run(debug = True, port = 8000)

# June 12, 2026. 2:30 p.m. Implementing templates
# June 12, 2026. 4:30 p.m. Implementing CSS
# June 12, 2026. 8:20 p.m. Implementing Scoring System
# June 12, 2026. 8:45 p.m. Break
# June 12, 2026. 9:10 p.m. Continue
# June 13, 2026. 1:10 a.m. Refining GUI
# June 13, 2026. 2:00 a.m. Finished
