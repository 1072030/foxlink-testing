import json, asyncio, time
from datetime import datetime, timedelta
from app.env import CURRENT_PATH, SCENARIO
from app.core.database import database, FoxlinkEvent

filename = f'{CURRENT_PATH}/app/scenario/{SCENARIO}'

async def main_routine():
    await database.connect()

    with open(filename) as file:
        scenario = json.load(file)
        file.close()

    i = 0
    events = scenario['foxlinkEvent']
    event_number = len(events)

    while True:
        i = 0
        while True:
            if i == event_number :
                break

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

            i += 1

        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main_routine())
    loop.run_forever()