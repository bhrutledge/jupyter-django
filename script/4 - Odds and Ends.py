
# coding: utf-8

# In[1]:

from django.db import connection
from graphviz import Source
from IPython.display import Image
import pandas as pd

pd.options.display.max_rows = 10


# ## Using SQL

# In[2]:

dot = get_ipython().getoutput('/Users/brian/Code/jahhills.com/hth/manage.py graph_models music 2>/dev/null')
Source(dot.n)


# In[3]:

songs = pd.read_sql("""
SELECT
    id AS song_id
    , title AS song_title
    , release_id
FROM music_song
""", connection)

songs.head()


# In[4]:

releases = pd.read_sql("""
SELECT
    id AS release_id
    , title AS release_title
    , date AS release_date
FROM music_release
""", connection)

releases.head()


# In[5]:

song_releases = songs.merge(releases).set_index('song_id')
song_releases.head()


# In[6]:

release_tracks = song_releases.groupby('release_title')['song_title'].count()
release_tracks


# In[7]:

release_tracks.describe()


# ## CSV Import/Export

# In[8]:

song_releases.to_csv('song-releases.csv')
get_ipython().system('head song-releases.csv')


# In[9]:

pd.read_csv('song-releases.csv').head()


# ## Other Stuff
# 
# - "File > Download as"
# - GitHub rendering
# - Best practices
# - Dashboard

# In[ ]:



