
# coding: utf-8

# # Introducing the Jupyter Notebook

# ## What is it?
# 
# From [jupyter.org](http://jupyter.org/):
# 
# > An open-source web application that allows you to create and share documents that contain live code, equations, visualizations and explanatory text. 
# 
# The "document", aka "notebook", is composed of Code and Markdown cells, which you interact with using Command and Edit mode.

# ## Command mode
# 
# - Show keyboard shortcuts: `h`
# - Move up and down: `j`/`Down` and `k`/`Up`
# - Insert cell above or below: `a` or `b`
# - Run cell: `Shift`+`Enter`
# - Save: `S`
# - Switch to Edit mode: `Enter`

# ## Markdown cells
# 
# We're already using these!

# ## Code cells
# 
# Similar to running Python from the command line, but each one is a mini-editor with syntax highlighting, auto-indent, and more.
# 
# * Autocomplete: `Tab` 
# * Help: `Shift`+`Tab` (repeat for more)
# * Run cell: `Shift`+`Enter`
# * Switch to Command mode: `Esc`

# In[1]:

hello = 'Hello, {}!'
who = input('Who? ')
hello.format(who)


# In[ ]:




# ## IPython?

# [IPython](http://ipython.org/) is a powerful replacement for the standard Python shell, which spawned the IPython Notebook. Eventually, the developers extracted the language-independent features of notebook web application to create the Jupyter Notebook.  This "Big Split" occurred almost 2 years ago, but you'll still find lots of references to IPython in documentation and examples.
# 
# - IPython still serves as the backend (aka "[kernel](http://jupyter.readthedocs.io/en/latest/projects/kernels.html)") for running Python code in the Notebook
# - "Jupyter" is an amalgamation of "Julia", "Python", and "R", which were the most popular languages used with the Notebook.
# 
# 

# ## Getting started with Django
# 
# [Django Extensions](https://django-extensions.readthedocs.io/en/latest/shell_plus.html) makes this easy. From within your virtual environment:
# 
# ```
# (venv)$ pip install django-extensions jupyter
# (venv)$ cd /path/to/notebooks
# (venv)$ /path/to/manage.py shell_plus --notebook
# ```
# 
# __NOTE__: There's a [known issue](https://github.com/django-extensions/django-extensions/issues/1026) with this method for users who want to use the notebook with multiple Django projects. Hopefully there will be a fix or a documented alternative soon.
