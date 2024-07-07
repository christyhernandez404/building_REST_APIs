#Create Flask routes to add, retrieve, update, and delete members from the Members table.
#Use appropriate HTTP methods: POST for adding, GET for retrieving, PUT for updating, and DELETE for deleting members.

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow # will use this to create a schema
from marshmallow import fields, ValidationError 
from connection import connection, Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only = True) 
    member_name = fields.String(required=True) #to be valid, this needs a value
    email = fields.String(required=True)
    phone = fields.String(required=True)

class MembersSchema(ma.Schema):
    id = fields.Int(dump_only = True) 
    member_name = fields.String(required=True) #to be valid, this needs a value
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta(): 
        fields = ("member_name", "email", "phone")

member_schema = MemberSchema() 
members_schema = MembersSchema(many=True) 


class SessionSchema(ma.Schema):
    id = fields.Int(dump_only = True) 
    member_id = fields.Int(required=True) 
    duration = fields.Int(required=True)
    session_time_date = fields.DateTime(required=True)


class SessionsSchema(ma.Schema):
    id = fields.Int(dump_only = True) 
    member_id = fields.Int(required=True) 
    duration = fields.Int(required=True)
    session_time_date = fields.DateTime(required=True)


    class Meta(): 
        fields = ("member_id", "duration", "session_time_date")

session_schema = SessionSchema() 
sessions_schema = SessionsSchema(many=True) 

#reads all member data via a GET request
@app.route("/members", methods = ['GET'])
def get_members():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True) 
            query = "SELECT * FROM members;"

            cursor.execute(query)
            members = cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members) 
            #it will take members data, turn it into json data.

# Create a new member with a POST request
@app.route("/members", methods= ["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            #new member data
            new_member = (member_data["member_name"], member_data["email"],member_data["phone"])

            query = "INSERT INTO members(member_name, email, phone) VALUES (%s,%s,%s)"

            # Execute the query with new_member data
            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message': 'New member added successfully!'}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

#UPDATE member
@app.route("/members/<int:id>", methods= ["PUT"]) # dynamic route that will change based off of different query parameters

def update_customer(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member: #if we dont find any member with that id
                return jsonify({"error": "Member was not found."}), 404
            
            updated_member = (member_data['member_name'], member_data['email'], member_data['phone'],id)

            query = "UPDATE members SET member_name = %s, email = %s, phone = %s WHERE id = %s"

            cursor.execute(query, updated_member)
            conn.commit()

            return jsonify({'message': f"Successfully updated user {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

#delete member
@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members where id = %s"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member not found"})
            
            
            query = "DELETE FROM members where id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"message": f"Member {id} was succesfully deleted!"})
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()

# Create a new session with a POST request
@app.route("/workoutsession", methods= ["POST"])
def add_session():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            #new session data
            new_session = (session_data["member_id"], session_data["duration"],session_data["session_time_date"])

            query = "INSERT INTO workout_sessions(member_id, duration, session_time_date) VALUES (%s,%s,%s)"

            # Execute the query with new_member data
            cursor.execute(query, new_session)
            conn.commit()

            return jsonify({'message': 'New session added successfully!'}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
#UPDATE workout session
@app.route("/workoutsession/<int:id>", methods= ["PUT"]) 

def update_session(id):
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM workout_sessions WHERE id = %s"
            cursor.execute(check_query, (id,))
            session = cursor.fetchone()
            if not session: #if we dont find any session with that id
                return jsonify({"error": "session was not found."}), 404
            
           
            updated_session = (session_data['member_id'], session_data['duration'], session_data['session_time_date'],id)

            query = "UPDATE workout_sessions SET member_id = %s, duration = %s, session_time_date = %s WHERE id = %s"

            cursor.execute(query, updated_session)
            conn.commit()

            return jsonify({'message': f"Successfully updated session {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
#reads all session data via a GET request
@app.route("/workoutsessions", methods = ['GET'])
def get_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True) 
            query = "SELECT * FROM workout_sessions;"

            cursor.execute(query)
            sessions = cursor.fetchall()
        finally:
            if conn and conn.is_connected(): #dont under why both statements are needed here
                cursor.close()
                conn.close()
                return sessions_schema.jsonify(sessions) 

if __name__ == "__main__": #this will start Flask every time
    app.run(debug=True)





    