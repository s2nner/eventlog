"""
read csv as dict and obj
support usecols=(0, 4)

csv
1997,Ford,E350,"ac, abs, moon",3000.00
1999,Chevy,"Venture ""Extended Edition"","",4900.00
1996,Jeep,Grand Cherokee,"MUST SELL! air, moon roof, loaded",4799.00

vs = get_csv(filename, names=('f1', 'f2'), usecols=(0, 4))
result
{'f1': '1997', 'f2': '3000.00'}
{'f1': '1999', 'f2': '4900.00'}
{'f1': '1996', 'f2': '4799.00'}

example
https://stackoverflow.com/a/37768961/2677704
a.petrov
s2nner@gmail.com
"""
from typing import Union
import csv


class RowObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)


async def get_csv(file_name, *,
                  names=None,
                  usecols=None,
                  mode='r',
                  encoding="utf8",
                  quoting=csv.QUOTE_ALL,
                  delimiter=',',
                  as_obj=False) -> Union[dict, tuple, RowObject]:
    with open(file_name, mode=mode, encoding=encoding) as csvfile:
        data_reader = csv.reader(csvfile, quoting=quoting, delimiter=delimiter)
        for row in data_reader:
            if usecols and names:
                q = dict(zip(names, (row[i] for i in usecols)))
                yield q if not as_obj else RowObject(**q)
            elif usecols and not names:
                yield list(row[i] for i in usecols)
            elif names and not usecols:
                q = dict(zip(names, (row[i] if i < len(row) else None for i, _ in enumerate(names))))
                yield q if not as_obj else RowObject(**q)
            else:
                yield row
