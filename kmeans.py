#!/usr/bin/python
#-*-coding:utf-8

import sys
import os
import math
import math
import logging
import pdb

'''
author : darrenan
email : ldanduo@gmail.com
created : 2014:03:10
'''

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'),\
        level = logging.INFO, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')

class KMeans:
    def __init__(self,dict_file,k):
        self.__word_dict = set()
        self.__load_word_dict(dict_file)
        self.__cluster_center = {}
        self.__k = k
        self.__init_center_class = {}
    def __load_word_dict(self, dict_file):
        ifp = file(dict_file)
        for line in ifp:
            word = line.strip()
            if not word:continue
            self.__word_dict.add(word)
        ifp.close()

    def __inc(self, d, k, v):
        if k not in d:
            d[k] = 0.0
        d[k] += v

    def __normalized(self, v):
        den = 0.0
        for k in v:
            den += v[k] * v[k]
        den = math.sqrt(den)
        for k in v:
            v[k] = v[k] / den
        return v
    def __get_vsm(self, words_list):
        v = {}
        for w in words_list:
            if w in self.__word_dict:
                self.__inc(v, w, 1.0)
        v = self.__normalized(v)
        return v

    def max_list(self, input_list):
        max_num = 0.0
        max_index = 0
        for i in range(len(input_list)):
            if input_list[i] >max_num:
                max_num = input_list[i]
                max_index = i
        return max_index

    ''' 计算每篇新闻到中心余弦的距离，
    (x1*y1 +...+ xn*yn)/(sqrt(x1*x1+..+xn*xn)*sqrt(y1*y1+...+yn*yn)) 每次已经对质心进行了归一化。而在计算一篇新闻到各个质心距离并进行比较时，
    并不需要考虑，新闻本身模的大小'''
    def __distance(self, vsm):
        result_list = [0.0] * self.__k
        for w in vsm:
            if w not in self.__cluster_center:continue
            for l in range(self.__k):
                result_list[l] += vsm[w] * self.__cluster_center[w][l]
        return self.max_list(result_list)


    '''对质心建立倒排，word:list 每行为一个词，每列为该词在质心中的得分即权重'''
    def init_center(self, center_file):
        for word in self.__word_dict:
            if word not in self.__cluster_center:
                self.__cluster_center[word] = [0.0] * self.__k

        ifp = file(center_file)
        line_count = -1
        for line in ifp:
            line = line.strip()
            if not line:continue
            line_count += 1
            if line_count>=self.__k:break
            init_center_class = line.strip().split("\t")[0]
            self.__init_center_class[line_count] = init_center_class

            words = line.strip().split("\t")[1]
            words_list = words.split(" ")
            v = self.__get_vsm(words_list)
            for w in v:
                if word in self.__cluster_center:
                    self.__cluster_center[w][line_count] = v[w]

        ifp.close()

    def __assigment(self, article_vsm):
        category = {}
        for aid in article_vsm:
            class_index = self.__distance(article_vsm[aid])
            category[aid] = class_index
        return category

    def __adjust_center(self, category, article_vsm):
        center = {}
        for word in self.__word_dict:
            if word not in center:
                center[word] = [0.0] * self.__k

        counter = {}
        for aid in article_vsm:
            c = category[aid]
            for w in article_vsm[aid]:
                center[w][c] += article_vsm[aid][w]
            self.__inc(counter,c, 1.0)
        tmp_list = [0.0] * self.__k
        for w in center:
            for c in counter:
                center[w][c] = center[w][c] / counter[c]
                tmp_list[c] += center[w][c] * center[w][c]
        tmp_list = [math.sqrt(i) for i in tmp_list]

        for w in center:
            for c in counter:
                center[w][c] = center[w][c] / tmp_list[c]

        return center

    def __center_cmp(self,center):
        ret = False
        print >>sys.stderr,"Center Diff "
        result_list = [0.0] * self.__k
        for w in self.__cluster_center:
            for i in range(self.__k):
                a = self.__cluster_center[w][i]
                b = center[w][i]
                result_list[i] += (a - b) * (a - b)
                if result_list[i] >= 0.000001:
                    ret = True
        return ret

    def cluster(self, data_file, output_file):
        ifp = file(data_file)
        article_vsm = {}
        article_id = 1
        article_label = {}

        for line in ifp:
            line = line.strip()
            if not line:continue
            lineArr = line.strip().split("\t")
            label = lineArr[0]
            words_list = lineArr[1].split(" ")
            vsm = self.__get_vsm(words_list)
            article_vsm[article_id] = vsm
            article_label[article_id] = label
            article_id += 1
        ifp.close()

        any_change = True
        itr = 1
        while any_change:
            print >> sys.stderr,"iter : %d .." % (itr)
            category = self.__assigment(article_vsm)
            cluster_center = self.__adjust_center(category, article_vsm)
            any_change = self.__center_cmp(cluster_center)
            self.__cluster_center = cluster_center
            itr += 1
        ofp = file(output_file,"w")
        for did in category:
            class_num = category[did]
            print >> ofp, "%s\t%s" % (article_label[did],self.__init_center_class[class_num])

        for w in self.__cluster_center:
            count_list = map(str,self.__cluster_center[w])
            logging.info("%s\t%s" % (w,"         ".join(count_list)))

        ofp.close()

