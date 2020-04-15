# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from functools import reduce

from gluon.packages.dal.pydal.restapi import Policy, RestAPI


def index():

    # there will be dragons!!!
    # there is a ¿bug? making "list" type of fields hidden in search, so we need to write a whole new widget
    # for including it, because nobody thought about including the search_options parameter in the grid call
    search_options = {
        'string': ['=', '!=', '<', '>', '<=', '>=', 'starts with', 'contains', 'in', 'not in'],
        'text': ['=', '!=', '<', '>', '<=', '>=', 'starts with', 'contains', 'in', 'not in'],
        'date': ['=', '!=', '<', '>', '<=', '>='],
        'time': ['=', '!=', '<', '>', '<=', '>='],
        'datetime': ['=', '!=', '<', '>', '<=', '>='],
        'integer': ['=', '!=', '<', '>', '<=', '>=', 'in', 'not in'],
        'double': ['=', '!=', '<', '>', '<=', '>='],
        'id': ['=', '!=', '<', '>', '<=', '>=', 'in', 'not in'],
        'reference': ['=', '!='],
        'boolean': ['=', '!='],
        'list:string': ['contains'],
    }
    keywords = ''
    if 'keywords' in request.post_vars:
        keywords = request.post_vars.keywords
    elif 'keywords' in request.get_vars:
        keywords = request.get_vars.keywords
    formname = 'web2py_grid'
    tables = [db.casos]
    sfields = reduce(lambda a, b: a + b,
                     [[f for f in t if f.readable and f.searchable] for t in tables])
    advanced_search = True
    prefix = formname == 'web2py_grid' and 'w2p' or 'w2p_%s' % formname
    search_menu = SQLFORM.search_menu(sfields, search_options=search_options, prefix=prefix)
    spanel_id = '%s_query_fields' % prefix
    sfields_id = '%s_query_panel' % prefix
    skeywords_id = '%s_keywords' % prefix
    hidden_fields = [INPUT(_type='hidden', _value=v, _name=k) for k, v in request.get_vars.items() if
                     k not in ['keywords', 'page']]
    search_widget = lambda sfield, url: CAT(FORM(
        INPUT(_name='keywords', _value=keywords,
              _id=skeywords_id, _class='form-control',
              _onfocus="jQuery('#%s').change();jQuery('#%s').slideDown();" % (
              spanel_id, sfields_id) if advanced_search else ''
              ),
        INPUT(_type='submit', _value=T('Search'), _class="btn btn-default btn-secondary"),
        INPUT(_type='submit', _value=T('Clear'), _class="btn btn-default btn-secondary",
              _onclick="jQuery('#%s').val('');" % skeywords_id),
        *hidden_fields,
        _method="GET", _action=url), search_menu)
    # end of madness, we are not in Sparta

    grid = SQLFORM.grid(db.casos, user_signature=False, search_widget=search_widget)
    return dict(grid=grid)

def api():
    # response.generic_patterns.append('json')
    # response.generic_patterns.append('xml')

    policy = Policy()
    policy.set('casos', 'GET', authorize=True, allowed_patterns=['*'])
    # policy.set('*', 'GET', authorize=True, allowed_patterns=['*'])
    # policy.set('*', 'PUT', authorize=False)
    # policy.set('*', 'POST', authorize=False)
    # policy.set('*', 'DELETE', authorize=False)

    return response.json(RestAPI(db, policy)(request.method, request.args(0), request.args(1),
                                  request.get_vars, request.post_vars))

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
