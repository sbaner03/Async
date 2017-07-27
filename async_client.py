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
        postfetch = (mid-start).total_seconds()
        total = (end-start).total_seconds()
        for html in htmls:
            print (html)
        print (postfetch,total)


checklist = pickle.load( open( "checklist.pkl", "rb" ) )
checklist = list(pd.unique(checklist))[0:20]
jsondata = [json.dumps({'con': '10000','origin': i[0], 'destination': i[1],'location': i[0],'arratloc': '2017-07-08 17:30:00'}) for i in checklist]
websites = [['http://48f2c246.ngrok.io/',jsondata[ix]] for ix,i in enumerate(checklist)]
loop = asyncio.get_event_loop()
loop.run_until_complete(main(websites))
