import ETLCovid19
event = []
context = []

def test_ETLCovid19():
    assert ETLCovid19.main(event, context)
    print('Test ETLCovid19 OK')
