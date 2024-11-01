
import json


class readwriteJSON():

    def readJSON():
        # Opening JSON file
        with open('src/files/coord_data.json', 'r') as openfile:
         
            # Reading from json file
            json_object = json.load(openfile)
        
        json_object = json.loads(json_object) 
        # json_object = json.dumps(json_object, indent=2)
        # print(json_object)

        return json_object


    
    def saveJSON(coordinates):
        #data = coordinates.json()  # Convert the response to JSON
        data = json.dumps(coordinates)
        print(f"save datas {data}")
        # Store the JSON data in a file
        with open('src/files/coord_data.json', "w") as file:
            json.dump(data, file)
        
        print("Data stored successfully!")

