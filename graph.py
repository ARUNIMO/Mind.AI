import json
import streamlit as st
import plotly.express as px

def graph():
    # Read the JSON file
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    # Sort the data by score in descending order
    data.sort(key=lambda x: x["score"], reverse=True)

    # Extract the top 10 names and scores
    top_names = [item["name"] for item in data[:10]]
    top_scores = [item["score"] for item in data[:10]]

    # Create a pie chart using Plotly Express with a specific color scale
    fig = px.pie(
        names=top_names,
        values=top_scores,
        title="Mood Graph",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    # Display the pie chart using Streamlit

    # Save the pie chart as a PNG file
    fig.write_image("mood_graph.png", format="png", scale=2.0)

# Call the function to display the graph
if __name__ == "__main__":
    graph()
