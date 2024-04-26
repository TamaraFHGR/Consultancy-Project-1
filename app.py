    fig = px.scatter(df, x='MappedFixationPointX', y='MappedFixationPointY',
                     size='FixationDuration',
                     title='Gaze Plot')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
    )
    return fig