import json
import time
import logging
import argparse
import asyncio
import signal
from datetime import datetime, timedelta
from app.services.database import database, FoxlinkEvent,DATABASE_URI

async def generator(event,speed):
    current_time =  datetime.now() - timedelta(hours=8)
    start_time = datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    end_time = None if event['end_time'] == '' else datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    if event['status'] == 'create':
        await asyncio.sleep(float(max((start_time - current_time).total_seconds(),0))/speed) 
        await FoxlinkEvent.objects.create(
            project=event['project'],
            line=str(int(event['line'])),
            device_name=event['device_name'],
            category=event['category'],
            start_time=start_time,
            end_time=end_time,
            message=event['message'],
            start_file_name='',
            end_file_name='',
            event_id=event['event_id']
        )

    if end_time and event['status'] == 'update':
        event = await FoxlinkEvent.objects.filter(event_id=event['event_id']).get_or_none()
        if event:
            await asyncio.sleep(float(max((end_time - current_time).total_seconds(),0))/speed) 
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
                        generator(events[i],args.speed)
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
    parser.add_argument("-n",dest="speed",type=int,default=1)
    args, unknown = parser.parse_known_args()
    asyncio.run(driver(args))
    
if __name__ == "__main__":
    entry_point()
   