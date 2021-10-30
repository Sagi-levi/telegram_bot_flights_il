from pandas import DataFrame


def get_database():
    CONNECTION_STRING = "mongodb+srv://SGLV:rxQC*3vPuXi38nc@yadstaim.gvmoh.mongodb.net/test"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['BestFlightsDB']


# This is added so that many files can reuse the function get_database()

def Read_all_flights():
    dbname = get_database()
    collection_name = dbname["currentBestFlights"]
    item_details = collection_name.find()
    # convert the dictionary objects to dataframe
    items_df = DataFrame(item_details)
    return items_df


def Better_new_same(flight):
    print(flight['To'])
    dbname = get_database()
    collection_name = dbname["currentBestFlights"]
    x = collection_name.find_one({'To': flight['To'],
                                  'From': flight['From'],
                                  'MinPrice': flight['MinPrice'],
                                  'DepartureDate': flight['DepartureDate']})
    if x is None:
        Add_new_best_flight(flight)
        return
    if x['MinPrice'] > flight['MinPrice']:
        collection_name.delete_one(x)
        Add_new_best_flight(flight)


def Add_new_best_flight(flight):
    dbname = get_database()
    collection_name = dbname["currentBestFlights"]
    collection_name.insert(flight)

# def Replace_best_flight(flight_id):
#     filter = {'_id': flight_id}
#     newValue
#     dbname = get_database()
#     collection_name = dbname["currentBestFlights"]
#     collection_name.update_one(filter)
