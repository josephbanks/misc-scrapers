import requests
import json
from bs4 import BeautifulSoup

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

states = [states[state].lower().replace(' ', '-') for state in states]
states.sort()

categories = ['medicaid',
              'private-payer-laws',
              'professional-regulationhealth-safety'
             ]

medicaid_live_video = ['live-video-policy', 
              'live-video-eligible-servicesspecialties',
              'live-video-eligible-providers',
              'live-video-eligible-sites',
              'live-video-geographic-limits',
              'live-video-facilitytransmission-fee'
             ]

medicaid_store_forward = ['store-and-forward-policy',
                 'store-and-forward-eligible-servicesspecialties',
                 'store-and-forward-geographic-limits',
                 'store-and-forward-transmission-fee'
                ]

medicaid_remote_patient = ['remote-patient-monitoring-policy',
                  'remote-patient-monitoring-conditions',
                  'remote-patient-monitoring-limitations',
                  'remote-patient-monitoring-restrictions'
                 ]

medicaid = ['summary',
            'definition',
            'definitions', 
            medicaid_live_video, 
            medicaid_store_forward, 
            medicaid_remote_patient, 
            'emailphonefax',
            'consent',
            'out-state-providers',
            'miscellaneous'
           ]

privatepayer = ['definition',
                'definitions'
                'consent',
                'parity'
               ]

professional = ['definition',
                'definitions',
                'consent',
                'prescribing',
                'cross-state-licensing',
                'miscellaneous'
               ]

format_link = 'https://www.cchpca.org/telehealth-policy/current-state-laws-and-reimbursement-policies/{}-{}-{}'

def get_text(soup):
    paragraph_tag = 'c-law__info__description' # 'paragraph paragraph--type--law-info paragraph--view-mode--default c-law__info'
    text = []
    for paragraph in soup.findAll('div', class_=paragraph_tag):
        text.append(paragraph.text.strip())
    string = ''
    for el in text:
        string += el + ' '
    return string

def harvest(states, categories, medicaid, privatepayer, professional, file):
    format_link = 'https://www.cchpca.org/telehealth-policy/current-state-laws-and-reimbursement-policies/{}-{}-{}'
    state_json = {}
    for state in states:
        category_json = {}
        for category in categories:
            sub_type = None
            if category == 'medicaid':
                sub_type = medicaid
            elif category == 'private-payer-laws':
                sub_type = privatepayer
            else:
                sub_type = professional
            item_json = {}
            for item in sub_type:
                if type(item) == list:
                    sub_json = {}
                    for sub in item:
                        url = format_link.format(state, category, sub)
                        page = requests.get(url)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        text = get_text(soup)
                        if text:
                            sub_json[sub] = text
                            print('.', end='')
                    if item[0] == 'live-video-policy':
                        item_json['medicaid live video'] = sub_json
                    elif item[1] == 'store-and-forward-policy':
                        item_json['medicaid_store_forward'] = sub_json
                    else:
                        item_json['medicaid_remote_patient'] = sub_json
                else:
                    url = format_link.format(state, category, item)
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    text = get_text(soup)
                    if text:
                        item_json[item] = text
                        print('.', end='')
            category_json[category] = item_json
        state_json[state] = category_json
    json.dump(state_json, outputfile, indent=2)


filename = 'states.json' # change file name
statename = 'alabama'

with open(filename, 'w') as outputfile:
    harvest(states, categories, medicaid, privatepayer, professional, outputfile) # This will do all states
    # harvest([statename], categories, medicaid, privatepayer, professional, outputfile) # This will collect alabama