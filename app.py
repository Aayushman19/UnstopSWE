from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Initialize the seating arrangement
rows = 11  # 10 rows with 7 seats + 1 row with 3 seats
seats_per_row = 7
seats = {}
for row in range(rows):
    for seat in range(seats_per_row if row < 10 else 3):
        seat_number = row * seats_per_row + seat + 1
        seats[seat_number] = False  # All seats are initially unbooked

# Function to book seats
def book_seats(num_seats):
    if num_seats > 7:
        return {"error": "You cannot book more than 7 seats at a time"}
    
    available_seats = []
    
    # Check for available rows first
    for row in range(10):  # First 10 rows have 7 seats each
        row_seats = [i for i in range(row * seats_per_row + 1, row * seats_per_row + seats_per_row + 1)]
        booked_seats = [seat for seat in row_seats if seats[seat]]
        free_seats = [seat for seat in row_seats if not seats[seat]]
        
        if len(free_seats) >= num_seats:
            available_seats = free_seats[:num_seats]
            break
    
    # If not enough seats in any row, look for nearby seats
    if not available_seats:
        for row in range(10):  # First 10 rows
            row_seats = [i for i in range(row * seats_per_row + 1, row * seats_per_row + seats_per_row + 1)]
            free_seats = [seat for seat in row_seats if not seats[seat]]
            
            if len(free_seats) >= num_seats:
                available_seats = free_seats[:num_seats]
                break
        
        # Check last row separately
        if not available_seats:
            last_row_seats = [i for i in range(71, 74)]  # Last row
            free_seats = [seat for seat in last_row_seats if not seats[seat]]
            
            if len(free_seats) >= num_seats:
                available_seats = free_seats[:num_seats]
    
    if available_seats:
        for seat in available_seats:
            seats[seat] = True
        return {"booked_seats": available_seats}
    else:
        return {"error": "Not enough seats available"}

@app.route('/')
def index():
    return render_template_string('''
        <h1>Train Seat Reservation</h1>
        <form action="/book" method="post">
            <label for="seats">Number of Seats:</label>
            <input type="number" id="seats" name="seats" min="1" max="7" required>
            <input type="submit" value="Book Seats">
        </form>
        <h2>Seat Map</h2>
        <pre>
        {% for row in range(0, 80, 7) %}
            {% for seat in range(row + 1, row + 8) %}
                {% if seat in seats and seats[seat] %}
                    [X]
                {% else %}
                    [ ]
                {% endif %}
            {% endfor %}
            {% if row == 70 %}
                {% for seat in range(71, 74) %}
                    {% if seat in seats and seats[seat] %}
                        [X]
                    {% else %}
                        [ ]
                    {% endif %}
                {% endfor %}
            {% endif %}
        {% endfor %}
        </pre>
    ''')

@app.route('/book', methods=['POST'])
def book():
    num_seats = int(request.form['seats'])
    result = book_seats(num_seats)
    
    if 'error' in result:
        return jsonify(result)
    else:
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
