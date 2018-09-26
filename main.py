import argparse
import asyncio

from csv_reader import get_csv
from helpers import percentile
from request import Request
from writer import print_global_stats, print_group_request_stats

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='path to input.txt', default='input.txt')
args = parser.parse_args()


async def main(file: str) -> None:
    ids_requests_time: dict = {}
    ids_errors: list = []
    requests: dict = {}

    csv_coro = get_csv(file, names=('time', 'id_request', 'event_type', 'gr', 'args'), as_obj=True, delimiter='\t')
    async for d in csv_coro:
        if d.event_type == 'BackendError':
            ids_errors.append(d.id_request)

        if d.event_type == 'StartRequest':
            ids_requests_time[d.id_request] = int(d.time)
            requests[d.id_request] = Request(d)
        elif d.event_type == 'FinishRequest':
            ids_requests_time[d.id_request] = int(d.time) - ids_requests_time[d.id_request]
            request = requests[d.id_request]
            request.finish(d)
        else:
            request = requests[d.id_request]
            request.process(d)

    max_request_time = max(ids_requests_time, key=ids_requests_time.get)
    requests_max_time = sorted(ids_requests_time, key=ids_requests_time.get, reverse=True)[:10]

    pure_percentile = percentile([ids_requests_time.get(max_request_time)], 0.95)
    # numpy_percentile = np.percentile(np.array([ids_requests_time.get(max_request_time)]), 95)

    errors = len(ids_errors)

    print_global_stats(pure_percentile, requests_max_time, errors)
    print_group_request_stats(requests)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(args.file))
loop.close()
