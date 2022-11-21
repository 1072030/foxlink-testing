from datetime import datetime, timedelta
from app.core.database import database, FoxlinkEvent
import argparse
import asyncio
import json

async def generator(events,i):
    current_time =  datetime.now()
    start_time = datetime.strptime(events[i]['start_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    end_time = None if events[i]['end_time'] == '' else datetime.strptime(events[i]['end_time'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=8)
    if current_time >= start_time and events[i]['status'] == 'create':
        is_create = await FoxlinkEvent.objects.filter(event_id=events[i]['event_id']).exists()

        if not is_create:
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

    if end_time and current_time >= end_time and events[i]['status'] == 'update':
        event = await FoxlinkEvent.objects.filter(event_id=events[i]['event_id']).get_or_none()
        if event:
            await event.update(end_time=end_time)

async def main_routine(args):
    await database.connect()
    scenario = None
    with open( f'./app/scenario/{args.json}.json') as file:
        scenario = json.load(file)
        print(scenario)
        file.close()
    print(f"Scenario:{args.json} loaded")

    events = scenario['foxlinkEvent']
    event_number = len(events)
    print("Num events:",event_number)

    print("Start Process.")
    await  asyncio.gather(*[generator(events,i) for i in range(event_number)])
    print("Process Done.")
    await database.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='json')
    args = parser.parse_args()
    asyncio.run(main_routine(args))