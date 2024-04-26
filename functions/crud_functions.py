'''

This module contains all CRUD functions called from app.py as well as additional helper functions for abstraction.
These functions are designed to help you manipulate the data within the MySQL database as well as format data types.

Additionally, there is also a function which takes in an SQL string query as a parameter (which you can edit through here)
and returns data. 

'''

#This will import SQL_Connection module in order to connect with MySQL database.
from functions.SQL_Connection import * 

#This will be used to change the date format from yyyy-mm-dd to dd/mm/yyyy to ensure consistency within the database.
from datetime import datetime

#This function will obtain a list of all entries/rows within the MySQL database.
def all_entries():

    #This is a variable representing database connection.
    sql_cxn = dbConnection()

    #Cursor used to execute statements to communicate with the MySQL database.
    cur = sql_cxn.cursor(dictionary = True) # 'dictionary=True' will return each entry as a dictionary

    #This is a SQL query to return all entries from the datatable sorted by 'id'
    sql_query = 'SELECT * FROM sales ORDER BY id'

    #This executes given query.
    cur.execute(sql_query)

    #This represents all entries in the database.
    all_entries = cur.fetchall()

    #Closes the cursor, resets all results, and ensures that the cursor object has no reference to its original connection object.
    cur.close()

    #Closes connection to MySQL database.
    sql_cxn.close()
    return all_entries

#This function will return a set of entries based on an input pair of dates. This was by far
#the most difficult part of this application to implement due to formatting and syntax complexities.
def entries_by_date(start_date, end_date):

    # Comments for functionality included already within 'def all_entries()'.
    sql_cxn = dbConnection()
    cur = sql_cxn.cursor(dictionary=True)

    #Calling our helper function to format the date.
    start_date = format_transaction_date(start_date)
    end_date = format_transaction_date(end_date)

    # SQL query to retrieve data greater than or equal to start_date
    query_start = "SELECT * FROM sales WHERE transaction_date >= %s ORDER BY transaction_date ASC"
    cur.execute(query_start, (start_date,))
    data_start = cur.fetchall()

    #----------------------------------

    '''
    The following represents a solution for not being able to use the 'SELECT * FROM __ WHERE __ BETWEEN __ AND __' SQL query.
    It instead filters data given after a certain 'start_date' if it falls before the 'end_date'.

    '''

    #----------------------------------

    #Initialize an empty list to store filtered entries.
    filtered_entries = []

    # Iterate through the entries
    for entry in data_start:

        #Extract the transaction_date from the entry.
        extracted_date = entry['transaction_date']

        #Check if the transaction_date is less than or equal to end_date.
        if extracted_date <= end_date:

            #If so, add the entry to the filtered_entries list
            filtered_entries.append(entry)

    #Close the cursor and connection
    cur.close()
    sql_cxn.close()

    #Return the filtered_entries list containing entries between start_date and end_date
    return filtered_entries

#This function will allow you to add an entry to the database.
def add_entry(id = '', store_code = '', total_sale = '', transaction_date = ''):

    #Comments for functionality included already within 'def all_entries()'.
    sql_cxn = dbConnection()
    cur = sql_cxn.cursor(dictionary = True)

    #Formatting our 'transaction_date'
    transaction_date = format_transaction_date(transaction_date)

    #Formatting 'total_sale'.
    total_sale = format_total_sale(total_sale)

    #SQL query for inserting data into database.
    sql_query = ("INSERT INTO sales (id, store_code, total_sale, transaction_date) VALUES (%s, %s, %s, %s)")
    values = (id, store_code, total_sale, transaction_date)
    cur.execute(sql_query, values)

    #Commit changes to data base and close.
    sql_cxn.commit()
    cur.close()
    sql_cxn.close()

    #This represents number of rows affected (0 or 1).
    add_result = cur.rowcount

    #Will return 1 if addition was successful.
    return add_result

#This function will allow you to edit an entry within the database.
def edit_entry(id = '', store_code = '', total_sale = '', transaction_date = ''):
    sql_cxn = dbConnection()
    cur = sql_cxn.cursor(dictionary = True)

    # Formatting our 'transaction_date'
    transaction_date = format_transaction_date(transaction_date)

    #Formatting our 'total_sale'
    total_sale = format_total_sale(total_sale)

    #SQL query for editing and updating data wihtin the database.
    sql_query = ("UPDATE sales SET store_code = %s, total_sale = %s, transaction_date = %s WHERE id = %s")
    values = (store_code, total_sale, transaction_date, id)
    cur.execute(sql_query, values)

    #Commit changes to data base and close.
    sql_cxn.commit()
    cur.close()
    sql_cxn.close()

    #This represents the number of rows that were modified. 
    edit_result = cur.rowcount 
    return edit_result

#This function will allow you to delete an entry from the database.
def delete_entry(id = ''):
    sql_cxn = dbConnection()
    cur = sql_cxn.cursor(dictionary = True)

    #SQL query for deleting data wihtin the database.
    sql_query = ("DELETE FROM sales WHERE id = %s")

    #Since 'id' is a single value wrapped in parentheses, we include a comma so that it can be interpreted as a tuple.
    values = (id,)
    cur.execute(sql_query, values)

    #Commit changes to data base and close.
    sql_cxn.commit()
    cur.close()
    sql_cxn.close()

    #This represents the number of rows that were modified.
    delete_result = cur.rowcount 
    return delete_result


'''

Included below are additional helper functions for formatting.

'''

#This helper function is designed to format the dates. In HTML, dates are represented as YYYY-MM-DD, whereas in our MySQLdatabase 
#the dates are formatted as MM/DD/YYYY with no trailing zeroes.
def format_transaction_date(transaction_date):

    # Convert the transaction_date string to a datetime object
    transaction_date_obj = datetime.strptime(transaction_date, '%Y-%m-%d')

    # Format the datetime object to the desired format without leading zeroes
    transaction_date_formatted = transaction_date_obj.strftime('%m/%d/%Y')

    # Remove leading zeroes from day and month if present
    transaction_date_final = '/'.join(str(int(x)) for x in transaction_date_formatted.split('/'))

    return transaction_date_final

#This helper function is designed to format the 'total_sale' amount like the other values in our MySQL database.
def format_total_sale(total_sale):

    #Convert total_sale to float and format it to two decimal places.
    total_sale_formatted = '{:,.2f}'.format(float(total_sale))

    #Add dollar sign to the formatted total_sale.
    total_sale_with_currency = '$' + str(total_sale_formatted)

    return total_sale_with_currency



