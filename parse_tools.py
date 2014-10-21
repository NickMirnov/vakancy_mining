#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = 'nick'


def create_joblist():
    """

    :rtype :  dict
    in: jobs-vakancy; city

    :return:# [[code,job,url_percent_encode]]
    """
    import sys
    import urllib
    import csv

    geo_list = open('city.txt').readlines()
    rid_dict = {}
    invite = '\nМосква\nСанкт-Петербург\nНовосибирск\nЕкатеринбург\
    \nНижний Новгород\nКазань\nСамара\nОмск\nЧелябинск\nРостов-на-Дону\
    \nУфа\nВолгоград\nКрасноярск\nПермь\nВоронеж\n'
    #   print invite
    try:
        input_info = sys.argv[1]
    except IndexError:
        input_info = 'Москва'

    print('raw_inp:\t', input_info)

    for rid in geo_list:
        rid = rid.split('\t')
        rid_dict[rid[0]] = rid[1]

    while input_info not in rid_dict.keys():
        print('Неверный ввод города. Попробуйте еще раз из списка:\n{0}'.format(invite))
        input_info = raw_input()

    rid = rid_dict[input_info]

    #    rid = sys.argv[1]
    joblist = []
    for row in csv.reader(open('indatajobs.csv', 'r'), delimiter='\t'):
        if len(row[0]) <= 2:
            row[1] = 'group :: ' + row[1]
            joblist.append([row[0], row[1]])
            print(row[0], row[1])
        elif len(row[0]) == 3:
            row[1] = 'subgroup :: ' + row[1]
            joblist.append([row[0], row[1]])
            print(row[0], row[1])
        else:
            job_hh_encode = urllib.quote(row[1].strip())
            url = r'http://rabota.yandex.ru/salary.xml?text={0}&rid={1}'.format(job_hh_encode, rid)
            joblist.append([row[0], row[1], url])
            print(row[0], row[1], url)
    return joblist


def check_logs():
    """


    :return: list with logs
    """
    import csv
    log_l = []
    for row in csv.reader(open('out_test.csv', 'r'), delimiter='\t'):
        try:
            if row[4]:
                log_l.append(row[4])
                print(row[4])
        except:
            continue
    print('log::::', log_l)
    return log_l


def rid_choice():
    """
    :return: int rid
    """
    import sys
    try:
        geo_list = open('city.txt').readlines()
        rid_dict = {}
        invite = '\nМосква\nСанкт-Петербург\nНовосибирск\nЕкатеринбург\
    \nНижний Новгород\nКазань\nСамара\nОмск\nЧелябинск\nРостов-на-Дону\
    \nУфа\nВолгоград\nКрасноярск\nПермь\nВоронеж\n'
    #   print invite

        #input_info = sys.argv[1]

        input_info = 'Москва'

        #print('raw_inp:\t', input_info)

        for rid in geo_list:
            rid = rid.split('\t')
            rid_dict[rid[0]] = rid[1]

        while input_info not in rid_dict.keys():
            print('Неверный ввод города. Попробуйте еще раз из списка:\n{0}'.format(invite))
            input_info = raw_input()

        rid = rid_dict[input_info]
        return rid
    except:
        #print('FILE WITH SITIES IS NOT OPEN, RID IS DEFAULT')
        rid = '213'
        return rid


def build_url(vakancy):
    """

    :param vakancy: string
    :param rid: int
    :return: hh_coding url with rid
    """
    import urllib

    vakancy_hh_encode = urllib.quote(vakancy.rstrip())
    rid = rid_choice()
    url = r'http://rabota.yandex.ru/salary.xml?text={0}&rid={1}'.format(vakancy_hh_encode, rid)
    return url


def compar_vakancy_titles(vakancy, lst):
    # if match_job --> next job
    #print('LST',lst)
    if lst:
        for log in lst:
            if log in vakancy:
                print('this request for vakancy[{0}] already processed'.format(vakancy))
                return True
    else:
        return False


def first_page_iteration(vakancy_name):

    """

    :type vakancy_name: object
    """
    import urllib
    import lxml.html
    import re
    import urlparse
    import datetime
    import random
    import time

    delay = random.uniform(random.uniform(1, 2), random.uniform(3, 4))
    url1 = build_url(vakancy_name)
    #print(vakancy_name, url1)
    w_time = datetime.datetime.now()
    numb_pattern = re.compile('\d+')
    #url1 = 'http://rabota.yandex.ru/salary.xml?text=%D1%85%D0%B8%D0%BC%D0%B8%D0%BA%0A&rid=213'
    #print('url1', url1)
    #    url1 = "http://rabota.yandex.ru/salary.xml?text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80"
    page = urllib.urlopen(url1)
    doc = lxml.html.document_fromstring(page.read())
    if check_vakancy(doc, vakancy_name):
        sal_head = doc.cssselect('div.b-salary-header__body .b-link')
        hrf = sal_head[0].get('href')
        vol_selection_str = sal_head[0].text
        volume_of_selection = numb_pattern.match(vol_selection_str)
        #print type(volume_of_selection.group())
        how_many_pages = pages_counter(str(volume_of_selection.group()))
        salary_tag = doc.cssselect('div.b-salary-header__body .b-salary-value')
        salary_average_str = salary_tag[0].text
        salar = ''.join(numb_pattern.findall(salary_average_str))
        query = urlparse.urlparse(hrf).query
        params = urlparse.parse_qs(query)
        job = params['text'][0]
        volume = volume_of_selection.group()
        #out_str1 = out_str + '{0}\t{1}\t{2}\t{3}'.format(job, salar, volume, url1.strip())
        #print(out_str, file=open('out_test.csv', 'a'))
        #print(out_str)
        print('', '', '', '', vakancy_name, job, url1, salar, volume_of_selection.group(), sep='\t')
        print(w_time.strftime('%d.%m.%y %H %M'), vakancy_name, job, url1, salar, volume_of_selection.group(), sep='\t')
        url_steps = ['http://rabota.yandex.ru/search.xml/?text={0}&rid=213&page_num={1}'.format(job, num) for num in
                 range(1, how_many_pages)]
        time.sleep(delay)
        return url_steps, job
    else:
        url_steps = []
        time.sleep(delay)
        return url_steps, vakancy_name

def check_vakancy(html_document, vakancy_name):
    notice = html_document.cssselect('div.b-hint.b-hint_type_notice')
    if notice:
        print("{0} : no vakancy".format(vakancy_name))
        return False
    else:
        print("{0} : vakancy YES".format(vakancy_name))
        return True


def pages_counter(volume):
    import math

    pgs = int(math.ceil(int(volume) / 10))
    if pgs >= 100:
        pgs = 101
    else:
        pgs += 1
    return pgs


def other_steps(url, group_num='groop : ', base_job_name='None'):
    """

    :rtype : None
    """
    import urllib
    import lxml.html
    import time
    import random
    import re

    delay = random.uniform(random.uniform(1, 2), random.uniform(3, 4))
    page = urllib.urlopen(url)
    doc = lxml.html.document_fromstring(page.read())
    l_page = doc.cssselect('div.l-page__left .b-serp-item')
    pattern = re.compile('\d')
    outlst = []
    for serp in l_page:
        #print type(serp)
        salary_lst = serp.cssselect('div.b-serp-item__left .b-salary__value')
        title_lst = serp.cssselect('div.b-serp-item__right .b-serp-item__title a')
        company = serp.cssselect('div.b-serp-item__right .b-serp-item__company')
        find = serp.find_class('i-clearfix')
        company_title = company[0].text_content()[11:]
        title_vakancy = title_lst[0].text_content()
        source_vakancy = title_lst[0].get('href')
        salary_str = salary_lst[0].text_content()
        salary = re.sub(" ", '', salary_str.encode('utf-8'))
        if ' – ' in salary:
            split_sal = salary.split(' – ')
            sal = (float(split_sal[1]) + float(split_sal[0])) / 2
            if sal > 11000:
                salary = int(sal)
                #print('interval_sal \t {0}'.format(salary))
        elif 'от' in salary:
            sal = 1.25 * float(''.join(pattern.findall(salary)))
            if sal > 11000:
                salary = int(sal)
                #print('ot \t {0}'.format(salary))
        elif 'до' in salary:
            sal = 0.75 * float(''.join(pattern.findall(salary)))
            if sal > 11000:
                salary = int(sal)
                #print('do \t {0}'.format(salary))
        elif 'не указана' in salary:
            continue
            #salary = re.sub('з/п не указана', 'None', salary)
            #print('не указана: \t {0}'.format(salary))
        else:
            if int(salary) > 11000:
                salary = salary
        requirements = find[1].text_content()[10:]
        responsibility = find[2].text_content()[11:]
        terms_and_geo = find[3].text_content()[7:]
        outstr = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format( 
        title_vakancy.encode('utf-8'), 
        source_vakancy.encode('utf-8'), 
        salary, company_title.encode('utf-8'), 
        requirements.encode('utf-8'), responsibility.encode('utf-8'),
        terms_and_geo.encode('utf-8'))
        #print(outstr2, file=open('out_test.csv', 'a'))
        #print(outstr2)
        #date = find[4].text_contents()[]
        #print(responsibility)
        #print(find[4].text_content())
        outlst.append(outstr)
    time.sleep(delay)
    outstr1 = ''.join(outlst)
    return outstr1

if __name__ == '__main__':
    vakancy = 'менеджер'
    url_steps, vakancy_name = first_page_iteration(vakancy)
    for url in url_steps:
        outstr = other_steps(url)
        print(outstr)
