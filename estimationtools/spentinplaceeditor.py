# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2010 Joachim Hoessler <hoessler@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.

from trac.core import implements
from trac.web.api import IRequestFilter, IRequestHandler
from trac.web.chrome import ITemplateProvider, add_script

from estimationtools.utils import EstimationToolsBase


class SpentInPlaceEditor(EstimationToolsBase):
    """A filter to implement in-place editing for spent hours field in
    query page.

    Requires Trac XML-RPC Plug-in.
    """

    implements(IRequestFilter, IRequestHandler, ITemplateProvider)

    # IRequestHandler methods

    def match_request(self, req):
        return req.path_info == '/estimationtools/editspent.js'

    def process_request(self, req):
        data = {'field': self.spent_field}
        return 'editspent.html', {'data': data}, 'text/javascript'

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        try:
            realm = data['context'].resource.realm
        except:
            realm = None
        if realm in ('query', 'report', 'wiki', 'milestone', 'roadmap') \
                and 'preview' not in req.args \
                and 'TICKET_MODIFY' in req.perm \
                and 'XML_RPC' in req.perm:
            add_script(req, 'estimationtools/jquery.jeditable.mini.js')
            add_script(req, '/estimationtools/editspent.js')
        return template, data, content_type

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('estimationtools', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]
