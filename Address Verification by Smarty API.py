# -*- coding: utf-8 -*-
import smartystreets_python_sdk
import os
import pandas as pd
import numpy as np

from smartystreets_python_sdk import SharedCredentials, StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
from smartystreets_python_sdk.us_street.match_type import MatchType

addresses = pd.read_csv('Book(Sheet1).csv')
outputsRows = []

def run():


    # for server-to-server requests, use this code:
    auth_id = os.environ['SMARTY_AUTH_ID']
    auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()

    # client = ClientBuilder(credentials).with_custom_header({'User-Agent': 'smartystreets (python@0.0.0)', 'Content-Type': 'application/json'}).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_http_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
    # Uncomment the line above to try it with a proxy instead

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields
    for index, address in addresses.iterrows():
        lookup = StreetLookup()
        lookup.input_id = index  # Optional ID from your system
        lookup.street = address['Street']
        lookup.urbanization = ""  # Only applies to Puerto Rico addresses
        lookup.city = address['City']
        lookup.state = address['State']
        lookup.zipcode = address['ZIP']
        lookup.candidates = 3
        lookup.match = MatchType.INVALID  # "invalid" is the most permissive match,
                                          # this will always return at least one result even if the address is invalid.
                                          # Refer to the documentation for additional Match Strategy options.
    
        # Uncomment the below line to add a custom parameter
        # lookup.add_custom_parameter("parameter", "value")
    
        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            print(err)
            return
    
        result = lookup.result
    
        if not result:
            print("No candidates. This means the address" + address + "is not valid.")
    
        first_candidate = result[0]
    
        # print("There is at least one candidate.")
        # print("If the match parameter is set to STRICT, the address is valid.")
        # print("Otherwise, check the Analysis output fields to see if the address is valid.\n")
        
        outputsRows.append({'Number':first_candidate.components.primary_number, 'Street Name': first_candidate.components.street_name, 'ZIP Code': first_candidate.components.zipcode, 'County': first_candidate.metadata.county_name, 'Residential': first_candidate.metadata.rdi, 'DPV CMRA': first_candidate.analysis.cmra, 'DPV Match Code': first_candidate.analysis.dpv_match_code, 'Vacant': first_candidate.analysis.vacant})
        
        print("Input ID: {}".format(lookup.input_id))
        # print("ZIP Code: " + first_candidate.components.zipcode)
        # print("County: " + first_candidate.metadata.county_name)
        # print("Latitude: {}".format(first_candidate.metadata.latitude))
        # print("Longitude: {}".format(first_candidate.metadata.longitude))
        # print("Precision: {}".format(first_candidate.metadata.precision))    
        # print("Residential: {}".format(first_candidate.metadata.rdi))
        # print("DPV CMRA: " + first_candidate.analysis.cmra)
        # print("DPV Match Code: " + first_candidate.analysis.dpv_match_code)
        # print("Vacant: {}".format(first_candidate.analysis.vacant))
        # Complete list of output fields is available here:  https://smartystreets.com/docs/cloud/us-street-api#http-response-output
    outputs = pd.DataFrame(outputsRows)
    outputs.to_csv('output.csv')

if __name__ == "__main__":
    run()