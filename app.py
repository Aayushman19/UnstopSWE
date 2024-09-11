from flask import Flask, render_template, request, jsonify, render_template_string

app = Flask(__name__)

rows = 11
seats_per_row = 7
seats = {}
for row in range(rows):
    for seat in range(seats_per_row if row < 10 else 3):
        seat_number = row * seats_per_row + seat + 1
        seats[seat_number] = False

def book_seats(num_seats):
    if num_seats > 7:
        return {"error": "You cannot book more than 7 seats at a time"}
    
    available_seats = []
    
    for row in range(10):
        row_seats = [i for i in range(row * seats_per_row + 1, row * seats_per_row + seats_per_row + 1)]
        booked_seats = [seat for seat in row_seats if seats[seat]]
        free_seats = [seat for seat in row_seats if not seats[seat]]
        
        if len(free_seats) >= num_seats:
            available_seats = free_seats[:num_seats]
            break
    
    if not available_seats:
        for row in range(10):
            row_seats = [i for i in range(row * seats_per_row + 1, row * seats_per_row + seats_per_row + 1)]
            free_seats = [seat for seat in row_seats if not seats[seat]]
            
            if len(free_seats) >= num_seats:
                available_seats = free_seats[:num_seats]
                break
        
        if not available_seats:
            last_row_seats = [i for i in range(71, 74)]
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
    return render_template('reservation.html', seats = seats)

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
