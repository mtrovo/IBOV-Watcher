from google.appengine.ext import db

class Stock(db.Model):
	code = db.StringProperty()
	description = db.StringProperty()
	type= db.StringProperty()
    
	def __str__(self):
		return "Stock<key: %s, code: %s, description: %s, type: %s>" % (str(self.key()), self.code, self.description, self.type)

class IbovWatcherUser(db.Model):
	user = db.UserProperty()
	watched_stocks = db.StringListProperty()
	email_interval = db.IntegerProperty()
	last_sent_email = db.DateTimeProperty()

	
def load_all_stocks_ot():
	import ot_stocks.py
	ot_stocks.main()

q = Stock.all()
if not q.fetch(1):
	load_all_stocks_ot()