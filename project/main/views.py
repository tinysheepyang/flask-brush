# project/main/views.py
# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, redirect, url_for, g, current_app
from flask.ext.login import login_required
from flask import request, flash, jsonify
from project import app, db
from project.models import IP_log, Case
from flask_paginate import Pagination, get_page_args
import MySQLdb
from datetime import datetime

import datetime
import sys;
reload(sys);
sys.setdefaultencoding("utf8")


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
@login_required
def home():
    return render_template('main/index.html')


@main_blueprint.route('/reports/auto', methods=['GET', 'POST'])
@login_required
def reports():

    searchtime = request.args.get('searchtime')
    starttime,endtime = search_time(searchtime)
    starttime = starttime.split("'")[1]
    endtime = endtime.split("'")[1]
    search_days = []
    click_days = []
    searchdict = {'name':'serch'}
    clickdict = {'name':'click'}
    days = []
    if searchtime is not None:
        sea = db.func.date_format(IP_log.created_at, "%Y-%m-%d").label('search')
        search = db.session.query(sea, db.func.count(IP_log.click)).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == 0)).group_by('search').all()
        cli = db.func.date_format(IP_log.created_at, "%Y-%m-%d").label('search')
        click = db.session.query(cli, db.func.count(IP_log.click)).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == 1)).group_by('search').all()
    else:
        sea = db.func.date_format(IP_log.created_at, "%Y-%m-%d").label('search')
        search = db.session.query(sea, db.func.count(IP_log.click)).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == 0)).group_by('search').all()
        cli = db.func.date_format(IP_log.created_at, "%Y-%m-%d").label('search')
        click = db.session.query(cli, db.func.count(IP_log.click)).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == 1)).group_by('search').all()
    if len(search) == 0 or len(click) == 0:
        starttime,endtime = create_time(starttime,endtime)
        for i in range((endtime-starttime).days+1):
            day = starttime + datetime.timedelta(days=i)
            day = unicode(str(day),'utf-8')
            if len(search) == 0:
                search.append([day,0])
            else:
                click.append([day,0])
    for search_day, click_day in zip(search,click):
        search_day = list(search_day)
        search_day[0] = search_day[0].encode("utf-8")
        search_day[1] = int(search_day[1])
        click_day = list(click_day)
        click_day[0] = click_day[0].encode("utf-8")
        click_day[1] = int(click_day[1])
        search_days.append(search_day)
        click_days.append(click_day)

    searchdict['data'] = search_days
    clickdict['data'] = click_days
    days.extend([searchdict,clickdict])
    return render_template('/main/auto.html', data=days)


@main_blueprint.route('/reports/detail', defaults={'page':1}, methods=['GET', 'POST'])
@main_blueprint.route('/reports/detail/page/<int:page>/')
@main_blueprint.route('/reports/detail/page/<int:page>')
@login_required
def detail(page):
    # usertype = request.args.getlist('usertype')
    KEYWORD = request.args.get('keyword')
    ip = request.args.get('ip')
    searchtype = request.args.get('searchtype')
    searchtime = request.args.get('searchtime')

    starttime,endtime = search_time(searchtime)
    page, per_page, offset = get_page_args()

    print isinstance(ip, unicode)
    if searchtime is not None and isinstance(ip, unicode):
        starttime = starttime.split("'")[1]
        endtime = endtime.split("'")[1]
        total = db.session.query(IP_log).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.keyword.like('%' + KEYWORD + '%'))).count()
        users = db.session.query(IP_log).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.keyword.like('%' + KEYWORD + '%'))).limit(per_page).offset(offset).all()

    elif searchtime is not None and searchtype != 'none':
        starttime = starttime.split("'")[1]
        endtime = endtime.split("'")[1]
        total = db.session.query(IP_log).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.keyword.like('%' + KEYWORD + '%'), IP_log.click == searchtype)).count()
        users = db.session.query(IP_log).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.keyword.like('%' + KEYWORD + '%'), IP_log.click == searchtype)).limit(per_page).offset(offset).all()

    elif (not isinstance(ip, unicode) and ip != None):
        total = db.session.query(IP_log).filter(IP_log.ip == ip).count()
        users = db.session.query(IP_log).filter(IP_log.ip == ip).limit(per_page).offset(offset).all()

    else:
        total = db.session.query(IP_log).count()
        # users = db.session.query(IP_log).order_by(db.desc(IP_log.created_at)).limit(per_page).offset(offset).all()
        users = db.session.query(IP_log).order_by(db.desc(IP_log.created_at)).limit(per_page).offset(offset).all()

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='iplog',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('/main/detail.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@main_blueprint.route('/reports/count', defaults={'page':1}, methods=['GET', 'POST'])
@main_blueprint.route('/reports/count/page/<int:page>/')
@main_blueprint.route('/reports/count/page/<int:page>')
@login_required
def count(page):
    # usertype = request.args.getlist('usertype')
    searchtype = request.args.get('searchtype')
    searchtime = request.args.get('searchtime')
    starttime,endtime = search_time(searchtime)

    page, per_page, offset = get_page_args()
    if searchtime is not None and searchtype != 'none':
        starttime = starttime.split("'")[1]
        endtime = endtime.split("'")[1]
        total = db.session.query(db.func.count('*'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == searchtype)).group_by(IP_log.keyword).count()
        users = db.session.query(db.func.count('*').label('count'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime), IP_log.click == searchtype)).group_by(IP_log.keyword).limit(per_page).offset(offset).all()
    elif searchtime is not None:
        starttime = starttime.split("'")[1]
        endtime = endtime.split("'")[1]
        total = db.session.query(db.func.count('*').label('count'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime))).group_by(IP_log.keyword).count()
        users = db.session.query(db.func.count('*').label('count'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime))).group_by(IP_log.keyword).limit(per_page).offset(offset).all()
    else:
        starttime = starttime.split("'")[1]
        endtime = endtime.split("'")[1]
        total = db.session.query(db.func.count('*').label('count'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime))).group_by(IP_log.keyword).count()
        users = db.session.query(db.func.count('*').label('count'), IP_log.keyword).filter(db.and_(IP_log.created_at.between(starttime, endtime))).group_by(IP_log.keyword).limit(per_page).offset(offset).all()

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='iplog',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('/main/count.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@main_blueprint.route('/reports/localauto/', methods=['GET', 'POST'])
@login_required
def localreports():
    searchtime = request.args.get('searchtime')
    starttime,endtime = search_time(searchtime)
    search_days = []
    click_days = []
    searchdict = {'name':'serch'}
    clickdict = {'name':'click'}
    day = []
    if searchtime is not None:
        g.cur.execute('select DATE_FORMAT(f.created_at, "%Y-%m-%d") days,count(f.click) from ip_log f where f.created_at between {} and {} and f.click = 0 group by days'.format(starttime,endtime))
        search = g.cur.fetchall()
        g.cur.execute('select DATE_FORMAT(f.created_at, "%Y-%m-%d") days,count(f.click) from ip_log f where f.created_at between {} and {} and f.click = 1 group by days'.format(starttime,endtime))
        click = g.cur.fetchall()
    else:
        g.cur.execute('select DATE_FORMAT(f.created_at, "%Y-%m-%d") days,count(f.click) from ip_log f where f.created_at between {} and {} and f.click = 0 group by days'.format(starttime,endtime))
        search = g.cur.fetchall()
        g.cur.execute('select DATE_FORMAT(f.created_at, "%Y-%m-%d") days,count(f.click) from ip_log f where f.created_at between {} and {} and f.click = 1 group by days'.format(starttime,endtime))
        click = g.cur.fetchall()

    if len(search) == 0 or len(click) == 0:
        starttime,endtime = create_time(starttime,endtime)
        for i in range((endtime-starttime).days+1):
            day = starttime + datetime.timedelta(days=i)
            day = unicode(str(day),'utf-8')
            if len(search) == 0:
                search.append([day,0])
            else:
                click.append([day,0])

    for search_day, click_day in zip(search,click):
        search_day = list(search_day)
        search_day[0] = search_day[0].encode("utf-8")
        search_day[1] = int(search_day[1])

        click_day = list(click_day)
        click_day[0] = click_day[0].encode("utf-8")
        click_day[1] = int(click_day[1])

        search_days.append(search_day)
        click_days.append(click_day)

    searchdict['data'] = search_days
    clickdict['data'] = click_days
    day.extend([searchdict,clickdict])
    return render_template('/main/localauto.html', data=day)


@main_blueprint.route('/reports/localdetail', defaults={'page':1}, methods=['GET', 'POST'])
@main_blueprint.route('/reports/localdetail/page/<int:page>/')
@main_blueprint.route('/reports/localdetail/page/<int:page>')
@login_required
def localdetail(page):
    # usertype = request.args.getlist('usertype')
    KEYWORD = request.args.get('keyword')
    ip = request.args.get('ip')
    searchtype = request.args.get('searchtype')
    searchtime = request.args.get('searchtime')

    print 'searchtime--->[%s],KEYWORD--->[%s],searchtype--->[%s],ip--->[%s]' % (searchtime,KEYWORD,searchtype,type(ip)),ip
    starttime,endtime = search_time(searchtime)

    KEYWORD = "'" + "%" + str(KEYWORD) + "%" + "'"

    page, per_page, offset = get_page_args()
    print per_page,offset
    if searchtime is not None and not isinstance(ip,int):
        g.cur.execute('select count(*) from ip_log where ip_log.created_at between {} and {} and ip_log.keyword like {}'.format(starttime,endtime,KEYWORD))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from ip_log where ip_log.created_at between {} and {} and ip_log.keyword like {} order by ip_log.created_at limit {}, {}'.format(starttime,endtime,KEYWORD,offset, per_page))
        users = g.cur.fetchall()
    elif searchtime is not None and searchtype != 'none':
        g.cur.execute('select count(*) from ip_log where ip_log.created_at between {} and {} and ip_log.click = {} and ip_log.keyword like {}'.format(starttime,endtime,searchtype,KEYWORD))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from ip_log where ip_log.created_at between {} and {} and ip_log.click = {} and ip_log.keyword like {} order by ip_log.created_at limit {}, {}'.format(starttime,endtime,searchtype,KEYWORD,offset, per_page))
        users = g.cur.fetchall()
    elif isinstance(ip,int):
        ip = "'" + str(ip) + "'"
        g.cur.execute('select count(*) from ip_log where ip_log.ip = {}'.format(ip))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from ip_log where ip_log.ip = {} order by ip_log.created_at limit {}, {}'.format(ip,offset, per_page))
        users = g.cur.fetchall()
    elif searchtime is not None:
        g.cur.execute('select count(*) from ip_log where ip_log.created_at between {} and {} '.format(starttime,endtime))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from ip_log where ip_log.created_at between {} and {} order by ip_log.created_at limit {}, {}'.format(starttime,endtime,offset, per_page))
        users = g.cur.fetchall()
    else:
        g.cur.execute('select count(*) from ip_log')
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from ip_log order by ip_log.created_at limit {}, {}'.format(offset, per_page))
        users = g.cur.fetchall()

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='iplog',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('/main/localdetail.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@main_blueprint.route('/reports/localcount', defaults={'page':1}, methods=['GET', 'POST'])
@main_blueprint.route('/reports/localcount/page/<int:page>/')
@main_blueprint.route('/reports/localcount/page/<int:page>')
@login_required
def localcount(page):
    # usertype = request.args.getlist('usertype')
    searchtype = request.args.get('searchtype')
    searchtime = request.args.get('searchtime')
    starttime,endtime = search_time(searchtime)
    page, per_page, offset = get_page_args()

    if (searchtime is not None and searchtype != 'none'):
        g.cur.execute('select count(t.keyword) from (select count(*),keyword  from ip_log where ip_log.created_at between {} and {} and ip_log.click = {} group by keyword) t'.format(starttime,endtime,searchtype))
        total = g.cur.fetchone()[0]
        g.cur.execute('select count(*),keyword from ip_log where ip_log.created_at between {} and {} and ip_log.click = {} group by keyword limit {}, {}'.format(starttime,endtime,searchtype,offset, per_page))
        users = g.cur.fetchall()

    elif searchtime is not None:
        g.cur.execute( 'select count(t.keyword) from (select count(*),keyword  from ip_log where ip_log.created_at between {} and {} group by keyword) t'.format(starttime,endtime))
        total = g.cur.fetchone()[0]
        g.cur.execute('select count(*),keyword from ip_log where ip_log.created_at between {} and {} group by keyword limit {}, {}'.format(starttime,endtime,offset, per_page))
        users = g.cur.fetchall()
    else:
        g.cur.execute('select count(t.keyword) from (select count(*),keyword  from ip_log where ip_log.created_at between {} and {} group by keyword) t'.format(starttime,endtime))
        total = g.cur.fetchone()[0]
        g.cur.execute('select count(*),keyword from ip_log where ip_log.created_at between {} and {}  group by keyword limit {}, {}'.format(starttime,endtime,offset, per_page))
        users = g.cur.fetchall()

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='iplog',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('/main/localcount.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@main_blueprint.route('/brush/insert', methods=['GET', 'POST'])
@login_required
def brush():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        url = request.form.get('url')
        btn = request.form.get('button')
        print 'keywoed--->[%s],url--->[%s],btn--->[%s]' % (keyword,url,btn)

        if btn == 'insert':
            if keyword == None or url == None or keyword == '' or url == '':
                flash('搜索词或者URL为空！', 'danger')
                return render_template('/main/brush.html')
            else:
                # case = Case(
                #         info=keyword,
                #         url=url,
                #         create_time=datetime.datetime.now()
                # )
                # db.session.add(case)
                # db.session.commit()
                # db.session.close()
                try:
                    g.cur.execute("insert into Cases(info, url, created_time) VALUES('%s', '%s', '%s')" % (keyword, url, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    flash('添加成功！', 'success')
                except Exception as e:
                    print '数据库操作异常',e
                    g.conn.rollback()
                    flash("添加失败", 'danger')

        else:
            # db.session.query(Case).filter(Case.url == url).delete()
            # db.session.commit()
            # db.session.close()
            g.cur.execute("delete from Cases where url = '%s'" % url)
            flash('删除成功！', 'success')
    return render_template('/main/brush.html')

@main_blueprint.route('/brush/search', methods=['GET', 'POST'])
@login_required
def brushsearch():
    KEYWORD = request.args.get('keyword')
    searchtime = request.args.get('searchtime')
    ID = request.values.get('delete')
    print 'ID',ID
    if ID is not None:
        ID = int(ID)
    KEYWORD = "'" + "%" + str(KEYWORD) + "%" + "'"
    starttime,endtime = search_time(searchtime)
    page, per_page, offset = get_page_args()

    if searchtime is not None:
        g.cur.execute('select count(*) from Cases where created_time between {} and {}'.format(starttime,endtime))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from Cases where created_time between {} and {} limit {}, {}'.format(starttime,endtime,offset,per_page))
        users = g.cur.fetchall()

    elif searchtime is not None and KEYWORD !='%%':
        g.cur.execute('select count(*) from Cases where created_time between {} and {} and info like {}'.format(starttime,endtime,KEYWORD))
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from Cases where created_time between {} and {} and info like {} limit {}, {}'.format(starttime,endtime,KEYWORD,offset,per_page))
        users = g.cur.fetchall()

    elif isinstance(ID, int):
        g.cur.execute('delete from Cases where id = %s' % ID)
        g.cur.execute('select count(*) from Cases')
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from Cases order by created_time desc  limit {}, {}'.format(offset,per_page))
        users = g.cur.fetchall()

    else:
        # total = db.session.query(Case).count()
        # users = db.session.query(Case).order_by(db.desc(Case.created_time)).limit(per_page).offset(offset).all()
        g.cur.execute('select count(*) from Cases')
        total = g.cur.fetchone()[0]
        g.cur.execute('select * from Cases order by created_time desc  limit {}, {}'.format(offset,per_page))
        users = g.cur.fetchall()

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='case',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('/main/brushsearch.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)

def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )

@main_blueprint.before_request
def before_request():
    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        g.conn = MySQLdb.connect(host='101.201.117.71', user='root', passwd='yimaoqiche', port=3306, charset='utf8')
        g.cur = g.conn.cursor()  # 获取一个游标对象
        g.cur.execute("USE brush")
    except Exception as e:
        print("连接数据库发生异常 %s" % e)


@main_blueprint.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        g.cur.close()  # 关闭游标
        g.conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
        g.conn.close()  # 关闭到数据库的连接，释放数据库资源

def search_time(searchtime):
    if searchtime is not None and '—' in searchtime:
        starttime = searchtime.split('—')[0] + ' '+ '00:00:00'
        endtime = searchtime.split('—')[1] + ' '+ '23:59:59'
        starttime = "'" + starttime + "'"
        endtime = "'" + endtime + "'"
        return  starttime,endtime
    elif searchtime is not None and '一' in searchtime:
        starttime = searchtime.split('一')[0] + ' '+ '00:00:00'
        endtime = searchtime.split('一')[1] + ' '+ '23:59:59'
        starttime = "'" + starttime + "'"
        endtime = "'" + endtime + "'"
        return  starttime,endtime
    else:
        endtime = datetime.date.today()
        starttime = (endtime - datetime.timedelta(days=1))
        endtime = "'" + str(endtime) + ' '+ '23:59:59' + "'"
        starttime = "'" + str(starttime) + ' '+ '00:00:00' + "'"
        return  starttime,endtime

def create_time(starttime,endtime):
    if '-' in starttime:
         y = int(starttime.split(' ')[0].split('-')[0])
         m = int(starttime.split(' ')[0].split('-')[1])
         d = int(starttime.split(' ')[0].split('-')[2])

         starttime = datetime.date(y, m, d)

         Y = int(endtime.split(' ')[0].split('-')[0])
         M = int(endtime.split(' ')[0].split('-')[1])
         D = int(endtime.split(' ')[0].split('-')[2])
         endtime = datetime.date(Y, M, D)
    else:
        y = int(starttime.split(' ')[0].split('/')[0])
        m = int(starttime.split(' ')[0].split('/')[1])
        d = int(starttime.split(' ')[0].split('/')[2])

        starttime = datetime.date(y, m, d)

        Y = int(endtime.split(' ')[0].split('/')[0])
        M = int(endtime.split(' ')[0].split('/')[1])
        D = int(endtime.split(' ')[0].split('/')[2])
        endtime = datetime.date(Y, M, D)

    return starttime,endtime
