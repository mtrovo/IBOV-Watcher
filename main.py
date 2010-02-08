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
import logging
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
    size_str = self.request.get('size')
    if not size_str or size_str == '':
      size_str = '20'
    page_size = int(size_str)
    
    stocks = None
    if last_str and '' != last_str:
      logging.info("last_str: %s" % last_str)
      last_key = db.Key(last_str)
      query = models.Stock.gql('WHERE __key__ > :1 ORDER BY __key__', last_key)
      stocks = query.fetch(page_size)
    elif first_str and '' != first_str:
      logging.info("first_str: %s" % first_str)
      first_key = db.Key(first_str)
      query = models.Stock.gql('WHERE __key__ < :1 ORDER BY __key__ DESC', first_key)
      stocks = query.fetch(page_size)
      stocks.reverse()
      logging.info("len(stocks): %s" % len(stocks))
      if not stocks: stocks = models.Stock.gql('ORDER BY __key__').fetch(page_size)
    else:
      logging.info("fetching without offset")
      stocks = query.fetch(page_size)
      
    if not stocks: stocks = []
    args['stocks'] = stocks
    args['render_next_link'] = len(stocks) == page_size
    args['size'] = page_size
    if len(stocks) == page_size: args['last'] = str(stocks[page_size - 1].key())
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
