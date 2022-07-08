import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

clients = pd.read_csv('clients.csv')
#Converting Client ID and Date Created to string and date time objects"
clients['ClientID'] = clients['ClientID'].astype(str)
clients['Date Created'] =  pd.to_datetime(clients['Date Created'], format='%m/%d/%Y %H:%M')

#Reading in service episodes raw
ser = pd.read_csv('service_episode_raw.csv')
ser[['ClientID', 'ServiceEpisodeID']] = ser[['ClientID', 'ServiceEpisodeID']].astype(str)
ser['Created At'] =  pd.to_datetime(ser['Created At'], format='%m/%d/%Y %H:%M')


#Reading in the lookup table of organizations and their county, state and zipcodes
orgs_lookup_table = pd.read_csv('orgs.csv')

#Replacing all NaN state values in service epi raw by looking up the organization states from lookup_table
ser['Address 1 State']=np.where(ser['Address 1 State'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').State),ser['Address 1 State'])

#Replacing all NaN county values in service epi raw by looking up the organization county from lookup_table
ser['Address 1 County']=np.where(ser['Address 1 County'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').County),ser['Address 1 County'])

#Replacing all NaN zipcode values in service epi raw by looking up the organization zipcode from lookup_table
ser['Address 1 Postal Code']=np.where(ser['Address 1 Postal Code'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').ZipCode),ser['Address 1 Postal Code'])

#Cleaning the 9-digit zipcodes. We want to truncate them to 5-digits
long_zip_codes = ser['Address 1 Postal Code'].str.len() > 5
print(ser['Address 1 Postal Code'][long_zip_codes].unique())

ser['Address 1 Postal Code'] = ser['Address 1 Postal Code'].str.slice(0, 5)


#Creating new csv in project folder of clean data
ser.to_csv(r'ser_cleaned.csv', index = False)

ser_cleaned = pd.read_csv('ser_cleaned.csv')

#Finding the service types with the most service episodes(aka touchpoints)
print(ser_cleaned['Service Type'].value_counts())

#Finding which client needed the most help
print(ser_cleaned['ClientID'].value_counts())

#Number of unique clients

unique_clients = len(pd.unique(ser_cleaned['ClientID']))
print("There are", unique_clients, "unique clients")

#Dropping duplicates ages of duplicate clients

d = ser_cleaned.drop_duplicates(subset = ['ClientID', 'Age'], keep='first')

#Calculating the average age of the unique clients

print("The average age of the clients is", round(d.Age.mean()), "years old")



