def create_payload(dictionary):
        payload_scoring = {"input_data": [
                        {"fields": ["Unnamed: 0","Fartøynasjonalitet gruppe","Kvalitet", "Art FAO","Fartøynavn","Hovedområde FAO"],
                                "values": [[None,None,None,"Sild",None,None]]}]}
        payload_scoring_order = payload_scoring["input_data"][0]["fields"]
        list_default = [None, None, None, None, None, None]
        for i in list(dictionary):
                verdi = dictionary[i]
                location = payload_scoring_order.index(i)
                list_default[location] = verdi
        payload_scoring["input_data"][0]["values"] = [list_default]
        return payload_scoring



def query_ai_model(dictionary):
    import requests
    payload_scoring = create_payload(dictionary)
    API_KEY = "C3MoXJ5hNilXgWfmxgyDtm8pinnSRPs7JumSwYUE_vPy"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    response_scoring = requests.post("https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/4af07307-6c7e-4367-bfcc-c47b79a95a68/predictions?version=2023-01-11", json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    return response_scoring.json()
