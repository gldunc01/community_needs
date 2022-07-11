import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#Reading in service episodes raw
ser = pd.read_csv('service_episode_raw.csv')
ser[['ClientID', 'ServiceEpisodeID']] = ser[['ClientID', 'ServiceEpisodeID']].astype(str)
ser['Created At'] =  pd.to_datetime(ser['Created At'], format='%m/%d/%Y %H:%M')


#Reading in the lookup table of organizations and their county, state and zipcodes
orgs_lookup_table = pd.read_csv('orgs.csv')

#Replacing all NaN state values in service episode raw by looking up the organization states from orgs_lookup_table
ser['Address 1 State']=np.where(ser['Address 1 State'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').State),ser['Address 1 State'])

#Replacing all NaN county values in service episode raw by looking up the organization county from orgs_lookup_table
ser['Address 1 County']=np.where(ser['Address 1 County'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').County),ser['Address 1 County'])

#Finding and cleaning the 9-digit zipcodes. We want to truncate them to 5-digits
long_zip_codes = ser['Address 1 Postal Code'].str.len() > 5
print(ser['Address 1 Postal Code'][long_zip_codes].unique())
ser['Address 1 Postal Code'] = ser['Address 1 Postal Code'].str.slice(0, 5)

#Replacing all NaN zipcode values in service episode raw by looking up the organization zipcode from orgs_lookup_table

ser['Address 1 Postal Code']=np.where(ser['Address 1 Postal Code'].isnull(),ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID').ZipCode),ser['Address 1 Postal Code'])

#Creating new csv in project folder of cleaned service episode raw data
ser.to_csv(r'ser_cleaned.csv', index = False)

ser_cleaned = pd.read_csv('ser_cleaned.csv')

#Finding the service types with the most service episodes(aka touchpoints)
print(ser_cleaned['Service Type'].value_counts())

#Finding which client needed the most help
print(ser_cleaned['ClientID'].value_counts())

print(ser_cleaned['Created At'].value_counts())

#Finding the number of unique clients by clientID
unique_clients = len(pd.unique(ser_cleaned['ClientID']))
print("There are", unique_clients, "unique clients")

#Dropping duplicate ages of duplicate clients so we can perform an average formula
ser_unique_clients = ser_cleaned.drop_duplicates(subset = ['ClientID', 'Age'], keep='first')

#Calculating the average age of the unique clients
print("The average age of a clients is", round(ser_unique_clients.Age.mean()), "years old")

#Average number of touchpoints(service episodes) per unique client

unique_service_epi = len(pd.unique(ser_cleaned['ServiceEpisodeID']))
ser_per_client = round(unique_service_epi/unique_clients)
print("There are", unique_service_epi, "unique service episodes, with an average of" , ser_per_client, "service episodes per client") 

#Percentage of unique males
ser_unique_genders = ser_unique_clients['Gender'].value_counts()
print((round((ser_unique_genders['Male']/unique_clients)*100)), "percent of the clients are male")
print((round((ser_unique_genders['Female']/unique_clients)*100)), "percent of the clients are female. The remaining are undisclosed")

#Percentage of clients for Jefferson County
ser_counties = ser_unique_clients['Address 1 County'].value_counts()
print((round((ser_counties['Jefferson County']/unique_clients)*100)), "percent of the clients come from Jefferson County")

#Zipcode with the highest count of clients
highest_zipcode = ser_unique_clients['Address 1 Postal Code'].value_counts()
print(highest_zipcode)



