import pandas as pd
import folium
import gradio as gr

df_sw = pd.read_csv('tundra_swan.csv', parse_dates=['TimeStamp'])
df_co2 = pd.read_csv('co2.csv', parse_dates=['start_date','end_date'])

df_sw = df_sw.set_index('TimeStamp')
df_co2 = df_co2.set_index('start_date')

months = []
for i in range(2008, 2013):
    for j in range(1, 13):
        if i==2008:
            if j < 7:
                continue
        elif i==2012:
            if j > 7:
                break
        months.append(f"{i}-{j:02}")

def map(odate):
    m = folium.Map([50, -120], zoom_start=3)
    for index, row in df_sw[odate].iterrows():
      folium.CircleMarker([row['latitude'], row['longitude']],
                          popup=row['description'], 
                          radius=10, 
                          fill=True,
                          color=row['color'], 
                          fill_color=row['color'],
                          fill_opacity=0.5,
                          opacity=0.5).add_to(m)
    for index, row in df_co2[odate].iterrows():
        folium.Marker([row['latitude'],row['longitude']], popup=f"Temp:{row['tair_int']}\nNee:{row['nee']}").add_to(m)
    # html = m.get_root().render()
    html = m._repr_html_()
    html = (
        ""
        + html
        + ""
    )
    return html

with gr.Blocks() as app:
    gr.Markdown("# Overseer")
    gr.Markdown("### Overseeing Bird Migration")
    gr.Markdown("Choose Year-Month from dropdown list, and wait patiently for the result to show on the map!")
    dropdown = gr.Dropdown(months, label="Choose Year-Month")
    html = gr.HTML()
    dropdown.change(map, dropdown, html)

if __name__=="__main__":
    app.launch()