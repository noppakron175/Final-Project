import random
import string
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("password-panda-firebase-adminsdk-pikqp-d441acb80f.json")  # Path to your Firebase credentials
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def generate_random_password(length):
    lower_case_letters = string.ascii_lowercase
    upper_case_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    password = [
        random.choice(upper_case_letters),
        random.choice(digits),
        random.choice(special_characters)
    ]

    all_characters = lower_case_letters + upper_case_letters + digits + special_characters
    password += [random.choice(all_characters) for _ in range(length - len(password))]
    random.shuffle(password)

    return ''.join(password)

def save_to_firebase(username, password):
    print(f"Attempting to save user: {username}, password: {password}")
    try:
        # Add user data to the 'users' collection
        doc_ref_tuple = db.collection('users').add({
            'username': username,
            'password': password
        })
        # Extract document ID from the returned tuple
        doc_ref = doc_ref_tuple[1] if isinstance(doc_ref_tuple, tuple) else doc_ref_tuple
        print(f"User saved with ID: {doc_ref.id if hasattr(doc_ref, 'id') else 'unknown'}")
        return doc_ref.id if hasattr(doc_ref, 'id') else None
    except Exception as e:
        print(f"Failed to save user: {e}")
        return None


def main():
    st.title("Password Generator")

    username = st.text_input("Enter your username:")
    length = st.number_input("Enter the desired password length (at least 4 characters):", min_value=4)

    method = st.radio("Choose a password generation method:", ("Simple random generation", "Select character types", "Specify required characters"))

    if method == "Simple random generation":
        if st.button("Generate Password"):
            password = generate_random_password(length)
            st.success(f"Generated password: *{password}*")
            if username:
                user_id = save_to_firebase(username, password)
                if user_id:
                    st.success(f"User saved with ID: {user_id}")
                else:
                    st.error("Failed to save user to Firebase. Check the console for details.")
            else:
                st.error("Please enter a username.")

if _name_ == "_main_":
    main()
    
