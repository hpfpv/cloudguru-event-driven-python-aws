import import_csv
import pandas


def main():
    try:
        uscovid19 = import_csv.usdata()
        recovered = import_csv.recovered()

        uscovid19['date'] = pandas.to_datetime(uscovid19['date'])
        recovered['Date'] = pandas.to_datetime(recovered['Date'])

        alldata = pandas.merge(uscovid19, recovered, left_on='date', right_on='Date')
        alldata = alldata.drop('Date', axis='columns')

        return alldata
    except Exception as er:
        print(er)

if __name__ == '__main__':
    main()