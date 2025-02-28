"""
TODO
"""
import pickle
import dash
import plotly.graph_objects as go
from arrange_icons import main as arrange_icons

# Init Dash app
app = dash.Dash(__name__)

# Arrange Icons
# walls, unhung = arrange_icons()

# with open("prearranged/walls5.pickle", "wb") as file:
#     pickle.dump(walls, file)

with open("prearranged/walls5.pickle", "rb") as file:
    walls = pickle.load(file)

figures = []

walls.sort(key=lambda w: w.id)

# This contains a list of tuples: Icon, x, y
for wall in walls:

    # Create a figure (WALL) and add icons
    fig = go.Figure()

    # Add icons
    for icon, (x, y) in wall.hung_icons:
        # print(icon.id, x, "-", x+icon.width, y, "-", y+icon.height)
        fig.add_layout_image(
            source=f"./assets/{icon.id}.png",
            x=x/wall.width,
            y=abs(y/wall.height - 1),
            xanchor="left",
            yanchor="top",
            sizex=(icon.width - 30)/wall.width,
            sizey=(icon.height - 30)/wall.height ,
        )


    # Configure wall layout
    fig.update_layout(
        title=f"Wall {wall.id} - Width: {wall.width} mm, Height: {wall.height} mm",
        xaxis=dict(range=[0, wall.width], showgrid=True),
        yaxis=dict(range=[0, wall.height], showgrid=True),
        width=wall.width,
        height=wall.height,
    )

    figures.append(dash.dcc.Graph(figure=fig))

# Dash layout
app.layout = dash.html.Div([
    dash.html.H1("Wall Icon Arrangement"),
    # dash.dcc.Graph(figure=fig),
    *figures,
    # dash.html.Img(src="./assets/1.png", draggable="true")
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
