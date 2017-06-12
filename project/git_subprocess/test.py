#-*-coding:utf-8-*-
__author__ = 'csy'

import os, re
from bs4 import BeautifulSoup
from urllib2 import urlopen
from project.git_subprocess import Repository

# my_repo = Repository("E:/csyrepo/repo")
# # my_repo.clone_from("git@git.emao.net:ops-group/TestAutomation.git")
# os.chdir("E:/csyrepo/repo")
# # my_repo.add_file('E:/csyrepo/repo/Page/config.ini')
# # my_repo.commit('csy<chenshiyang460@emao.com>', 'Sample Commit Message')
# # my_repo.push('master')
#
# my_repo.get_branches("E:/csyrepo/repo")f
#
#
# my_repo.checkout('dealer')
#
# my_repo.get_branches("E:/csyrepo/repo")

bsObj = BeautifulSoup(urlopen('http://www.xicidaili.com', 'html.parser'))
ipList = bsObj.findAll('td', text=re.compile('[0-9]+(?:\.[0-9]+){3}'))
for each in ipList:
    ip = each.get_text()
    # port = each.next_sibling.next_sibling.get_text() 因为换行的原因要取两次兄弟节点
    port = each.parent.find('td', text=re.compile('^\d{2,5}$')).get_text()
    # 测试中遇到5位端口号，遂将{2,4}改为{2,5}
    proxy = ip + ':' +port