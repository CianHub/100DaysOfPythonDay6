from collections import defaultdict, namedtuple, Counter, deque
import csv
import random
import pprint
from urllib.request import urlretrieve

County = namedtuple(
    'County', 'county population cases deaths')

counties_csv = 'data.csv'

urlretrieve(
    'http://opendata-geohive.hub.arcgis.com/datasets/4779c505c43c40da9101ce53f34bb923_0.csv?outSR={%22latestWkid%22:3857,%22wkid%22:102100}', counties_csv)

county_data = defaultdict(list)


def convert_data_to_county(data=counties_csv):

    with open(data, encoding='utf-8') as f:
        for line in csv.DictReader(f):
            try:
                county = line['CountyName']
                population = line['PopulationCensus16']
                cases = line['ConfirmedCovidCases']
                # .replace('\xa0', '')
                deaths = line['ConfirmedCovidDeaths']
            except ValueError:
                continue

            c = County(county=county, population=population,
                       cases=cases, deaths=deaths)

            county_data[county].append(c)
    return county_data


def get_cases_per_1000_people(data=convert_data_to_county()):
    count = Counter()
    for county, data in county_data.items():
        pop = int(data[0].population) / 1000
        count[county] = round(int(data[0].cases) / pop)

    return count.most_common(10)


pprint.pprint(get_cases_per_1000_people())
