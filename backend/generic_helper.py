
# Session_id using Python's Regular expression concept
import re
def extract_session_id(session_str: str):

    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""

def get_str_from_food_dict(food_dict: dict):
    return ",".join([f"{int(value)} {key}" for key, value in food_dict.items()])

#To test
if __name__ == "__main__":
    print(get_str_from_food_dict({"samosa": 2, "chole": 5}))
    #print(extract_session_id("projects/ruby-chatbot-bed9/agent/sessions/9cf22652-3e08-bc79-957e-ce67c3c951c4/contexts/ongoing-tracking"))
