# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = 'nickses245'

class Vakancy:

    def __init__(self, super_group=None, group=None, sub_group=None, vakancy_name=None):
        """



        :rtype : object
        :type self:vakancy_obj
        :param super_group:
        :param group:
        :param sub_group:
        :param vakancy_name:
        """
        self.super_group = super_group
        self.group = group
        self.sub_group = sub_group
        self.vakancy_name = vakancy_name


    def build_url(self):
        """

        :param vakancy: string
        :param rid: int
        :return: hh_coding url with rid
        """
        import urllib
        from parse_tools import rid_choice

        vakancy_hh_encode = urllib.quote(self.vakancy_name.rstrip())
        rid = rid_choice()
        url = r'http://rabota.yandex.ru/salary.xml?text={0}&rid={1}'.format(vakancy_hh_encode, rid)
        self.url = url
        return self.url


    def first_scrappy(self, url):

        """

        :type self: object
        """
        import urllib
        import lxml.html
        import re
        import urlparse
        import datetime
        import random
        import time
        import parse_tools
        #====test print ===== url
        print('test url in firstscrap = ', url)
        delay = random.uniform(random.uniform(1, 2), random.uniform(3, 4))
        w_time = datetime.datetime.now()
        numb_pattern = re.compile('\d+')
        page = urllib.urlopen(url)
        doc = lxml.html.document_fromstring(page.read())
        if parse_tools.check_vakancy(doc, self.vakancy_name):
            print('test i am in true check_vakancy')
            sal_head = doc.cssselect('div.b-salary-header__body .b-link')
            hrf = sal_head[0].get('href')
            vol_selection_str = sal_head[0].text
            volume_of_selection = numb_pattern.match(vol_selection_str)
            how_many_pages = parse_tools.pages_counter(str(volume_of_selection.group()))
            salary_tag = doc.cssselect('div.b-salary-header__body .b-salary-value')
            salary_average_str = salary_tag[0].text
            salar = ''.join(numb_pattern.findall(salary_average_str))
            query = urlparse.urlparse(hrf).query
            params = urlparse.parse_qs(query)
            job = params['text'][0]
            self.job = job
            volume = volume_of_selection.group()
            self.volume = volume
            print('self.volume is: ', self.volume)
            self.url_steps = ['http://rabota.yandex.ru/search.xml/?text={0}&rid=213&page_num={1}'.format(job, num) for num in range(1, how_many_pages)]
            time.sleep(delay)
         #   for url in self.url_steps:
               # print('url in steps:\t', url)
            return self.url_steps, self.job
        else:
            self.url_steps = []
            self.job = ''
            return self.url_steps, self.job

    def other_scrappy(self, urlst):
        """

        :rtype : object
        """
        import parse_tools
        print('i im in other scrapp')
        result_lst = []
        #print('result_lst',result_lst)
        count = 0 
        for url in urlst:
            count+=1
            str1 = parse_tools.other_steps(url,self.super_group,
                    self.vakancy_name)
            print(str1, sep='\t', file=open('out_all_pool.csv', 'a'))
            print(self.super_group, self.vakancy_name,'processing...',\
                   count, 'pages', sep='\t')
            result_lst.append(str1)
        self.result_lst = result_lst
        return self.result_lst
    
def simple_mining():

    """
    in : vakancy_pool-file
    out: csv-file with salaries
    """
    for ttl_vakancy  in open('vakancy_from_yandex.txt'):
        vakancy = Vakancy(vakancy_name = ttl_vakancy)
        url = vakancy.build_url()
        urlst, job = vakancy.first_scrappy(url)
       # print(10*'*\n',urlst)
       # for ur in urlst:
       #     print('urlst in testing:')
        result = vakancy.other_scrappy(urlst)
       # print(vakancy.super_group, vakancy.group, vakancy.sub_group,
       #         vakancy.vakancy_name, vakancy.url, vakancy.job,
       #         ''.join(vakancy.result_lst), sep='\t', file=open('out_all_pool.csv', 'a'))
        print(vakancy.super_group, vakancy.group, vakancy.sub_group, vakancy.vakancy_name, vakancy.url, vakancy.job, ''.join(vakancy.result_lst))
if __name__ == '__main__':
    simple_mining()

#==========case  full mining, with using classificator's codes=============
#    from in_handle import create_vakancy_dict
#   gen_dic_vakancies = create_vakancy_dict()
#   for sup_key in gen_dic_vakancies:
#       for gr_key in gen_dic_vakancies[sup_key]:
#           for sub_gr_key in gen_dic_vakancies[sup_key][gr_key]:
#               for vakancy_name in gen_dic_vakancies[sup_key][gr_key][sub_gr_key]:
#                   vakancy = Vakancy(sup_key, gr_key, sub_gr_key, vakancy_name)
#                   url = vakancy.build_url()
#                   urlst, job = vakancy.first_scrappy(url)
#                   result = vakancy.other_scrappy(urlst)
#                   print(vakancy.super_group, vakancy.group, vakancy.sub_group, vakancy.vakancy_name, vakancy.url, vakancy.job, ''.join(vakancy.result_lst), sep='\t', file=open('out_test.csv', 'a'))
 #                  print(vakancy.super_group, vakancy.group, vakancy.sub_group, vakancy.vakancy_name, vakancy.url, vakancy.job, ''.join(vakancy.result_lst))

#===========end tests full salary mining=====================
    #stolar = Vakancy(vakancy_name='xxxxxxx')
    #url = stolar.build_url()
    #urlst, job = stolar.first_scrappy(url)
    #result = stolar.other_scrappy(urlst)
    #print(result)
