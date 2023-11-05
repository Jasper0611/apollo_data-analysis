#!/usr/bin/env python
# coding: utf-8

# # Importing necessary libraries

# In[270]:


import pymysql as py
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# # Connecting to the MySQL server

# In[186]:


con= py.connect(host='3.213.221.109',user='coe_n8nuser',password='7kbn21CLh5JQ', database='domain_profiler')
cursor=con.cursor()
cursor.execute('SHOW tables')
cursor.fetchall()


# # Fetching the rows from organisation_details and Org_Profiling_Consolidated_View Tables 

# In[187]:


cursor.execute("SELECT * FROM Org_Profiling_Consolidated_View")
column_headers_contacts = [i[0] for i in cursor.description]
contacts_details=cursor.fetchall()

cursor.execute("SELECT * FROM organisation_details")
column_headers_company = [i[0] for i in cursor.description]
company_details=cursor.fetchall()


cursor.close()
con.close()


# # Reading the Company information 

# In[193]:


company_data=pd.DataFrame(company_details, columns=column_headers_company)
company_data


# # Technologies available in company Table

# In[197]:


company_chart= company_data.groupby('compatible_tech',dropna=False).size()
company_chart


# In[271]:


# Showing the technologies availble in company table by bar chart 
chart= company_chart.plot(kind='bar')

for i , j in enumerate(company_chart):
    chart.text(i, j,str(j), ha='center', va='bottom')
    
plt.xlabel('Techstack')
plt.ylabel('Count')
plt.title('Count of Techstack')
plt.figure(figsize=(10, 10))
total= (f"Total company = {len(company_data)}")
print(total)
plt.show()    


# #  Total companies available is 5303 out of which there are 2942 companies identified as not having any techstack

# # Contact profile Table

# In[194]:


profiled_data=pd.DataFrame(contacts_details, columns=column_headers_contacts)
profiled_data


# # Splitting rows with and without email id 

# In[219]:


with_email= profiled_data[profiled_data['email'].notnull()]
without_email = profiled_data[profiled_data['email'].isnull()]
with_email


# * There are 34545  rows where having email id on contacts table

# In[273]:


#Bar chart showing contacts with email and without email
x=['With Email', 'Without Email']
y=[len(with_email),len(without_email)]
for i, v in enumerate(y):
    plt.text(i, v, str(v), ha='center', va='bottom')
colors = ['skyblue', 'salmon']
plt.bar(x,y, color=colors)

plt.ylabel('Counts')
plt.title('Contact With Email Vs Contact Without Email')
print(f'Overall Data = {len(profiled_data)}')
plt.show()


# # Filtering targeted Titles from the contacts with email is available

# In[274]:


titles= ['CEO', 'General Manager', 'Owner', 'Founder', 'President',
         'Marketing','Information Technology', 'IT', 'CMO', 'CTO',
        'operation', 'COO', 'Business Development', 'Ecommerce', 'E-commerce','CIO','strategist']
filterd_titles ='|'.join(rf'\b{word}\b' for word in titles)

targeted_contacts= with_email[with_email['title'].str.contains(filterd_titles, case=False, na=False)]
targeted_contacts


# * There are 7223 contacts available from our targeted titles.

# In[275]:


no_targeted_contacts = with_email[~with_email['title'].str.contains(filterd_titles, case=False, na=False)]  # ~ used this operator to get the value for false 
no_targeted_contacts


# * There are 27,322 contacts is not our Targeted audience

# In[276]:


# Visualizing the targeted contacts and not targeted titles availabe in contact table


x=['Targeted contacts','No targeted contacts']
y=[len(targeted_contacts),len(no_targeted_contacts)]
for i, v in enumerate(y):
    plt.text(i, v, str(v), ha='center', va='bottom')
colors = ['skyblue', 'pink']
plt.bar(x,y, color=colors)

plt.ylabel('Counts')
plt.title('Our Targeted contacts Vs Other Contacts')
print(f"Total contacts = {len(with_email)}")
plt.show()


# # Checking top 20 titles which are marked as not our targeted contacts

# In[277]:


print("Examples of titles Not Targeted")
no_targeted_contacts['title'].head(20)


# # Grouping the Targeted contacts based on its Techstack before limiting 3 contacts per company

# In[278]:


targeted_contacts.groupby('compatible_tech', dropna=False).size()


# * You could see there are 32 contacts were miss-routed here eventhough its not having any techstack.

# In[279]:


# Visualizing the group of tecstack using bar chart


techchart= targeted_contacts.groupby('compatible_tech',dropna=False).size()
ax=techchart.plot(kind='bar')

for i, v in enumerate(techchart):
    ax.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel('Techstack')
plt.ylabel('Count')
plt.title('Count of Techstack')
plt.figure(figsize=(10, 10))
plt.show()


# In[280]:


# Visualizing the same with using pie cart to check its percentage

tech_pie_chart= targeted_contacts.groupby('compatible_tech', dropna=False).size().reset_index()
tech_pie_chart.columns = ['Tech', 'count']

fig = px.pie(tech_pie_chart, names='Tech', values='count', title='Distribution of Techstacks')
fig.update_traces(textinfo='percent+label', pull=[0.1] * len(tech_pie_chart))
fig.update_layout(
    showlegend=False,  # Hide the legend
    title_text='Distribution of Techstacks',  # Set the chart title
    title_x=0.5,  # Center the title
    title_y=0  
)
print('Percentage wise techstack on Targeted contacts available')
fig.show()


# # Grouping the Targeted contacts based on its Techstack after limiting 3 contacts per company

# In[295]:


limiting_targeted_contacts= targeted_contacts.groupby('domain').head(3)
number_of_unique_companies = len(limiting_targeted_contacts['domain'].unique())
before_limiting = targeted_contacts.groupby('compatible_tech', dropna=False).size()
after_limiting = limiting_targeted_contacts.groupby('compatible_tech', dropna=False).size()
print(f'''
Before Limiting the Contacts into 3 per domain
-----------------------------------------------
{before_limiting},
_________________________________________________________

After Limiting the Contacts into 3 per domain
-----------------------------------------------

{after_limiting},
'''

)


# In[359]:


#assigning df based on revenue

fivemillion_150M= limiting_targeted_contacts[(limiting_targeted_contacts['apollo_annual_revenue'] >=5000000) & (limiting_targeted_contacts['apollo_annual_revenue'] <= 150000000) ]
below5M= limiting_targeted_contacts[limiting_targeted_contacts['apollo_annual_revenue'] <5000000 ]
Above150M = limiting_targeted_contacts[limiting_targeted_contacts['apollo_annual_revenue'] > 150000000 ]


# # Visualization on contacts based on Annual Revenue

# In[372]:


below_5M_count = len(below5M)
between_5M_and_150M_count = len(fivemillion_150M)
above_150M_count = len(Above150M)

categories = ['Below 5M', '5M to 150M', 'Above 150M']
counts = [below_5M_count, between_5M_and_150M_count, above_150M_count]

colors = ['lightcoral', 'darkkhaki', 'firebrick']
plt.bar(categories, counts, color=colors)

for i, count in enumerate(counts):
    plt.text(i, count, str(count), ha='center', va='bottom')

plt.xlabel('Annual Revenue Categories')
plt.ylabel('Count')
plt.title('Distribution of Annual Revenue Categories')
plt.show()


# # Conclusion: 

# * Total company sent to Apollo API is 5303
# * Valid companies 1202 with available contacts 2958 (limited to 3 per company)
# * Invalid companies 4101.
# 
