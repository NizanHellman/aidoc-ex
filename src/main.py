from .storage import LocalStorage


def main():
    # Initialize storage
    storage = LocalStorage("example_storage")
    
    # Example data
    user = {
        "name": "Nizan",
        "age": 33,
        "location": "Mattan",
        "hobbies": ["coding", "gaming", "reading"],
        "contact": {
            "email": "nizan@example.com",
            "phone": "123-456-7890"
        }
    }
    
    # Store data
    print("Storing user data...")
    storage.save("user", user)
    
    # Retrieve data
    print("\nRetrieving user data...")
    loaded_user = storage.get("user")
    
    # Display results
    print(f"\nStored user data:")
    print(f"Name: {loaded_user['name']}")
    print(f"Age: {loaded_user['age']}")
    print(f"Location: {loaded_user['location']}")
    print(f"Hobbies: {', '.join(loaded_user['hobbies'])}")
    print(f"Email: {loaded_user['contact']['email']}")
    

if __name__ == "__main__":
    main()
