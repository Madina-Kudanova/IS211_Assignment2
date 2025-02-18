import argparse
import urllib.request
import logging
import datetime
import ssl

# Function to set up the logger
def setup_logger():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    formatter = logging.Formatter('Error processing line #%s for ID #%s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def downloadData(url):
    """Downloads the data"""
    context = ssl._create_unverified_context()  # Create an SSL context to ignore certificates 
    try:
        with urllib.request.urlopen(url, context=context) as response:
            data = response.read().decode('utf-8')
            return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        exit()

def processData(file_content):
    logger = setup_logger()
    personData = {}
    
    # Split the data into lines and process each line
    lines = file_content.splitlines()
    
    for linenum, line in enumerate(lines, 1):
        try:
            parts = line.split(',')
            user_id = int(parts[0])  # Assumes the ID is the first column
            name = parts[1]  # Assumes the name is the second column
            birthday_str = parts[2]  # Assumes the birthday is the third column
            
            # Try to parse the birthday into a datetime object
            try:
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
            except ValueError:
                logger.error(f"Error processing line #{linenum} for ID #{user_id}")
                continue
            
            # Store the data in the dictionary
            personData[user_id] = (name, birthday)
        
        except Exception as e:
            print(f"Error processing line #{linenum}: {e}")
    
    return personData


def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that ID.")
    

def main(url):
    print(f"Running main with URL = {url}...")
    # Download the data from the URL
    csvData = downloadData(url)
    
    # Process the data 
    personData = processData(csvData)
    
    # Ask for user input and display the person's info
    while True:
        user_id = int(input("Enter an ID to lookup (or 0 or negative to exit): "))
        if user_id <= 0:
            print("Exiting...")
            break
        displayPerson(user_id, personData)



if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
