#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import models


class MainHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    args = {}
    self.response.out.write(template.render(path, args))

class StockHandler(webapp.RequestHandler):
  def get(self):
    args = {}
    
    query = models.Stock.gql('ORDER BY __key__')
    last_str = self.request.get('last')
    first_str = self.request.get('first')
    stocks = None
    if last_str and '' != last_str:
      last_key = db.Key(last_str)
      query = models.Stock.gql('WHERE __key__ > :1 ORDER BY __key__', last_key)
      stocks = query.fetch(20)
    elif first_str and '' != first_str:
      first_key = db.Key(first_str)
      query = models.Stock.gql('WHERE __key__ < :1 ORDER BY __key__', first_key)
      stocks = query.fetch(20).reverse()
      #if not stocks: stocks = models.Stock.gql('ORDER BY __key__').fetch(20)
    else:
      stocks = query.fetch(20)
      
    if not stocks: stocks = []
    args['stocks'] = stocks
    if len(stocks) == 20: args['last'] = str(stocks[19].key())
    if len(stocks) >= 1: args['first'] = str(stocks[0].key())
    
    path = os.path.join(os.path.dirname(__file__), 'stocks.html')
    self.response.out.write(template.render(path, args))

def main():
  configs = []
  configs.append(('/', MainHandler))
  configs.append(('/stocks', StockHandler))
  application = webapp.WSGIApplication(configs,
      debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
