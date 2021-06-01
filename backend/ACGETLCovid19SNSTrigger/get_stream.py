def get_stream_insert(event, context):
    try:
        new_rows_count = 0
        for record in event ['Records']:
            if record['eventName'] == 'INSERT':
                new_rows_count += 1
        return new_rows_count
    except Exception as er:
        print(er)

def get_stream_remove(event, context):
    try:
        del_rows_count = 0
        for record in event ['Records']:
            if record['eventName'] == 'REMOVE':
                del_rows_count += 1
        return del_rows_count
    except Exception as er:
        print(er)
