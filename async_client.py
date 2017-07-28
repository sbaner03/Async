import aiohttp
import asyncio
import async_timeout
from datetime import datetime
import pickle
import pandas as pd
import json



async def fetch(session, url,data):
    with async_timeout.timeout(0):
        async with session.get(url, data = data) as response:
            return await response.text()

async def main(websites):
    async with aiohttp.ClientSession() as session:
        start = datetime.now()
        htmls = [await fetch(session, html[0],html[1]) for html in websites]
        mid = datetime.now()
        end = datetime.now()
        total = (end-start).total_seconds()
        return (total,len(htmls))


checklist = pickle.load( open( "checklist.pkl", "rb" ) )
checklist = list(pd.unique(checklist))[0:5]
jsondata = [json.dumps({'con': '10000','origin': i[0], 'destination': i[1],'location': i[0],'arratloc': '2017-07-08 17:30:00'}) for i in checklist]
websites = [['http://localhost:50000/',jsondata[ix]] for ix,i in enumerate(checklist)]
loop = asyncio.get_event_loop()
stats = loop.run_until_complete(main(websites))
output = open('stats.pkl', 'wb')
pickle.dump(stats, output)
output.close()
print (stats)
