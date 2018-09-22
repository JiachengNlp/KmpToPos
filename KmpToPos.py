# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:21:35 2018

@author: DONG
"""

import pandas as pd

def get_Start_Index(s,p):
    '''
    :param s: 原始字符串
    :param p: 需要匹配的字符串
    :return: 返回的匹配位置开始索引列表
    '''
    n = len(s)
    m = len(p)
    next_list = getNextList(p)
    start = []
    j = 0
    for i in range(n):
        while s[i] != p[j] and j > 0:
            j = next_list[j] 
        if s[i] == p[j]:
            j += 1
            if j == m:
                start.append(i-m+1)
                j = next_list[j]
    return start
  
def getNextList(strs): 
    n = len(strs)
    alist = [0,0]
    k = 0 
    for i in range(1,n): 
        while strs[i] != strs[k] and k != 0:
            k = alist[k] 
        if strs[i] == strs[k]:
            k += 1
        if strs[i] == strs[alist[i]]:   
            alist[i] = alist[alist[i]]
        alist.append(k) 
    return alist

def TL_ORG_POS(Sentence_data,list_ORG_append):
  '''
  :param Sentence_data: 每个句子列表
  :param list_ORG_append: 句子包含实体列表
  :return: 输出转换为BIO标签字典列表
  '''
  sentence_len = []
  all_tag = []
  for ORG_index,ORG_v in enumerate(list_ORG_append):
    if ORG_index == 0:
      for index, value in enumerate(Sentence_data):
        char_tag = dict()
        last_list =[]
        if list_ORG_append[ORG_index][index] == list_ORG_append[ORG_index][index]:
          start_list = get_Start_Index(value,list_ORG_append[ORG_index][index])
          for index_s,count in enumerate(start_list):
            last_list.append(count + len(list_ORG_append[ORG_index][index])-1)
            char_tag[count] = "B-ORG"
            x = count+1
            while(x <=last_list[index_s]):
              char_tag[x] = "I-ORG"
              x +=1
        all_tag.append(char_tag)
      for sentence in Sentence_data:
        sentence_len.append(len(sentence))
      for k ,v in enumerate(all_tag):
        for i in range(sentence_len[k]):
          if i not in all_tag[k].keys():
            all_tag[k][i] = "O"
    else:
      for index, value in enumerate(Sentence_data):
        last_list =[]
        if list_tag_append[ORG_index][index] == list_ORG_append[ORG_index][index]:
          start_list = get_Start_Index(value,list_ORG_append[ORG_index][index])
          for index_s,count in enumerate(start_list):
            last_list.append(count + len(list_ORG_append[ORG_index][index])-1)
            all_tag[index][count] = "B-ORG"
            x = count+1
            while(x <=last_list[index_s]):
              all_tag[index][x] = "I-ORG"
              x +=1
  return all_tag

  
if __name__ == '__main__':      
    data_str = pd.read_csv("data/NER_Sentence.csv")
    Sentence_data = data_str["﻿Sentence"]
    tag1 = data_str["ORG1"]
    tag2 = data_str["ORG2"]
    tag3 = data_str["ORG3"]
    tag4 = data_str["ORG4"]
    tag5 = data_str["ORG5"]
    list_tag_append =[]
    list_tag_append.append(list(tag1))
    list_tag_append.append(list(tag2))
    list_tag_append.append(list(tag3))
    list_tag_append.append(list(tag4))    
    list_tag_append.append(list(tag5))    
    all_tag = TL_ORG_POS(Sentence_data,list_tag_append)

    out_file = open("output/output.txt", 'a',encoding = "utf-8")
    for key,doc in enumerate(Sentence_data):
      if key > 0:
        out_file.write("\n")
        out_file.flush()
      for index,char in enumerate(doc):
        tag = all_tag[key][index]
        out_file.write("%s %s\n"  % (char,tag))
        out_file.flush()
          
      
      
      
      
      