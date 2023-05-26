import json
import datetime

def count_keywords(text, keywords):

    # Initialize a dictionary to store keyword counts
    keyword_counts = {}

    # Process the text
    for keyword in keywords:
        count = text.lower().count(keyword.lower())  # Case-insensitive count
        if count > 0:
            keyword_counts[keyword] = count

    # Get the current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the output dictionary
    output_dict = {
        'timestamp': current_time,
        'keyword_counts': keyword_counts
    }

    # Generate JSON output
    

    return output_dict


#The output JSON will contain each keyword as a key and its corresponding count as the value.
