import json

# Opening JSON file
jsonFile = open("data.json")
data = json.load(jsonFile)

def commonMember(first_list, sencond_list):
    first_list_set = set(first_list)
    sencond_list_set = set(sencond_list)
 
    if (first_list_set & sencond_list_set):
        return True
    else:
        return False

def alphExists(alph):
    return alph in data["alpha"]

def stateExists(state):
    for currentState in data["states"]:
        if state == currentState["name"]:
            return True
    return False

def findState(state):
    for currentState in data["states"]:
        if state == currentState["name"]:
            return currentState
    return False

def findNextStates(currentState, connector):
    states = []
    # Iterar por cada conexao do estado informado
    for connection in currentState["connections"]:
    # Inserir estado em um array caso o estado tenha uma conexao com a entrada informada
        if connector in connection["conector"]:
            states.append(connection["to"])
        
        if "e" in connection["conector"]:
            eState = findState( connection["to"] )
            if False == eState:
                continue
            nextStates = findNextStates( findState( connection["to"] ), connector )
            if 0 == len(nextStates):
                if eState in data['endStates']:
                    return True
            else:
                states.extend( nextStates )
    return states

def iterate(states, conector):
    connections = []
    for state in states:
        nextStates = findNextStates( findState( state ), conector)
        if 0 == len( nextStates ) and state in data['endStates']:
            return True
        connections.extend( nextStates )
    return connections

# Início
if False == stateExists(data["startState"]):
    print("Estado inicial não existe.")

exits = {"outputs": []}
# Para cada cadeia de entrada
for entry in data["entries"]:
    length = len(entry)
    currentStates = []
    currentStates.append( data["startState"] )
    count = 0
    for conector in entry:
        count += 1
        nextStates = iterate(currentStates, conector)
        if True == nextStates:
            print("Aceita")
            exits['outputs'].append({ 'entry': entry, 'response': True})
            break

        print(nextStates)
        currentStates.clear()
        currentStates.extend(nextStates)
        if count == length:
            if commonMember( nextStates, data['endStates'] ):
                print("Aceita")
                exits['outputs'].append({ 'entry': entry, 'response': True})
            else:
                print("Rejeita")
                exits['outputs'].append({ 'conector': entry, 'response': False})
    nextStates.clear()
with open('outputs.json', 'w') as f:
  f.write(str(exits))       
jsonFile.close()