import re
import json
import random
from datetime import datetime
from producer_app.configs import RAW_DATA_FILE_PATH

class DataGenerator:
    def __init__(self):
        self.data = self._load_data_from_file()

    def _load_data_from_file(self):
        """
            Summary:
                Load the full search results data from a .txt file
            Description:
                Load the full search results data from a .txt file into a python list
            Parameters:
            Returns:
                list: a python list that represent the search results such that each element
                is a user search results for multiple hotels
        """
        with open(RAW_DATA_FILE_PATH, 'r') as raw_data:
            data = [line.strip() for idx, line in enumerate(raw_data)]

        return data

    def _jsonify_search_results(self, search_results_str: str) -> dict:
        """
           Summary:
               Parse the hotelresults string
           Description:
               Fix the hotelresults string, wrap the hotel IDs inside a double quote  to be a valid json string
               and convert that json string into python dictionary
           Parameters:
               search_results_str (str): a string that represent the hotelresults for a single user
               in the search results data.
           Returns:
               dict: a python dictionary that represent the given string
       """
        s = search_results_str
        matches_start_idx = []
        # Pattern to find the hotel ID
        pattern = re.compile(r'\d{4}:{')
        # Find all matches (hotel IDs) start index in the given string
        for match in pattern.finditer(s):
            matches_start_idx.append(match.start())
            # print("match", match.group(), "start index", match.start(), "End index", match.end())

        # For each start idx calculate the new start idx in the modified string
        # Partition string into 3 parts then wrap the hotel ID in "" and construct the new one
        for i in range(len(matches_start_idx)):
            """ 
               Calculate the new idx of the hotel ID in the modifed string, 
               As long as we wrap the hotel ID inside double quotes which means pushing the idx 2 positions forward,
               so we need to adjust the current idx of the current hotel ID idx in the original string with
               respect to it's order of persistence in the matches_start_idx list
           """
            idx = matches_start_idx[i]
            modified_idx = idx + (i * 2)

            # Get the left sub-string
            part_1 = s[0: modified_idx]
            # Get the middle sub-string, Actual hotel ID
            part_2 = s[modified_idx: modified_idx + 4]
            # Get the right sub-string
            part_3 = s[modified_idx + 4:]
            # Construct the new string with the hotel ID wrapped inside double quotes
            s = part_1 + f'"{part_2}"' + part_3

        # Convert that complex datatype string into python dict
        datatype_dict = json.loads(s)

        return datatype_dict

    def randomly_generate_data(self):
        """
            Summary:
                Select a user's search results and break it down into multiple searchs
            Description:
                Every time this method being invoked its randomly select an element from the raw data list,
                flatten and break that element down into multiple searches such that each search has the following format
                {
                    'user_id': {USER-ID-STR},
                    'hotel_id': {HOTEL-ID-STR},
                    'search_timestamp': {DATETIME-TIMESTAMP},
                    'hotel_advertisers':  {DICT}
                }
            Parameters:
            Returns:
                bytes: a bytes object
        """
        line = random.choice(self.data)
        line = line.strip()

        user_id, timestamp, search_results = line.split('\t')
        search_results_json = self._jsonify_search_results(search_results)

        message = dict()
        message['user_id'] = user_id
        for hotel_id, advertisers in search_results_json.items():
            message['hotel_id'] = hotel_id
            message['search_timestamp'] = datetime.now().timestamp()
            message['hotel_advertisers'] = advertisers['advertisers']

            yield bytes(json.dumps(message), encoding='utf-8')

    def generate_all_data(self):
        """
            Summary:
                Get all search results data in the .txt file
            Description:
                flatten and break the search results elements down into multiple searches such that each search has the following format
                {
                    'user_id': {USER-ID-STR},
                    'hotel_id': {HOTEL-ID-STR},
                    'search_timestamp': {DATETIME-TIMESTAMP},
                    'hotel_advertisers':  {DICT}
                }
            Parameters:
            Return:
                bytes: a bytes object
        """
        # line = random.choice(self.data)
        for line in self.data:
            line = line.strip()

            user_id, timestamp, search_results = line.split('\t')
            search_results_json = self._jsonify_search_results(search_results)

            message = dict()
            message['user_id'] = user_id
            for hotel_id, advertisers in search_results_json.items():
                message['hotel_id'] = hotel_id
                message['search_timestamp'] = datetime.now().timestamp()
                message['hotel_advertisers'] = advertisers['advertisers']

                yield bytes(json.dumps(message), encoding='utf-8')
