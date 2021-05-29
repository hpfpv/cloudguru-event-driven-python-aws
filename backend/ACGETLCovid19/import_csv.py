import ssl
import pandas
ssl._create_default_https_context = ssl._create_unverified_context

def usdata():
    uscovid19 = []
    csvurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    uscovid19 = pandas.read_csv(csvurl, delimiter=',')
    #print (uscovid19)
    return uscovid19

def recovered():
    recovered = []
    recurl = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
    recovered = pandas.read_csv(recurl, delimiter=',', usecols=[0,1,4])
    recovered = recovered[recovered['Country/Region'] == 'US']
    recovered = recovered.drop('Country/Region', axis = 'columns')
    #print (recovered)
    return recovered

def main():
    try:
        usdata()
        recovered()
        return True
    except Exception as er:
        print(er)
        return False

if __name__ == '__main__':
    main()