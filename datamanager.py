from pocketbase import PocketBase  # Client also works the same

client = PocketBase('http://127.0.0.1:8090')

# list and filter "example" collection records
result = client.collection("example").get_list(
    1, 20, {"filter": 'status = true && created > "2022-08-01 10:00:00"'})

# create record and upload file to image field

class DataManager : 
    data_array : list
    
    def __init__(self, data_array,client) :
        self.data_2_add = data_array
        self.client = client 
    
    #we'll see how the data will be organized in the array
    def add_data(self, collection : str) : 
         return self.client.collection(collection).update(
           {"sparkdata" : self.data_array}
            )
         
    def get_data(self, client, collection) :
        data = client.collections(collection).get_list({"sparkdata"})  
    
    def create_collection(self, client, collection : str) :
        client.collections(collection).create()
        