import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#Reading in service episodes raw csv using pandas and changing some datatypes
ser = pd.read_csv('service_episode_raw.csv')
ser[['ClientID', 'ServiceEpisodeID']] = ser[['ClientID', 'ServiceEpisodeID']].astype(str)
ser['Created At'] =  pd.to_datetime(ser['Created At'], format='%m/%d/%Y %H:%M')


#Reading in the lookup table of organizations and their county, state and zipcodes
orgs_lookup_table = pd.read_csv('orgs.csv')

#This function replaces all NaN values in a service episode raw column by looking up the organization value from orgs_lookup_table

def ser_replace_nan(col, value):
    return np.where(
        ser[col].isnull(),
        ser['Originating Organization'].map(orgs_lookup_table.set_index('OrganizationID')[value]),
        ser[col]
        )

ser['Address 1 State'] = ser_replace_nan('Address 1 State', 'State')
ser['Address 1 County'] = ser_replace_nan('Address 1 County', 'County')


#Finding and cleaning the 9-digit zipcodes. We want to truncate them to 5-digits
long_zip_codes = ser['Address 1 Postal Code'].str.len() > 5
print(ser['Address 1 Postal Code'][long_zip_codes].unique())
ser['Address 1 Postal Code'] = ser['Address 1 Postal Code'].str.slice(0, 5)

#Replacing all NaN zipcode values in service episode raw by looking up the organization zipcode from orgs_lookup_table
ser['Address 1 Postal Code'] = ser_replace_nan('Address 1 Postal Code', 'ZipCode')

#Creating new csv in project folder of cleaned service episode raw data
ser.to_csv(r'ser_cleaned.csv', index = False)

ser_cleaned = pd.read_csv('ser_cleaned.csv')

#Finding the service types with the most service episodes(aka touchpoints)
ser_cleaned_by_top_need = ser_cleaned.groupby('Service Type', as_index=False,)['ServiceEpisodeID'].nunique().sort_values(['ServiceEpisodeID'])

print(ser_cleaned_by_top_need)

#Finding which client needed the most help and had the most service episodes
print("Client ID", ser_cleaned['ClientID'].value_counts().idxmax(), "had the most service episodes.")

#Finding which day of the month had the most service episodes
print(ser_cleaned['Created At'].mode())

#Finding the number of unique clients by clientID
unique_clients = len(pd.unique(ser_cleaned['ClientID']))
print("There are", unique_clients, "unique clients.")

#Dropping duplicate ages of duplicate clients so we can perform an average formula
ser_unique_clients = ser_cleaned.drop_duplicates(subset = ['ClientID', 'Age'], keep='first')

#Calculating the average age of the unique clients
print("The average age of a client is", round(ser_unique_clients.Age.mean()), "years old.")

#Average number of touchpoints(service episodes) per unique client
unique_service_epi = len(pd.unique(ser_cleaned['ServiceEpisodeID']))
ser_per_client = round(unique_service_epi/unique_clients)
print("There are", unique_service_epi, "unique service episodes, with an average of" , ser_per_client, "service episodes per client.") 

#Percentage of clients by gender
ser_unique_genders = ser_unique_clients['Gender'].value_counts()

ser_unique_genders_male = ser_unique_genders['Male']
percent_male = round((ser_unique_genders_male/unique_clients)*100)
print((round((ser_unique_genders_male/unique_clients)*100)), "percent of the clients are male.")

ser_unique_genders_female = ser_unique_genders['Female']
percent_female = round((ser_unique_genders_female/unique_clients)*100)
print((round((ser_unique_genders_female/unique_clients)*100)), "percent of the clients are female.")

ser_unique_genders_other = unique_clients - ser_unique_genders_female - ser_unique_genders_male
percent_other = round((ser_unique_genders_other/unique_clients)*100)
print((round((ser_unique_genders_other/unique_clients)*100)), "percent of the clients are other/non-binary.")

#Percentage of clients for Jefferson County
ser_counties = ser_unique_clients['Address 1 County'].value_counts()
print((round((ser_counties['Jefferson County']/unique_clients)*100)), "percent of the clients come from Jefferson County.")

#Zipcode with the highest count of clients
ser_unique_clients = ser_unique_clients.astype({'Address 1 Postal Code': 'Int32'})
highest_zipcode = ser_unique_clients['Address 1 Postal Code'].value_counts()
print(highest_zipcode)

#Plotting the highest needs by service episode volume
plt.style.use('seaborn-pastel')
plt.figure(figsize= (12,6))
plt.barh('Service Type', 'ServiceEpisodeID', data = ser_cleaned_by_top_need)
plt.ylabel('Service Type')
plt.xlabel('Number of Service Episodes')
plt.title('Top Community Needs')
plt.tight_layout()
plt.show()

#Plotting the gender makeup of the clients
plt.style.use('seaborn-pastel')
pie_chart_data = [percent_female, percent_male, percent_other]
plt.pie(pie_chart_data, labels = ['Female', 'Male', 'Other'], autopct='%1.1f%%')
plt.show()


