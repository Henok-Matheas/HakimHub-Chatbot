import requests
from bs4 import BeautifulSoup
import sys
import os

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, "../../utils"))
import file_handlers


def get_symptoms(urls):
    total_symptoms = []

    for url in urls:
        symptoms = []
        # Send a GET request to the URL
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')


        # Find the <h2> tag with text = Symptoms
        h2_tag = soup.find('h2', string='Symptoms')

        if not h2_tag:
            print("No symptoms found for {}".format(url))
            continue

        # Find the <ul> tag below the <h2> tag
        ul_tag = h2_tag.find_next_sibling(name = 'ul')

        if not ul_tag:
            print("No symptoms found for {}".format(url))
            continue


        for li_tag in ul_tag.find_all('li'):
            strong_tag = li_tag.find('strong')

            if strong_tag:
                symptoms.append(strong_tag.text)
            else:
                symptoms.append(li_tag.text)
        
        if not symptoms:
            raise Exception("No symptoms found")
        
        total_symptoms.append(symptoms)

    return total_symptoms

def main(inputFile, outFile):
    specs_with_url = file_handlers.load_json(inputFile)
    specs_with_symptoms = []
    for spec_with_url in specs_with_url:
        specialization = spec_with_url['specialization']
        url = spec_with_url['url']

        symptoms = get_symptoms(url)

        spec_with_symptoms = {
        "specialization": specialization,
        "symptoms": symptoms
        }

        specs_with_symptoms.append(spec_with_symptoms)

    file_handlers.dump_json(specs_with_symptoms, outFile)



if __name__ == '__main__':
    inputFile = os.path.join(current_dir, 'specalizations-with-url.json')
    outFile = os.path.join(current_dir, "specializations-with-symptoms.json")
    specs_with_url = main(inputFile = inputFile, outFile = outFile)
