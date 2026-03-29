import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import os
import matplotlib.pyplot as plt
from PIL import Image

st.title(" Player Behavior Analysis Dashboard")
st.caption("Interactive dashboard analyzing player behavior, bot distribution, and engagement patterns across maps.")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_all_data(base_path="player_data"):
    frames = []
    
    for day_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, day_folder)
        
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                
                try:
                    table = pq.read_table(file_path)
                    df_temp = table.to_pandas()
                    
                    df_temp['event'] = df_temp['event'].apply(
                        lambda x: x.decode('utf-8') if isinstance(x, bytes) else x
                    )
                    
                    df_temp['is_bot'] = df_temp['user_id'].apply(
                        lambda x: str(x).isdigit()
                    )
                    
                    frames.append(df_temp)
                
                except:
                    continue
    
    return pd.concat(frames, ignore_index=True)

df = pd.read_csv("optimized_data.csv")
df['ts'] = pd.to_datetime(df['ts'])
df['date'] = df['ts'].dt.date
df['ts'] = pd.to_datetime(df['ts'])
df['date'] = df['ts'].dt.date

col1, col2, col3 = st.columns(3)

col1.metric("Total Players", df['user_id'].nunique())
col2.metric("Total Matches", df['match_id'].nunique())
col3.metric("Total Events", len(df))
# -------------------------------
# MAP CONFIG
# -------------------------------
MAP_CONFIG = {
    "AmbroseValley": {"scale": 900, "origin_x": -370, "origin_z": -473},
    "GrandRift": {"scale": 581, "origin_x": -290, "origin_z": -290},
    "Lockdown": {"scale": 1000, "origin_x": -500, "origin_z": -500},
}

def world_to_minimap(x, z, map_name):
    config = MAP_CONFIG[map_name]
    
    u = (x - config["origin_x"]) / config["scale"]
    v = (z - config["origin_z"]) / config["scale"]
    
    pixel_x = u * 1024
    pixel_y = (1 - v) * 1024
    
    return pixel_x, pixel_y

def load_map_image(map_name):
    base_path = "minimaps"
    
    png_path = os.path.join(base_path, f"{map_name}_Minimap.png")
    jpg_path = os.path.join(base_path, f"{map_name}_Minimap.jpg")
    
    if os.path.exists(png_path):
        return Image.open(png_path)
    
    if os.path.exists(jpg_path):
        return Image.open(jpg_path)
    
    raise FileNotFoundError(f"No minimap found for {map_name}")

# -------------------------------
# CONTROLS
# -------------------------------
st.sidebar.title("Controls")

map_name = st.sidebar.selectbox(
    "Select Map",
    df['map_id'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['date'].min(), df['date'].max()]
)

match_list = df[df['map_id'] == map_name]['match_id'].unique()

selected_match = st.sidebar.selectbox(
    "Select Match (Optional)",
    ["All"] + list(match_list)
)

view_option = st.sidebar.selectbox(
    "Select View",
    ["Human vs Bot", "Events", "Heatmap"]
)
show_split = st.sidebar.checkbox("Compare Human vs Bot movement")

st.markdown(f"### 📍 {map_name} — {view_option}")
# -------------------------------
# DATA FILTER
# -------------------------------
df_map = df[df['map_id'] == map_name].copy()

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    df_map = df_map[
        (df_map['date'] >= start_date) &
        (df_map['date'] <= end_date)
    ]

# Match filter
if selected_match != "All":
    df_map = df_map[df_map['match_id'] == selected_match]

df_map[['pixel_x', 'pixel_y']] = df_map.apply(
    lambda row: world_to_minimap(row['x'], row['z'], row['map_id']),
    axis=1,
    result_type='expand'
)

img = load_map_image(map_name)

# -------------------------------
# VISUALIZATION
# -------------------------------
if show_split:
    fig, axes = plt.subplots(1, 2, figsize=(14,6))
    
    human_df = df_map[df_map['is_bot'] == False]
    bot_df = df_map[df_map['is_bot'] == True]
    
    human_sample = human_df.sample(min(2000, len(human_df)))
    bot_sample = bot_df.sample(min(2000, len(bot_df)))
    
    # Human
    axes[0].imshow(img, extent=[0, 1024, 1024, 0])
    axes[0].scatter(human_sample['pixel_x'], human_sample['pixel_y'],
                    color='blue', s=1, alpha=0.5)
    axes[0].set_title("Human Movement")
    
    # Bot
    axes[1].imshow(img, extent=[0, 1024, 1024, 0])
    axes[1].scatter(bot_sample['pixel_x'], bot_sample['pixel_y'],
                    color='green', s=1, alpha=0.5)
    axes[1].set_title("Bot Movement")
    
    st.pyplot(fig)

else:
    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(img, extent=[0, 1024, 1024, 0])

    if view_option == "Human vs Bot":
        human_df = df_map[df_map['is_bot'] == False]
        bot_df = df_map[df_map['is_bot'] == True]
        
        human_sample = human_df.sample(min(2000, len(human_df)))
        bot_sample = bot_df.sample(min(2000, len(bot_df)))
        
        ax.scatter(human_sample['pixel_x'], human_sample['pixel_y'],
                   color='blue', s=1, alpha=0.5)
        
        ax.scatter(bot_sample['pixel_x'], bot_sample['pixel_y'],
                   color='green', s=1, alpha=0.5)
        
        st.caption("Blue = Human | Green = Bot")

    elif view_option == "Events":
        kills = df_map[df_map['event'] == 'Kill']
        loot = df_map[df_map['event'] == 'Loot']
        
        ax.scatter(kills['pixel_x'], kills['pixel_y'], color='red', s=30)
        ax.scatter(loot['pixel_x'], loot['pixel_y'], color='yellow', s=10)
        
        st.caption("Red = Kill | Yellow = Loot")

    elif view_option == "Heatmap":
        hb = ax.hexbin(
            df_map['pixel_x'],
            df_map['pixel_y'],
            gridsize=60,
            cmap='inferno',
            mincnt=5,
            alpha=0.6
        )
        
        fig.colorbar(hb, ax=ax)

    st.pyplot(fig)
