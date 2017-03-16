
# coding: utf-8

# # Introducing Pandas
# 
# Requirements:
# 
# ```
# (venv) $ pip install pandas matplotlib
# ```

# In[1]:

import pandas as pd
pd.options.display.max_rows = 20


# ## Introducing `DataFrame`

# From the [Pandas docs](http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe):
# 
# > `DataFrame` is a 2-dimensional labeled data structure with columns of potentially different types. You can think of it like a spreadsheet or SQL table. It is generally the most commonly used pandas object.
# 
# There are many ways to get a `DataFrame`, but we'll start with a list of dictionaries.

# In[2]:

df = pd.DataFrame([
    {'integer': 1, 'float': 1.0, 'string': 'one'},
    {'integer': 2, 'float': 2.0, 'string': 'two'},
    {'integer': 2, 'float': 2.0, 'string': 'two'},
    {'integer': 3, 'float': 3.0, 'string': 'three'},
])

# Print some details about the DataFrame
df.info()
df


# The Jupyter Notebook automatically renders `DataFrame` as HTML!
# 
# Note the first column; this is an `Index`, and is an essential component of `DataFrame`. Here, it was auto-generated, but we can also set it:

# In[3]:

df_index = df.set_index('string')
df_index


# The `Index` plays a key role in slicing the `DataFrame`:

# In[4]:

# Slice by label
df_index.loc['two']


# In[5]:

# Slice by position
df_index.iloc[-2:]


# We can also get individual columns:

# In[6]:

floats = df_index['float']
floats


# This is a `Series`, which is essentially a one-dimensional `DataFrame`, with a defined data type. Put another way, a `DataFrame` is a collection of `Series`.
# 
# Note that the `Series` retained the `Index` of our `DataFrame`, so we can use similar slicing:

# In[7]:

floats['two']


# `Series` and `DataFrame` support element-wise operations:

# In[8]:

df_index['float'] * df_index['integer']


# In[9]:

df_index * df_index


# In[10]:

number_format = 'Number {}'.format
df_index['integer'].apply(number_format)


# In[11]:

df_index.applymap(number_format)


# ## Using `DataFrame` with Django

# Django gives us a handy way to build a list of dictionaries:

# In[12]:

gig_values = Gig.objects.past().published().values('date', 'venue__name', 'venue__city')
gig_values[:5]


# `DataFrame` doesn't know what to do with a `QuerySet`; it wants something that looks more like a list.  
# We could use `list(gig_values)`, but `gig_values.iterator()` is more efficient.

# In[13]:

gigs = pd.DataFrame(gig_values.iterator())
gigs.info()
gigs


# This is a good place to start, and we've already got the answer to "How many gigs have we played"?
# 
# However, there are a few ways we can make this easier to work with:
# 
# - Shorter column names
# - Predictable column order
# - Indexed and sorted by date
# 
# For more control, we'll use a list of tuples to initialize the DataFrame.

# In[14]:

gig_values = Gig.objects.past().published().values_list('date', 'venue__name', 'venue__city')
gig_values[:5]


# In[15]:

gigs = pd.DataFrame(gig_values.iterator(), columns=['date', 'venue', 'city'])

gigs['date'] = pd.to_datetime(gigs['date'])
gigs = gigs.set_index('date').sort_index()

gigs.info()
gigs.head()


# ## Answering questions
# 
# 
# ### What gigs  did we play last year?

# In[16]:

gigs.loc['2016']


# ### How many gigs have we played each year?

# In[17]:

years = gigs.resample('A').size().to_period()
years


# In[18]:

get_ipython().magic('matplotlib inline')


# In[19]:

years.plot.bar()


# ### What are our most active months?

# In[20]:

months = gigs.reset_index()['date'].dt.strftime('%m %b').value_counts()
months


# In[21]:

ax = months.sort_index().plot.bar(table=True, figsize=(10,5))
ax.get_xaxis().set_visible(False)


# ### What cities have we played?

# In[22]:

gigs['city']


# In[23]:

cities = gigs['city'].value_counts()
cities


# In[24]:

cities.describe()


# In[25]:

top_cities = cities[cities > cities.mean()]
top_cities


# When did we play in Pittsburgh?

# In[26]:

in_pgh = gigs['city'].str.contains('Pittsburgh')
gigs[in_pgh]


# In[27]:

# Adding the ; suppresses `<matplotlib.axes._subplots.AxesSubplot ...>`
top_cities.sort_values().plot.barh();


# ### What states have we played?

# In[28]:

states = gigs['city'].str.split(',').str.get(1).value_counts()
states


# In[29]:

states.describe()


# In[30]:

states[:5].plot.bar(rot=0);


# ### What venues have we played?

# In[31]:

venues = gigs.groupby(['venue', 'city']).size()
venues


# This `Series` has a `MultiIndex`. Very powerful, but beyond the scope of this talk...

# In[32]:

venues.describe()


# In[33]:

top_venues = venues.nlargest(10)
top_venues


# In[34]:

top_venues.sort_values().plot.barh();


# In[ ]:



