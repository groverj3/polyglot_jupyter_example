#!/usr/bin/env python
# coding: utf-8

# # Python - Jupyter Project Environment
# ## Author: Jeffrey Grover
# ## Date: 2024-05-28
# ### Purpose:
# This notebook demonstrates an example of a python data science/bioinformatics environment living
# peacefully alongside its neighbor, an R environment, in the same project. The idea is, if you like
# either language for different tasks then you can create well-documented environments for both in a
# single repo, and use each language when you so desire.
# 
# This python example is intended to be run first.

# ### Get Some Test Data
# These commands actually run in your shell outside the notebook and the python virtualenv.

# In[1]:


# This test dataset is striaght from the pandas docs: https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html

get_ipython().system(' mkdir test_data')
get_ipython().system(' wget "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv" -P test_data')


# In[2]:


# Confirm that the test data was downloaded correctly

get_ipython().system(' ls test_data/')


# In[16]:


# Create a directory in which to place any results you wish to save
# I name these the same as the notebook file

get_ipython().system(' mkdir "polyglot_jupyter_example_py"')


# ### Load Modules

# In[3]:


# Load required modules

import pandas as pd
import seaborn as sns


# ### Load the Test Data

# In[4]:


# Load the test data from the directory we made earlier

titanic = pd.read_csv("test_data/titanic.csv")


# In[5]:


# Inspect the dataframe

titanic


# In[6]:


titanic.describe()


# ### Do Some "Analysis"
# Question: Did different classes have different survival rates?

# In[7]:


# Are there any NAs in the Survived and Pclass columns?

titanic.isnull().sum(axis = 0)


# **Result:** It looks like all the NAs are in other columns, so this shouldn't affect our "analysis."

# In[8]:


# Make a copy of the dataset for working

titanic_survival = titanic.copy()


# In[9]:


# Convert survived to boolean because it makes things clearer

titanic_survival["Survived"] = titanic_survival["Survived"].astype(bool)


# In[10]:


# We only need survived and Pclass for this analysis
# Get the count of true/false

titanic_survival = (
    titanic_survival.groupby(by="Pclass")["Survived"]
    .value_counts()
    .reset_index(name="Count")
)

titanic_survival


# In[11]:


# Add column for percent survival

titanic_survival["Percent"] = 100 * (titanic_survival["Count"] / titanic_survival.groupby("Pclass")["Count"].transform("sum")) 

titanic_survival


# **Result:** Kind of intuitive, as a proportion, more first class passengers survived.

# In[17]:


# Save the new dataframe

titanic_survival.to_csv("./polyglot_jupyter_example_py/titanic_survival.csv")


# ### Make Some Visualizations

# In[12]:


# Make a bar plot with seaborn showing surival rate by class and sex

sns.catplot(
    data=titanic,
    x="Pclass",
    y="Survived",
    hue="Sex",
    kind="bar",
).set(
    title="Titanic Survival Rate",
    xlabel="Passenger Class"
)


# **Result:** Exactly what we showed above but with a visual.

# In[13]:


# Plot the fare by class and Age

sns.relplot(
    data=titanic,
    x="Age",
    y="Fare",
    hue="Pclass"
)


# **Result:** Fares for 2nd and third classes were more consistent, while first class varies.

# In[14]:


# To look at the distribution of prices it will help to have class be a str

titanic["Pclass"] = titanic["Pclass"].astype(str)

titanic["Pclass"]


# In[18]:


# Combination violin and swarmplot, right from the seaborn docs: https://seaborn.pydata.org/generated/seaborn.catplot.html

sns.catplot(data=titanic, x="Age", y="Pclass", kind="violin", color=".9", inner=None)
sns.swarmplot(data=titanic, x="Age", y="Pclass", size=3)


# ### Conclusion
# 
# Jupyter installed at the global/user-level can be made to create notebooks and connect to an ipythonkernel installed in a virtualenv.

# ### Documenting the Environment
# 
# Outside the notebook a new requirements.txt was generated:
# 
# 1. Enter the directory of your project, where the notebooks live.
# 2. `pyenv activate polyglot_jupyter_example` (If your virtualenv isn't already active in your shell)
# 3. `pip freeze` > requirements.txt
# 4. You can now safely `pyenv deactivate` if you wish
# 5. The "requirements.txt" will then be tracked in the github repo and can be used to reconstruct the environment with `pip install -r requirements.txt` in the future.

# In[3]:


# I also export the notebook as a .py script so it can be run without jupyter and .html so non-coders can view it
# These can be run outside of the notebook, as long as you have nbconvert installed in your local python version

get_ipython().system(' jupyter nbconvert --to script --output-dir ./polyglot_jupyter_example_py/ polyglot_jupyter_example_py.ipynb')
get_ipython().system(' jupyter nbconvert --to html --output-dir ./polyglot_jupyter_example_py/ polyglot_jupyter_example_py.ipynb')


# ### Cleaning-up
# 
# Outside the virtualenv you can:
# 1. `jupyter kernelspec list` - To get the installed kernels and identify the one used in this project.
# 2. `jupyter kernelspec remove polyglot_jupyter_example` - Remove the virtualenv from the list of kernels.
# 3. Keep the virtualenv kernel installed if you intend to use more ipython kernel-based notebooks in this project.
