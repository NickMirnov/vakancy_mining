# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'nickses245'
#import csv
def read_files():
    job_dict = {}
    for pols in open('vakancy_from_yandex.txt'):
        unit = pols.rstrip()
        jobs = []
        for gst in open('gost_job_names.csv'):
            gst = gst.rstrip()
            splits = gst.split('\t')
            if unit in splits[2]:
                resume_str = '{0}\t{1}'.format(splits[2], splits[-1])
                jobs.append(resume_str)
        job_dict[unit] = jobs
    return job_dict


def counter(lst):
    ls = [int(l.split('\t')[1][:1]) for l in lst]
    count_result = [ls.count(num) for num in range(1, 10)]
    group_number = count_result.index(max(count_result)) + 1
    return group_number


def filter_group(job_dict):
    import time
    from vakancy import Vakancy
    vakancy_data_lst = []
    for key in job_dict:
        if job_dict[key]:
            target_lst = job_dict[key]
            number_group = counter(target_lst)
            vakancy = Vakancy(vakancy_name=key, super_group=number_group)
            vakancy_data_lst.append(vakancy)
    return vakancy_data_lst

if __name__ == '__main__':
    open('out_test.csv', 'w')
    job_dict = read_files()
    vak_lst = filter_group(job_dict)
    for vakancy in vak_lst:
        url = vakancy.build_url()
        urlst, job = vakancy.first_scrappy(url)
        result = vakancy.other_scrappy(urlst)
