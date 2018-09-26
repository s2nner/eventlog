import logging
import sys

from jinja2 import Template

from templates import print_global, group_request

targets = logging.StreamHandler(sys.stdout), logging.FileHandler('output.txt')
logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)


def print_global_stats(percentile: int, long_req: list, bad_req: int) -> None:
    global_stats = Template(print_global)
    logging.info(global_stats.render(p=percentile, r=long_req, gr=bad_req))


def print_group_request_stats(requests: dict) -> None:
    template = Template(group_request)
    logging.info('Обращения и ошибки по бекендам')
    for id, request in requests.items():
        logging.info(template.render(id=id, gr=request.group_requests))
