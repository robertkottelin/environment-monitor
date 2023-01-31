from database import config_database, connect, insert_temperature
from read_temp import read_temperature
from control_lamp import control_lamp
from sklearn.linear_model import LinearRegression

# Load the trained machine learning model from a file
ml_model = pickle.load(open('lamp_model.pkl', 'rb'))

# Define the fuzzy rules for the fuzzy controller
def fuzzy_rules(temp_error, rate_of_change):
    output = 0
    if temp_error > 0 and rate_of_change > 0:
        output = min(temp_error, rate_of_change)
    elif temp_error < 0 and rate_of_change < 0:
        output = max(temp_error, rate_of_change)
    return

def main():
    config_database()
    conn, cur = connect()
    prev_temp = None
    while True:
        temperature = read_temperature()
        insert_temperature(conn, cur, temperature)

        # Calculate the temperature error and rate of change
        if prev_temp is not None:
            temp_error = temperature - 22
            rate_of_change = temperature - prev_temp
        else:
            temp_error = 0
            rate_of_change = 0

        # Use the fuzzy rules to determine the initial output for the heating lamp
        fuzzy_output = fuzzy_rules(temp_error, rate_of_change)
        
        # Use the machine learning model to fine-tune the output
        ml_input = [[temperature, temp_error, rate_of_change]]
        ml_output = ml_model.predict(ml_input)[0]

        # Combine the fuzzy and machine learning outputs to determine the final heating lamp output
        lamp_output = 0.5 * fuzzy_output + 0.5 * ml_output

        # Turn the heating lamp on or off based on the final output
        if lamp_output > 0:
            control_lamp('on')
        else:
            control_lamp('off')

        prev_temp = temperature
        # time.sleep(1)

if __name__ == '__main__':
    main()

