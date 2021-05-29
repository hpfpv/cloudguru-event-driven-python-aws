import boto3
from botocore.credentials import JSONFileCache
from botocore.exceptions import ClientError

import json
import import_csv
import transformation

event = []
context = []

data = transformation.main()
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ACGETLCovid19')
stream = boto3.client('dynamodbstreams')

def append_data(dataframe, dynamotable):
    try:
        dynamocount = int(dynamotable.scan(Select = 'COUNT')['Count'])
        datacount = int(len(dataframe.index)) 
        for row in range(dynamocount, datacount):
            date = str(dataframe.loc[row, 'date'])
            cases = str(dataframe.loc[row, 'cases'])
            deaths = str(dataframe.loc[row, 'deaths'])
            Recovered = str(dataframe.loc[row, 'Recovered'])
            #print('date: ' + date + '       deaths:' + deaths)
            #check = dynamotable.get_item(
             #           Key={
              #              'date': date
               #         }
                #    )
            #if (check['Item']['date'] != date):
            dynamotable.put_item(
                    Item={
                        'date': date,
                        'cases': cases,
                        'deaths': deaths,
                        'Recovered': Recovered
                    }
                )       
        dynamotable.scan()
        print ('DynamoDB table updated successfully')
        finalcount = dynamotable.scan(Select = 'COUNT')['Count'] 
        response = finalcount - dynamocount
        return response
    except Exception as er:
        print(er)

def initial_load(dataframe, dynamotable):
    try:
        datacount = int(len(dataframe.index)) 
        for row in range(0, datacount):
            date = str(dataframe.loc[row, 'date'])
            cases = str(dataframe.loc[row, 'cases'])
            deaths = str(dataframe.loc[row, 'deaths'])
            Recovered = str(dataframe.loc[row, 'Recovered'])
            dynamotable.put_item(
                Item={
                    'date': date,
                    'cases': cases,
                    'deaths': deaths,
                    'Recovered': Recovered
                }
            )
        print ('First load of Items completed successfully')
        finalcount = dynamotable.scan(Select = 'COUNT')['Count'] 
        response = finalcount 
        return response
    except Exception as er:
        print(er)

def load_data(dataframe, dynamotable):
    print('---------------------')
    print('Begining data Laod')
    print('---------------------')
    dynamocount = int(dynamotable.scan(Select = 'COUNT')['Count'])
    datacount = int(len(dataframe.index))
    count = datacount - dynamocount
    print('Items in DynamoDB table: ' + str(dynamocount))
    print('Items in dataframe: ' + str(datacount))
    if dynamocount == 0:
        print('Table first load of items')
        response = initial_load(dataframe, dynamotable)
        print( str(response) + ' ITEMS CREATED')
    elif dynamocount == datacount:
        print('NO NEW ITEMS')
    elif dynamocount != datacount:
        print('Appending table with new items')
        response = append_data(dataframe, dynamotable)
        print( str(response) + ' ITEMS ADDED')
    print('---------------------')
    print ('Data load completed')
    print('---------------------')
    
    
def main(event, context):
    try:
        load_data(data, table)
        return True
    except Exception as er:
        print(er)
        return False

if __name__ == '__main__':
    main(event, context)