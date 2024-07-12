import datetime

def convert_timestamp_to_readable(timestamp):
    try:
        # Convert the timestamp to an integer
        timestamp = int(timestamp)
        
        # Convert the timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        
        # Format the datetime object into a readable string
        readable_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        
        return readable_date
    except (ValueError, OverflowError) as e:
        return f"Error converting timestamp: {e}"

def convert_readable_to_timestamp(readable_date):
    try:
        # Convert the readable date string to a datetime object
        dt_object = datetime.datetime.strptime(readable_date, '%Y-%m-%d %H:%M:%S')
        
        # Convert the datetime object to a Unix timestamp
        timestamp = int(dt_object.timestamp())
        
        return timestamp
    except ValueError as e:
        return f"Error converting date: {e}"



if __name__ == "__main__":
    try:
        choice = input("Choose conversion type:\n1. Timestamp to Readable Date\n2. Readable Date to Timestamp\nEnter 1 or 2: ").strip()
        
        if choice == '1':
            time = input("Enter timestamp: ").strip()
            
            # Check if the timestamp length is either 10 or 13 digits
            if len(time) in {10, 13} and time.isdigit():
                print("Timestamp entered:", time)
                
                # If timestamp is in milliseconds, convert to seconds
                if len(time) == 13:
                    time = int(time) // 1000
                
                print("Readable date:", convert_timestamp_to_readable(time))
            else:
                print("Invalid timestamp. Please enter a valid 10-digit or 13-digit timestamp.")
        
        elif choice == '2':
            readable_date = input("Enter readable date (YYYY-MM-DD HH:MM:SS): ").strip()
            timestamp = convert_readable_to_timestamp(readable_date)
            if isinstance(timestamp, int):
                print("Unix timestamp:", timestamp)
            else:
                print(timestamp)
        
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    except ValueError:
        print("Invalid input. Please enter a valid choice, timestamp, or date.")
    except Exception as e:
        print("An error occurred. Please try again. Error details:", e)
