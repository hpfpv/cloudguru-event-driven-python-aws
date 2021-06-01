import boto3
from get_stream import *

def main(event, context):
    try:
        sns = boto3.resource('sns')
        topic = sns.Topic('arn:aws:sns:us-east-1:601091111123:ETLCovid19Topic')
        newItems = str(get_stream_insert(event, context))
        delItems = str(get_stream_remove(event, context))
        response = topic.publish(
            Message = 'The ETL job is completed. The table has ' + newItems + ' new items and ' + delItems + ' deleted items.' ,
            Subject = 'ETLCovid19 job status',
            MessageStructure = 'string'
        )
        print(str(response) + ' has been published!')
        return response
    except Exception as er:
        print(er)
        print('Couldnt publish message to SNS')
    
if __name__ == '__main__':
    main(event, context)
