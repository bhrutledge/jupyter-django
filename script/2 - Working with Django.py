
# coding: utf-8

# # Working with Django
# 
# We'll be working with the data from [my band's website](http://www.hallelujahthehills.com/), which uses the Django admin as a basic CMS. The source is on [GitHub](https://github.com/bhrutledge/jahhills.com).
# 
# Requirements:
# 
# ```
# $ brew install graphviz
# (venv)$ pip install pydot graphviz
# ```
# 
# 

# ## What do our models look like?
# 
# Let's use some of IPython's magic to find out.

# Thanks to `manage.py shell_plus --notebook`, all of our models have already been imported.

# In[1]:

get_ipython().magic('pinfo2 Gig')


# In[2]:

from inspect import getfile


# In[3]:

gig_file = getfile(Gig)
gig_file


# In[4]:

get_ipython().magic('pycat $gig_file')


# In[5]:

# We still need to import non-model classes...
from core.models import PublishedModel
get_ipython().magic('pycat {getfile(PublishedModel)}')


# ---

# In[6]:

from os import path


# In[7]:

get_ipython().system('ls -l {path.dirname(gig_file)}')


# ---

# In[8]:

from graphviz import Source
from IPython.display import Image


# In[9]:

get_ipython().system('/Users/brian/Code/jahhills.com/hth/manage.py graph_models music news shows -o models.png  2>/dev/null')
Image('models.png')


# In[10]:

dot = get_ipython().getoutput('/Users/brian/Code/jahhills.com/hth/manage.py graph_models shows 2>/dev/null')
Source(dot.n)


# ---

# To learn more about IPython's magic functions:

# In[11]:

get_ipython().magic('quickref')


# ---

# ## Answering questions
# 
# ### How often do we play gigs?

# In[12]:

gigs = Gig.objects.published().past()
gigs.count()


# ### Where did we play last year?

# In[13]:

[gig for gig in gigs.filter(date__year='2016')]


# ### How many gigs have we played each year?

# In[14]:

for date in gigs.dates('date', 'year'):
    gig_count = gigs.filter(date__year=date.year).count()
    print('{}: {}'.format(date.year, gig_count))


# ### What venues have we played?

# In[15]:

gigs.values('venue').distinct().aggregate(count=Count('*'))


# In[16]:

from django.template import Context, Template
from IPython.display import HTML


# In[17]:

top_venues = (
    gigs.values('venue__name', 'venue__city')
    .annotate(gig__count=Count('*'))
    .order_by('-gig__count')
    [:10]
)

template = Template("""
<table>
    <tr>
        <th>Venue</th>
        <th>City</th>
        <th>Gigs</th>
    </tr>
    {% for v in venues %}
    <tr>
        <td>{{v.venue__name}}</td>
        <td>{{v.venue__city}}</td>
        <td>{{v.gig__count}}</td>
    </tr>
    {% endfor %}
</table>
""")

context = Context(
    {'venues': top_venues}
)

HTML(template.render(context))


# In[ ]:



