import redis as rd
import re
import time
import pandas as pd



r = rd.Redis(
  host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12900,
  password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb')

''' Templates
PROPOSAL_TEMPLATE = {
    "id" : id
    "proposers" : [
        "Pippo",
        "Paperino",
        "Pluto"
    ],
    "proposal_title" : "title of the proposal",
    "proposal_description" : "description of the proposal",
    "votes" : 0
}
'''

try:
    proposal_key = int(r.get("proposal_key"))
except TypeError:
    r.set("proposal_key", 0)
    proposal_key = 0
print(f"Current proposal key: {proposal_key}")  

    
def insertProposal(p_number = 1):
    for n in range(p_number):
      proposers = re.sub(r"[^\w\s]", "", input("Insert name(s) of the proposer(s): ")).split()
      proposal_title = input("Insert the title of the proposal: ")
      proposal_desc = input("Insert the description of the proposal: ")
      for n in range(len(proposers)):
          r.rpush(f"proposers:{proposal_key}", proposers[n])
      r.hmset(f"proposal:{proposal_key}", {
          "proposers": f"proposal:{proposal_key}",
          "proposal_title": proposal_title,
          "proposal_description": proposal_desc,
          "Votes": 0
          })
      r.incr("proposal_key")

def voteProposal():
    for n in range(int(r.get("proposal_key"))):
        proposal_dict = r.hgetall(f"proposal:{n}")
        proposers = r
        proposal_str = f'''
            Proposta: {proposal_dict["proposal_title"]}
            Descrizione:
            Autori:
            Voti:
        '''
        print(proposal_dict)



if __name__ == "__main__":
    '''
    print("Start")
    voteProposal()
    r.flushall()
    '''