import json
import time
import logging
import argparse
import asyncio
import signal
from datetime import datetime, timedelta
from app.services.database import database, FoxlinkEvent,DATABASE_URI

async def generator(events,i):
    current_time =  datetime.now() - timedelta(hours=8)
    start_time = datetime.strptime(events[i]['start_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    end_time = None if events[i]['end_time'] == '' else datetime.strptime(events[i]['end_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    if events[i]['status'] == 'create':
        await asyncio.sleep(max((start_time - current_time).total_seconds(),0)) 
        await FoxlinkEvent.objects.create(
            project=events[i]['project'],
            line=str(int(events[i]['line'])),
            device_name=events[i]['device_name'],
            category=events[i]['category'],
            start_time=start_time,
            end_time=end_time,
            message=events[i]['message'],
            start_file_name='',
            end_file_name='',
            event_id=events[i]['event_id']
        )

    if end_time and events[i]['status'] == 'update':
        event = FoxlinkEvent.objects.filter(event_id=events[i]['event_id']).get_or_none()
        if event:
            await asyncio.sleep(max((end_time - current_time).total_seconds(),0)) 
            await event.update(end_time=end_time)



async def driver(args):
    print(DATABASE_URI)
    await database.connect()
    with open( f'./app/scenario/{args.json}.json') as file:
        
        scenario = json.load(file)

        print(f"Scenario:{args.json} loaded")
        
        events = scenario['foxlinkEvent']
        event_number = len(events)
        
        print(f"Num events: {event_number}")

        print("StaRt ProCesS....")

        await asyncio.gather(
                    *[
                        generator(events,i)
                        for i in range(event_number)
                    ]
        )
        # while True:
        #     try:
               
        #     except:
        #         logging.error("exception occured!! retry to run all the events...")
        #         continue
        #     else: 
        #         break

        print("FoXliNk EveNt ImPorT Done....")
    await database.disconnect()

def entry_point():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='json')
    args = parser.parse_args()
    asyncio.run(driver(args))
    
if __name__ == "__main__":
    entry_point()
   