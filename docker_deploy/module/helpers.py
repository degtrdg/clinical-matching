import json
import chromadb

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_path}")
    return None  # Returning None to indicate that loading failed

def process_clinical_trial_data(data):
    def safe_get(d, keys, default='Not provided'):
        """
        Safely get a nested key from a dictionary.
        If any key in the chain is missing or the type is unexpected, return the default value.
        """
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return default
        return d if d is not None else default

    try:
        # Assume data is a dictionary and 'protocolSection' key must exist
        protocol_section = data.get('protocolSection', {})
        
        # Use the safe_get function to retrieve nested information
        identification_info = safe_get(protocol_section, ['identificationModule'], {})
        conditions_info = safe_get(protocol_section, ['conditionsModule', 'conditions'])
        interventions_list = safe_get(protocol_section, ['armsInterventionsModule', 'interventions'], [])
        eligibility_info = safe_get(protocol_section, ['eligibilityModule'], {})
        summary_info = safe_get(protocol_section, ['descriptionModule', 'briefSummary'])

        # Process the interventions
        interventions_descriptions = [
            intervention.get('description', 'Not provided')
            for intervention in interventions_list
            if isinstance(intervention, dict)
        ]
        
        # Summarize the extracted information
        extracted_info = {
            'NCT ID': identification_info.get('nctId', 'Not provided'),
            'Brief Title': identification_info.get('briefTitle', 'Not provided'),
            'Brief Summary': summary_info if summary_info else 'Not provided',
            'Official Title': identification_info.get('officialTitle', 'Not provided'),
            'Conditions': conditions_info if conditions_info else 'Not provided',
            'Interventions Description': interventions_descriptions,
            'Eligibility': {
                'Healthy Volunteers': eligibility_info.get('healthyVolunteers', 'Not provided'),
                'Sex': eligibility_info.get('sex', 'Not provided'),
                'Minimum Age': eligibility_info.get('minimumAge', 'Not provided'),
                'Maximum Age': eligibility_info.get('maximumAge', 'Not provided'),
                'Standard Ages': eligibility_info.get('stdAges', 'Not provided'),
                'Criteria Text ': eligibility_info.get('eligibilityCriteria', 'Not provided')
            }
        }
        
        return extracted_info
    except Exception as e:
        print(f"An error occurred while processing data: {e}")
        # Returning an empty dict to indicate processing failed
        return {}

import textwrap

# Update the function to use the new format_criteria function
def format_clinical_trial_summary(summary):
    """
    Generate a formatted summary for a clinical trial data dictionary,
    skipping any attributes that say 'Not provided'.
    
    :param summary: dict, structured summary of extracted clinical trial information
    :return: str, formatted summary suitable for presentation to a doctor
    """
    # Helper function to format a list with bullet points
    def format_list(items):
        if items:  # Ensure that items is not empty or None
            return "\n".join(f"• {item}" for item in items if item != 'Not provided')
        return ""

    # Helper function to wrap text for better readability
    def wrap_text(text, width=80):
        return "\n".join(textwrap.wrap(text, width=width))

    # Start building the formatted summary
    formatted_summary = "Clinical Trial Summary:\n\n"

    # Add identification information if provided
    if summary['NCT ID'] != 'Not provided':
        formatted_summary += f"NCT ID: {summary['NCT ID']}\n"
    if summary['Brief Title'] != 'Not provided':
        formatted_summary += f"Brief Title: {wrap_text(summary['Brief Title'])}\n"
    if summary['Brief Summary'] != 'Not provided':
        formatted_summary += f"Brief Summary: {wrap_text(summary['Brief Summary'])}\n"
    if summary['Official Title'] != 'Not provided':
        formatted_summary += f"Official Title: {wrap_text(summary['Official Title'])}\n"

    # Add conditions if provided
    conditions_formatted = format_list(summary['Conditions'])
    if conditions_formatted:
        formatted_summary += "Conditions:\n"
        formatted_summary += f"{conditions_formatted}\n\n"

    # Add interventions if provided
    interventions_formatted = format_list(summary['Interventions Description'])
    if interventions_formatted:
        formatted_summary += "Interventions Description:\n"
        formatted_summary += f"{wrap_text(interventions_formatted, width=100)}\n\n"

    # Add eligibility information if provided
    eligibility = summary['Eligibility']
    eligibility_text = []
    for key, value in eligibility.items():
        if value != 'Not provided':
            if key == 'Criteria Text ':
                eligibility_text.append(wrap_text(value, width=100))
            else:
                eligibility_text.append(f"{key}: {wrap_text(str(value))}")
    if eligibility_text:
        formatted_summary += "Eligibility Criteria:\n" + "\n".join(eligibility_text)

    return formatted_summary.strip()

def turn_json_to_valid_metadata(d):
    """
    Recursively go through the dictionary, converting any lists found into comma-separated strings.

    :param d: dict, the dictionary to convert
    :return: dict, the dictionary with lists converted to strings
    """

    # Helper function to wrap text for better readability
    def wrap_text(text, width=80):
        return "\n".join(textwrap.wrap(text, width=width))

    def recurse(value):
        try:
            if isinstance(value, dict):
                return {k: recurse(v) for k, v in value.items()}
            elif isinstance(value, list):
                # Ensure all items in the list can be converted to string
                if all(isinstance(item, (str, int, float, bool, type(None))) for item in value):
                    return ', '.join(str(item) for item in value)
                else:
                    print("Invalid type found in list; skipping list.")
                    return 'Not provided'
            else:
                return value
        except Exception as e:
            print(f"An error occurred during recursion: {e}")
            return 'Not provided'

    json_wo_lists = recurse(d)

    # Turn the eligibility json into a string through summarization
    eligibility_text = json_wo_lists['Eligibility']
    eligibility = d['Eligibility']
    eligibility_text = []
    for key, value in eligibility.items():
        if value != 'Not provided':
            if key == 'Criteria Text ':
                eligibility_text.append(wrap_text(value, width=100))
            else:
                eligibility_text.append(f"{key}: {wrap_text(str(value))}")
    if eligibility_text:
        eligibility_text = "Eligibility Criteria:\n" + "\n".join(eligibility_text)
    else:
        eligibility_text = 'Not provided'
    
    json_wo_lists['Eligibility'] = eligibility_text

    return json_wo_lists

def get_top_5_trials(patient_report):
    """
    Get the top 5 clinical trials through embedding search

    :param patient_report: str, patient report
    :param clinical_trials: list, list of clinical trials
    :return: list, top 5 clinical trials
    """
    # Import Chroma and instantiate a client
    client = chromadb.PersistentClient(path="./vector_db")
    # Create a new Chroma collection to store the supporting evidence. We don't need to specify an embedding fuction, and the default will be used.
    collection = client.get_collection("clinical_trials")
    result = collection.query(
    query_texts=[patient_report],
    n_results=5,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
    )
    documents = result['documents'][0]
    metadata =result['metadatas'][0]

    result = {
        'documents': documents,
        'metadata': metadata
    }

    return result
