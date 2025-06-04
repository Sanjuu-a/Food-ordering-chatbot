
import mysql.connector

# Establish the connection to the database
db = mysql.connector.connect(
    host="127.0.0.1",  # Your host, e.g., 'localhost'
    port=3306,  # Your port, e.g., 3306
    user="root",  # Your username, e.g., 'root'
    password="chotu",  # Your password
    database="pandeyji_eatery"  # Your database name
)

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = db.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        db.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")
        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        db.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        db.rollback()
        return -1

def get_total_order_price(order_id):
    cursor = db.cursor()

    # Get total order price (User-defined function)
    query = f"SELECT get_total_order_price({order_id})"  # Calling user-defined function
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Save to db:
def get_next_order_id():
    cursor = db.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)  # Changed from db.execute(query)

    # Fetch the result
    result = cursor.fetchone()[0]

    # Close the cursor
    cursor.close()

    # Return the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

def insert_order_tracking(order_id, status):
    try:
        cursor = db.cursor()

        # Inserting the record into the order_tracking table
        insert_query = "INSERT INTO order_tracking(order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))

        # Commit the changes
        db.commit()

        # Closing the cursor
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error inserting order tracking: {err}")
        db.rollback()

# Define the function to get the order status
def get_order_status(order_id: int):
    try:
        # Create a cursor object
        cursor = db.cursor()

        # SQL query to fetch the status for a given order_id
        query = "SELECT status FROM order_tracking WHERE order_id = %s"

        # Execute the query with the provided order_id
        cursor.execute(query, (order_id,))

        # Fetch the result (expecting one result)
        result = cursor.fetchone()

        # Check if the result exists
        if result is not None:
            return result[0]  # Return the status of the order
        else:
            return None  # Return None if no such order is found

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor
        cursor.close()


# Example usage
order_id = 1  # Replace this with the actual order ID you're testing
order_status = get_order_status(order_id)

# Display result based on the order ID
if order_status:
    print(f"The order status for order ID {order_id} is {order_status}")
else:
    print(f"Order Status: Order ID {order_id} not found.")
