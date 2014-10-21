# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = 'nickses245'


class VakancyPool:
    def __init__(self):
        """


        :rtype : url_str
        :type source_url:  str
        """
        self.fields_dic = {}
        source = 'http://rabota.yandex.ru/'
        self.source_url = source
        self.fool_pool = []

    def fields_scrappy(self):
        """
        get lst with vakancy_fields
        
        :rtype : dict
        """
        import urllib
        import lxml.html

        page = urllib.urlopen(self.source_url)
        doc = lxml.html.document_fromstring(page.read())
        field_info = doc.cssselect('a.b-popular__link')
        for field in field_info:
            if 'job_industry' in field.get('href'):
                field_url = self.source_url + field.get('href')
                self.fields_dic[field.text] = field_url
        return self.fields_dic

    def get_pool(self, names_lst):
        """

        :type names_lst: list
        """
        self.fool_pool += names_lst


class JobNamesFromPool:
    def __init__(self, industry, url):
        """


        :type url: str
        :param industry string
        :param url: url-string
        """
        self.industry = industry
        self.url = url

    def scrap_jobs(self):
        """


        """
        import urllib
        import lxml.html

        page = urllib.urlopen(self.url)
        doc = lxml.html.document_fromstring(page.read())
        vakancies = doc.cssselect('a.b-popular__link')
        self.vakancy_names = [vakancy.text for vakancy in vakancies]
        return self.vakancy_names


if __name__ == '__main__':
    import time
    import random

    if not open('vakancy_from_yandex.txt'):
        delay = random.uniform(random.uniform(1, 2), random.uniform(3, 4))
        page = VakancyPool()
        fields = page.fields_scrappy()
        for field in fields.keys():
            job_name = JobNamesFromPool(field, fields[field])
            name_lists = job_name.scrap_jobs()
            page.get_pool(name_lists)
            #print(field, fields[field])
            time.sleep(delay)
            print('field is:\t', field, '\t len of sub_pool:\t', len(name_lists), '\t sleep:\t', delay)
