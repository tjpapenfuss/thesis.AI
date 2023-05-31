import spacy

# There are multiple available models, this one loads a lightweight version
# More info here: https://spacy.io/models/en
model_name = 'en_core_web_sm' 

try:
    nlp = spacy.load(model_name)
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)")
    from spacy.cli import download
    download(model_name)
    nlp = spacy.load(model_name)

# Function to add an org name to the nlp pipeline
def add_entity(org, pipeline):
  """Adds an org as a named entity to a spacy nlp pipeline"""
  ruler = nlp.add_pipe("entity_ruler")
  patterns = [{"label": "ORG", "pattern": org}]
  ruler.add_patterns(patterns)

# To run above write code similar to below
#add_entity('Amazon', nlp)
#add_entity('Amazon Web Services', nlp)
#add_entity('AWS', nlp)

# Load up the raw text
text = "products email security and resiliencemost popular world-class efficacy, total deployment flexibility — with or without a gateway security awareness and user behavior award-winning training, real-life phish testing, employee and organizational risk scoring data retention and compliance industry-leading archiving, rapid data restoration, accelerated e-discovery get started mimecast plans email security, cloud integrated solutions secure your emailmost popular business email compromise brand impersonation ransomware more solutions data governance cyber awareness by platform google workspace microsoft 365 partners partner overview become a partner integrate with mimecast technology & alliance partners partner portal resource center analyst reports e-books whitepapers webinars more resources blog cybersecurity glossary threat intelligence hub for customers technical support knowledge hub featured the state of email security 2023 cyber risk and the c-suite in the state of email security about us company overview leadership team awards esg & global impact customer success stories trust center careers join the team help us build a better business for our people & customers. news & events secops virtual 2023 now available on-demand mimecast announces appointment of new chief financial officer tenancy deposit scheme tds gets a new lease on cybersecurity with mimecast solution problem benefit at a glance customer vision when alex hillier joined tds three years ago as the head of it, he realized there was a pressing need to upgrade his current cybersecurity solutions. alex and his small internal cybersecurity team realized they needed to consolidate their infrastructure and engage a cybersecurity solution provider that offered more robust email, web security and archiving/sync/recovery while seamlessly working within the microsoft office 365 suite. “i’ve known about mimecast for more than 10 years and first heard of its solutions when i was head of it for a large housing association. i’ve always thought highly of the company and its breadth of security suite products,” says alex. customer strategy alex evaluated several technology solutions, including proofpoint, cisco and smaller cybersecurity vendors, but kept coming back to mimecast. the company’s enterprise-level security tools really impressed him, particularly its archiving capabilities, which his former email security provider did not provide. archiving is vital to tds’ line of work, due to its authorization to litigate landlord-tenant disputes, which requires the ability to access archived documents to settle these disputes.. mimecast’s cloud archive solution provides guaranteed email retention, which cannot be deleted by end users and helps company meet its e-discovery and compliance obligations. “mimecast stood out among its competitors with its email filtering, archiving and outlook plugins,” he says. “mimecast’s extensive archiving and security solutions were a key factor in our decision to select mimecast for our overall security needs.”customer outcome tds’ managed service provider easily deployed mimecast, thanks to its easy-to-use plugins. and since the deployment, tds is better prepared to defend its company from standard phishing attacks and data loss. “we were able to consolidate our cybersecurity, security awareness training, email and web security and archiving needs by deploying mimecast, and we’re very happy with the outstanding protection, ease-of-use and seamless deployment,” says alex. “and in the end, switching to mimecast has saved our organization money.” “we were able to consolidate our cybersecurity, security awareness training, email and web security and archiving needs by deploying mimecast and we’re very happy with the outstanding protection, ease-of-use and seamless deployment. and in the end, switching to mimecast has saved our organization money. alex hillier director of technology, tds download your case study now about us products resource center contact us © 2003 - 2023 mimecast services limited"
# Run the raw text through the nlp pipeline process
doc = nlp(text)

# Some sort of loop to look through the doc
# The below checks every word in the doc to see if they are proper nouns

for w in doc:
  if w.tag_ == 'NNP':
    if w.ent_iob_ == 'B': # This means that the word is the beginning of a new entity (not a continuation from the previous word)
      print()             # So if it's a new entity, it goes to a new line
    print(w, end = ' ')   # If not, it will extend the previous entity