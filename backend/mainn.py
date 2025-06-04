
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mysql.connector
import db_helper
import generic_helper

app = FastAPI()
inprogress_order = {}

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="chotu",
    database="pandeyji_eatery"
)

# Define the function to get the order status
def get_order_status(order_id: int):
    try:
        cursor = db.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None


@app.post("/")
async def handle_request(request: Request):
    # Parse the request from Dialogflow
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    # Print intent and parameters to debug
    print(f"Received intent: {intent}")  # Debugging: Print the intent name
    print(f"Received parameters: {parameters}")

    # Dictionary to map intents to their respective handler functions
    intent_handler_dict = {
        'order.add-context: ongoing-order': add_to_order,
        'order.remove-context: ongoing-order' : remove_from_order,
        'order.complete-context: ongoing order': complete_order,
        'track.order-context: ongoing order' : track_order
    }

    # Check if the intent is in the handler dictionary
    if intent in intent_handler_dict:
        return intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={"fulfillmentText": "Sorry, I couldn't understand that."})

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        return JSONResponse(content={
            "fulfillmentText": "I am having trouble finding your order. Sorry! Can you place a new order, please?"
        })

    current_order = inprogress_order[session_id]
    food_items = parameters.get("food-items", [])

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    # Construct the response
    fulfillment_text = ""

    if removed_items:
        fulfillment_text += f'Removed {", ".join(removed_items)} from your order! '

    if no_such_items:
        fulfillment_text += f'Your current order does not have {", ".join(no_such_items)}. '

    if not current_order:
        fulfillment_text += "Your order is now empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })





    #Steps: 1. locate the session id record: {'vada pav':3, "mango lassi:1}
    #S2: get value from dict
    #S3: remove the food items. request :["vada pav","pizza"]


# Function to handle adding items to an order
def add_to_order(parameters: dict, session_id: str):
    print(f"Received parameters for add_to_order: {parameters}")

    food_items = parameters.get("food-items", [])
    quantities = parameters.get("number", [])

    print(f"Extracted food items: {food_items}")
    print(f"Extracted quantities: {quantities}")

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantity clearly :)"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_order:
            current_food_dict = inprogress_order[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_order[session_id] = current_food_dict
        else:
            inprogress_order[session_id] = new_food_dict

        print("***************")
        print(inprogress_order)

        order_str = generic_helper.get_str_from_food_dict(inprogress_order[session_id])
        fulfillment_text = f"So far, you have ordered: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def complete_order(parameters: dict, session_id: str):
    # Log the session ID to debug
    print(f"Session ID in complete_order: {session_id}")
    print(f"inprogress_order dictionary: {inprogress_order}")  # Debugging: Check current orders

    # Handle different sessions wrt session_id
    if session_id not in inprogress_order:
        fulfillment_text = "Sorry! I am having trouble finding your order. Can you place a new order, please?"

    else:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to backend error. Please place a new order again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome! We have placed your order. Here is your order ID # {order_id}. " \
                               f"Your order total is {order_total}, which you can pay at the time of delivery :)"

        # Remove items from dict when the order is completed
        del inprogress_order[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order: dict):
    #order = {"pizza":2, "chole":1}
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode ==-1:
           return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id



# Function to handle the "track order" intent
def track_order(parameters: dict, session_id: str = None):  # session_id is optional for tracking
    order_id = int(parameters.get('order_id', 0))  # Extract order_id from parameters
    order_status = get_order_status(order_id)  # Call the function to get order status

    if order_status:
        fulfillment_text = f"The order status for order ID {order_id} is: {order_status}."
    else:
        fulfillment_text = f"No order found with order ID {order_id}."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



# Running the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, ssl_keyfile="key.pem", ssl_certfile="cert.pem")












