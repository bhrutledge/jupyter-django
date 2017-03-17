
# coding: utf-8

# # Introducing Pandas
# 
# From the [docs](http://pandas.pydata.org/pandas-docs/stable/index.html):
# 
# > A Python package providing fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy and intuitive.
# 
# We also use [matplotlib](http://matplotlib.org/):
# 
# > A Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms.
# 
# Requirements:
# 
# ```
# (venv) $ pip install pandas matplotlib
# ```
# 
# We're going to see a sliver of the functionality provided by these packages.

# In[1]:

import pandas as pd
pd.options.display.max_rows = 20

get_ipython().magic('matplotlib inline')


# ## Introducing `DataFrame`

# From the [docs](http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe):
# 
# > __DataFrame__ is a 2-dimensional labeled data structure with columns of potentially different types. You can think of it like a spreadsheet or SQL table. It is generally the most commonly used pandas object.
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


# The previous cell demonstrates a good practice: make all of your modifications to a variable in one cell. This will help prevent surprises when you execute cells out of order as you play with code. If you need to make modifications later in the notebook, assign the result to a new variable.

# ## Answering questions
# 
# 
# ### What gigs  did we play last year?

# Using the date as the `Index` allows for fast slicing:

# In[16]:

gigs.loc['2016']


# ### How many gigs have we played each year?

# The date `Index` also allows for fast aggregration:

# In[17]:

# resample('A') creates year-end groups like '2005-12-31'
# to_period() turns that into '2005'
years = gigs.resample('A').size().to_period()
years


# In[18]:

years.plot.bar()


# ### What are our most active months?

# Get the dates as a `Series`:

# In[19]:

gig_dates = gigs.reset_index()['date']
gig_dates


# Convert those to sortable month names:

# In[20]:

# Series.dt gives us access to date-related methods
gig_months = gig_dates.dt.strftime('%m %b')
gig_months


# Count the unique values:

# In[21]:

months = gig_months.value_counts()
months


# In[22]:

# matplotlib has lots of options for customization
ax = months.sort_index().plot.bar(table=True, figsize=(10,5))
ax.get_xaxis().set_visible(False)


# ### What cities have we played?

# In[23]:

gig_cities = gigs['city']
gig_cities


# In[24]:

cities = gig_cities.value_counts()
cities


# In[25]:

cities.describe()


# In[26]:

# Adding the ; suppresses `<matplotlib.axes._subplots.AxesSubplot ...>`
cities[:10].sort_values().plot.barh();


# When did we play in Pittsburgh?
# 
# We can use a `Series` of boolean values to slice our `DataFrame`:

# In[27]:

# Series.str gives us access to string methods
in_pgh = gig_cities.str.contains('Pittsburgh')
in_pgh


# In[28]:

gigs[in_pgh]


# ### What states have we played?
# 
# The `Gig` model doesn't have a `state` field, so we need to parse it out. In vanilla Python, we'd do:

# In[29]:

'Boston, MA'.split(',')[1].strip()


# With pandas, we can do the same thing for every `Series` element:

# In[30]:

states = gig_cities.str.split(',').str.get(1).str.strip().value_counts()
states


# In[31]:

states.describe()


# In[32]:

# Don't rotate the x-axis labels
states[:5].plot.bar(rot=0);


# ### What venues have we played?

# `DataFrame` has powerful grouping and aggregration functionality:

# In[33]:

venues = gigs.groupby(['venue', 'city']).size()
venues


# This `Series` has a `MultiIndex`. Very useful, but beyond the scope of this presentation...

# In[34]:

venues.describe()


# In[35]:

top_venues = venues.nlargest(10)
top_venues


# In[36]:

top_venues.sort_values().plot.barh();


# In[ ]:



