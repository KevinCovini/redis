import redis as rd
import re
import time
import pandas as pd

# Connessione al DB Redis
r = rd.Redis(
    host='redis-12900.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=12900,
    password='uUlKJLiadqj12nYHVKcwK9TowwyuXrvb'
)

''' Esempio Templates

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
    '''Funzione di inserimento proposta richedendo queste info:
    Proponenti (chi fa la proposta), titolo e descrizione.
    La proposta verrà scritta in un hash e i proponenti in un set separato.
    '''
    for n in range(p_number):
        proposers = re.sub(r"[^\w\s]", "", input(
            "Inserisci cognome/i dei proponenti: ")).split()
        proposal_title = input("Inserisci il nome della proposta: ")
        proposal_desc = input("Inserisci la descrizione della proposta: ")
        r.hset(f"{proposal_title} proposta", mapping={
            "Titolo": proposal_title,
            "Descrizione": proposal_desc
        })
        for prop in proposers:
            r.sadd(f"{proposal_title} proponenti", prop)


def showProposal():
    '''Stampa tutte le proposte inserite in DB'''
    for i, key in enumerate(r.keys("*proposta")):
        print(f"{i+1}. {r.hgetall(key)[b'Titolo'].decode()} (", end="")
        for prop in r.smembers(f"{key.decode()[:-8]}proponenti"):
            print(prop.decode(), end=", ")
        print(")", end=": ")
        try:
            print(r.scard(f"{key.decode()[:-8]}votanti"), end=" voti\n")
        except ValueError:
            print("0 voti\n")
    print("\n")

def voteProposal():
    '''Richiede Cognome e ID proposta per inserire la votazione di essa:
    se la proposta è già stata votata non viene effettuata nessuna operazione sul DB;
    Se la proposta non è già stata votata verrà inserita la votazione per la proposta corrispondente.
    '''

    name = input("Insert last name: ")
    proposal_name = input("Insert proposal name: ")

    if r.sismember(f"{proposal_name} votanti", name):
        print("You already voted this proposal.")
    else:
        r.sadd(f"{proposal_name} votanti", name)
        showProposal()
    print("\n")
    
def descProposal():
    for i, key in enumerate(r.keys("*proposta")):
        print(f"{i+1}. {r.hgetall(key)[b'Titolo'].decode()}", end=" (")
        print(f"{r.hgetall(key)[b'Descrizione'].decode()})")
    print("\n")

if __name__ == "__main__":
    while True:
        showProposal()
        while True:
            try:
                print("1. Vedi le descrizioni delle proposte")
                print("2. Vota una proposta")
                print("3. Crea una proposta")
                print("4: Esci")
                print("\n")
                choice = int(input("Cosa vuoi fare: "))
                print("\n")
            except ValueError:
                print("Valore non accettato. Riprova")
                continue
            else:
                break
            

        match choice:
            case 1:
                descProposal()
            case 2:
                voteProposal()
            case 3:
                insertProposal()
            case 4:
                break