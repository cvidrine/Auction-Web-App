import web
db = web.database(dbn='sqlite',
        db='AuctionBase.db' 
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    query_string = 'select CurrentTime from CurrentTime'
    results = query(query_string)
    return results[0].CurrentTime 


# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id})
    if(result != []):
        return result[0]

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

def update_query(query_string, vars = {}):
    return db.query(query_string, vars)

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time

def setTime(newTime):
    query_string = 'update CurrentTime set CurrentTime = $currentTime'
    t = db.transaction()
    try:
        update_query(query_string, {'currentTime': newTime})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()

def auctionClosed(itemID):
    query_string = 'select Buy_Price, Currently from Items where ItemID = $itemID'
    results = query(query_string, {'itemID': itemID})
    return results[0].Buy_Price == results[0].Currently

def addBid(itemID, userID, amount):
    if(auctionClosed(itemID)):
        return False
    query_string = 'insert into Bids values ($itemID, $userID, $currtime, $amount)'
    varvalues = {}
    varvalues['itemID'] = itemID
    varvalues['userID'] = userID
    varvalues['currtime'] = getTime()
    varvalues['amount'] = amount
    t = db.transaction()
    try:
        query(query_string, varvalues)       
    except Exception as e:
        t.rollback()
        print str(e)
        return False
    else:
        t.commit()
    return True


def search(itemID, userID, minPrice, maxPrice, description, category, status):
#Choose what tables to compute a cross product on.
    query_string = "select * from Items i"
    varvalues = {}
    conditions = False
    if(category != ""):
        conditions = True
        query_string = query_string + ', Categories ca'
    if(status != 'all'):
        conditions = True
        query_string = query_string + ', CurrentTime c'
    query_string = query_string + ' where '

#Add query conditions as necessary
    if(itemID != ""):
        conditions = True
        query_string = query_string + 'i.ItemID = $itemID AND '
        varvalues['itemID'] = itemID
    if(userID != ""):
        conditions = True
        query_string = query_string + 'i.UserID = $userID AND '
        varvalues['userID'] = userID
        print 'userID'
    if(minPrice != ""):
        conditions = True
        query_string = query_string + 'i.Currently >= $minPrice AND '
        varvalues['minPrice'] = minPrice
        print 'minprice'
    if(maxPrice != ""):
        conditions = True
        query_string = query_string + 'i.Currently <= $maxPrice AND '  
        varvalues['maxPrice'] = maxPrice
        print 'maxprice'
    if(description != ""):
        conditions = True
        query_string = query_string + 'i.Description like %$description% AND '
        varvalues['description'] = description
    if(category != ""):
        query_string = query_string + 'i.ItemID = ca.ItemID AND ca.Category = $category AND '
        varvalues['category'] = category
    if(status == 'open'):
        query_string = query_string + 'i.Started <= c.CurrentTime AND i.Ends > c.CurrentTime AND (i.Buy_Price is null OR i.Buy_Price != i.Currently)'
        varvalues['status'] = status
    if (status == 'close'):
        query_string = query_string + '(i.Ends < c.CurrentTime OR (i.Buy_Price is not null AND i.Buy_Price = i.Currently))'
        varvalues['status'] = status
    if (status == 'notStarted'):
        query_string = query_string + 'i.Started > c.CurrentTime'
        varvalues['status'] = status
    if (status == 'all'):
        if(conditions):
            query_string = query_string[:len(query_string)-5]
        else:
            query_string = query_string[:len(query_string)-7]
        varvalues['status'] = status
    return query(query_string, varvalues)


def lookup(itemID, tableName):
    query_string = ""
    if(tableName == 'Items'):
        query_string = 'select * from Items where ItemID = $itemID'
        return query(query_string, {'itemID': itemID})
    else:
        query_string = 'select UserID, Time, Amount from Bids where ItemID = $itemID'
        return query(query_string, {'itemID': itemID})
    
