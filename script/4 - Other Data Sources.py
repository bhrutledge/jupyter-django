
# coding: utf-8

# # Other Data Sources

# In[1]:

from django.core.management import call_command
from django.db import connection
from graphviz import Source
from IPython.display import Image
import pandas as pd

pd.options.display.max_rows = 10


# ## Using SQL

# Another way to get the output of a management command:

# In[2]:

get_ipython().run_cell_magic('capture', 'dot', "call_command('graph_models', 'music')")


# In[3]:

Source(dot)


# In[4]:

songs = pd.read_sql("""
SELECT
    id AS song_id
    , title AS song_title
    , track AS release_track
    , release_id
FROM music_song
""", connection)

songs.head()


# In[5]:

releases = pd.read_sql("""
SELECT
    id AS release_id
    , title AS release_title
    , date AS release_date
FROM music_release
""", connection)

releases.head()


# Join the `DataFrame`s on the common `release_id` column:

# In[6]:

song_releases = songs.merge(releases).set_index('song_id')
song_releases.head()


# In[7]:

release_tracks = song_releases.groupby('release_title')['song_title'].count()
release_tracks


# In[8]:

release_tracks.describe()


# ## Using CSVs

# In[9]:

song_releases.to_csv('song-releases.csv')
get_ipython().system('head song-releases.csv')


# In[10]:

pd.read_csv('song-releases.csv').head()


# ## Many others
# 
# - Excel
# - HTML tables
# - JSON
# - Web APIs via [requests](http://docs.python-requests.org/en/master/)

# In[ ]:



