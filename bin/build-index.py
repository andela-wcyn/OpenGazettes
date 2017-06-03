#!/bin/env python
import json
import os
from collections import defaultdict, Counter
from itertools import chain


# jurisdiction -> year -> [gazettes]
jurisdictions = json.load(open('_data/jurisdictions.json'))
failed_gazettes = '_data/failed_gazettes.json'
success_gazettes = '_data/gazettes.json'


def write_year(juri, year, gazettes):
    juri_info = jurisdictions[juri]
    title = juri_info["name"]
    title = title + " Gazettes"

    with open('_gazettes/%s/%s.md' % (juri, year), 'w') as f:
        f.write("---\n")
        f.write("layout: year\n")
        f.write("title: %s %s\n" % (title, year))
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % juri_info["name"])
        f.write('year: "%s"\n' % year)
        f.write("---\n")


def write_jurisdiction(juri, years):
    path = '_gazettes/%s' % juri
    try:
        os.makedirs(path)
    except OSError:
        pass

    with open('%s/index.md' % path, 'w') as f:
        juri_info = jurisdictions[juri]
        title = juri_info["name"]
        title = title + " Gazettes"

        f.write("---\n")
        f.write("layout: jurisdiction\n")
        f.write("title: %s\n" % title)
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % juri_info["name"])
        f.write("---\n")

    for year in years.iterkeys():
        write_year(juri, year, years[year])


def build(gazettes, gazette, stats, juri):
    year = gazette['publication_date'].split('-')[0]
    iyear = int(year)
    if 'archive_url' not in gazette:
        gazette['archive_url'] = 'https://s3-eu-west-1.amazonaws.com/' \
                                 'cfa-opengazettes-ke/gazettes/' + \
                                 gazette['files'][0]['path']

    gazettes[juri]['gazettes'][year].append(gazette)
    gazettes[juri]['years'].add(year)

    stats['count'] += 1
    stats['earliest_year'] = min([stats['earliest_year'], iyear])
    stats['latest_year'] = max([stats['latest_year'], iyear])
    # for jekyll, years in keys should be strings
    stats['years'][year] += 1


def build_options(gazettes, juri, stats, failed):
    for line in open('data.jsonlines'):
        gazette = json.loads(line)

        # Don't include gazette if it has an error
        if failed:
            try:
                if gazette.get('files')[0]['has_error']:
                    build(gazettes, gazette, stats, juri)
            except KeyError:
                # If "has_error" not set, assume gazette is okay
                pass
            continue

        try:
            if gazette.get('files')[0]['has_error']:
                continue
        except KeyError:
            # If "has_error" not set, assume gazette is okay
            pass
        build(gazettes, gazette, stats, juri)

    return (stats, gazettes)


def build_index(gazette_file, failed=False):
    gazettes = {}
    for juri, info in jurisdictions.iteritems():
        name = info["name"]
        gazettes[juri] = {
            'name': name,
            'years': set(),
            'gazettes': defaultdict(list),
            'search_collection': info["search_collection"],
        }

    stats = {
        'count': 0,
        'earliest_year': 9999,
        'latest_year': 0,
        'years': defaultdict(int),
        'counts': {},
    }

    stats, gazettes = build_options(gazettes, juri, stats, failed)
    for juri in gazettes.iterkeys():
        write_jurisdiction(juri, gazettes[juri]['gazettes'])

    # sort gazettes by date, then title
    for code, juris in gazettes.iteritems():
        juris['years'] = sorted(list(juris['years']))
        for items in juris['gazettes'].itervalues():
            items.sort(key=lambda g: [g['publication_date'][:7],
                                      g['gazette_volume'],
                                      g['gazette_number'],
                                      g['gazette_title']])

        items = list(chain(*juris['gazettes'].itervalues()))

        # count by year
        years = Counter(g['publication_date'].split("-")[0] for g in items)
        if not years:
            continue

        # ensure values for all years
        min_year = min(int(i) for i in years.iterkeys())
        max_year = max(int(i) for i in years.iterkeys())
        for year in xrange(min_year, max_year + 1):
            years.update({str(year): 0})

        # count by year and month
        year_months = Counter(tuple(g['publication_date'].split("-")[0:2])
                              for g in items)

        # ensure values for contiguous years and months
        for year in xrange(min_year, max_year + 1):
            for m in xrange(1, 13):
                year_months.update({(str(year), '%02d' % m): 0})

        # make year_months nested
        year_months_nested = {}
        for (y, m), v in year_months.iteritems():
            year_months_nested.setdefault(y, {})[m] = v

        stats['counts'][code] = {
            'available': {
                'year': years,
                'year_month': year_months_nested,
            }
        }

    gazettes['stats'] = stats

    with open(gazette_file, 'w') as f:
        json.dump(gazettes, f, sort_keys=True)


if __name__ == '__main__':
    build_index(success_gazettes, failed=False)
    build_index(failed_gazettes, failed=True)
