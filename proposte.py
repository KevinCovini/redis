import redis as rd
import re
import time
import pandas as pd


r = rd.Redis(
    host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=12900,
    password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb')

''' Templates

macchinette = {
    titolo: "macchinette",
    descrizione: "macchinette buone",
}

macchinette_proponenti = set(
    "Pippo",
    "Paperino",
    "Pluto"
)

macchinette_votanti = set(
    "Pippo",
    "Paperino",
    "Pluto"
)

'''


def insertProposal(p_number=1):
    for n in range(p_number):
        proposers = re.sub(r"[^\w\s]", "", input(
            "Insert name(s) of the proposer(s): ")).split()
        proposal_title = input("Insert the title of the proposal: ")
        proposal_desc = input("Insert the description of the proposal: ")
        r.hset(f"{proposal_title} proposta", mapping={
            "Titolo": proposal_title,
            "Descrizione": proposal_desc
        })
        for prop in proposers:
            r.sadd(f"{proposal_title} proponenti", prop)


def showProposal():
    for i, key in enumerate(r.keys("*proposta")):
        print(f"{i+1}. {r.hgetall(key)[b'Titolo'].decode()} (", end="")
        for prop in r.smembers(f"{key.decode()[:-8]}proponenti"):
            print(prop.decode(), end=", ")
        print(")", end=": ")
        try:
            print(r.scard(f"{key.decode()[:-8]}votanti"), end=" voti\n")
        except ValueError:
            print("0 voti\n")

def voteProposal():
    # inserisci cognome (login)
    # inserisci id proposta
    # se hai già votato la proposta vai a fare in culo
    # altrimenti: cognome -> db (proposta.lista votanti), voti+=1

    cognome = input("Insert last name: ")
    proposal_id = input("Insert proposal ID: ")

    if r.sismember(f"voters:{proposal_id}", cognome):
        print("You already voted this proposal.")
    else:
        r.sadd(f"voters:{proposal_id}", cognome)
        r.hincrby(f"proposal:{proposal_id}", "votes")


if __name__ == "__main__":
    # insertProposal()
    showProposal()
