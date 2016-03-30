import socket
import threading
import random
import time
host = socket.gethostname()
port = 54321
word = ""
counter = 60
initial = 20
cooldown = 5
winner = ''


# Pick new word every 45 seconds
def Game():
    words = ["reece", "python", "code", "jazz", "rhythm", "counterstrike", "ainsley", "harriot",  # LOTS OF WORDS -->
             'handy', 'planes', 'mist', 'route', 'impossible', 'summer', 'dogs', 'dark', 'young', 'productive', 'play', 'rhythm', 'descriptive', 'straw', 'nifty', 'use', 'reduce', 'fretful', 'ray', 'coil', 'increase', 'psychotic', 'trade', 'slow', 'place', 'memorise', 'middle', 'calculating', 'pale', 'hot', 'bent', 'authority', 'yard', 'whisper', 'nonchalant', 'discover', 'contain', 'noxious', 'adhesive', 'spill', 'notebook', 'substantial', 'sheep', 'appear', 'selection', 'difficult', 'meek', 'profit', 'white', 'diligent', 'carriage', 'rightful', 'trite', 'poised', 'book', 'sneeze', 'post', 'form', 'chemical', 'shirt', 'cautious', 'abrasive', 'learn', 'stone', 'prefer', 'mother', 'nippy', 'umbrella', 'crown', 'tested', 'pump', 'handsome', 'profuse', 'tug', 'frogs', 'reaction', 'drab', 'lake', 'box', 'suppose', 'enchanted', 'hideous', 'conscious', 'rough', 'pets', 'miniature', 'gifted', 'grin', 'abnormal', 'undesirable', 'standing', 'smart', 'deranged', 'number', 'green', 'bumpy', 'top', 'tacky', 'breakable', 'left', 'annoyed', 'tramp', 'celery', 'annoy', 'snotty', 'cry', 'rod', 'meaty', 'swim', 'coach', 'bomb', 'obeisant', 'greet', 'lush', 'stew', 'bridge', 'clap', 'walk', 'sniff', 'replace', 'night', 'ice', 'dramatic', 'eatable', 'correct', 'blush', 'juice', 'lock', 'deadpan', 'witty', 'month', 'scattered', 'rabbits', 'hard', 'messy', 'matter', 'man', 'somber', 'thank', 'concentrate', 'righteous', 'tail', 'cheer', 'muscle', 'gentle', 'damaging', 'savory', 'yam', 'grumpy', 'curvy', 'wretched', 'command', 'bright', 'amusing', 'instruct', 'last', 'excuse', 'wink', 'tan', 'ablaze', 'mom', 'sack', 'chief', 'borrow', 'baby', 'year', 'pipe', 'bushes', 'squealing', 'tiger', 'barbarous', 'record', 'self', 'change', 'wound', 'doctor', 'death', 'aspiring', 'berserk', 'business', 'puzzled', 'complex', 'yummy', 'ultra', 'wrist', 'form', 'admit', 'zoom', 'small', 'stiff', 'uppity', 'cemetery', 'cobweb', 'cheerful', 'guttural', 'expansion', 'quarter', 'selective', 'macabre', 'unlock', 'coil', 'library', 'deer', 'crack', 'trap', 'jail', 'robin', 'afraid', 'terrify', 'waste', 'useless', 'blow', 'shade', 'fertile', 'glow', 'filthy', 'fluffy', 'film', 'flight', 'tickle', 'modern', 'heat', 'blue-eyed', 'regret', 'smiling', 'name', 'sedate', 'side', 'pretty', 'quickest', 'things', 'drown', 'military', 'wild', 'bless', 'eggs', 'pet', 'dangerous', 'horses', 'smell', 'dear', 'punch', 'airport', 'grip', 'smash', 'suggest', 'window', 'cake', 'addition', 'like', 'rhetorical', 'digestion', 'sincere', 'suspend', 'necessary', 'panoramic', 'stain', 'creator', 'marry', 'gold', 'knee', 'vacuous', 'famous', 'trade', 'abrupt', 'friendly', 'attack', 'lucky', 'scientific', 'fascinated', 'baseball', 'peel', 'medical', 'hurried', 'unfasten', 'smile', 'spark', 'rail', 'fry', 'purring', 'equal', 'dock', 'ambitious', 'dinner', 'distance', 'rhyme', 'straight', 'hose', 'hope', 'spring', 'miscreant', 'match', 'fool', 'previous', 'questionable', 'cactus', 'prickly', 'horse', 'sharp', 'unite', 'level', 'seemly', 'truculent', 'imported', 'overt', 'stingy', 'axiomatic', 'try', 'shaky', 'ground', 'bottle', 'switch', 'question', 'offer', 'cough', 'taste', 'throat', 'dead', 'ill-informed', 'cast', 'board', 'amazing', 'dog', 'drip', 'feeble', 'fierce', 'responsible', 'few', 'adamant', 'smell', 'versed', 'tangy', 'pleasant', 'pot', 'recognise', 'fact', 'dolls', 'useful', 'act', 'mouth', 'highfalutin', 'joke', 'helpful', 'gruesome', 'quick', 'spicy', 'bump', 'enjoy', 'floor', 'immense', 'receipt', 'wiggly', 'sisters', 'scene', 'foot', 'fortunate', 'swanky', 'stir', 'fuzzy', 'sordid', 'flippant', 'damage', 'quiet', 'curious', 'gun', 'current', 'stitch', 'pray', 'sidewalk', 'thundering', 'branch', 'show', 'shop', 'boot', 'pricey', 'tow', 'wry', 'existence', 'desert', 'stick', 'travel', 'precious', 'earth', 'light', 'reflect', 'quixotic', 'threatening', 'prose', 'tearful', 'willing', 'wax', 'permissible', 'soothe', 'reign', 'structure', 'hunt', 'quack', 'bruise', 'own', 'battle', 'slim', 'question', 'boundless', 'delicious', 'omniscient', 'battle', 'chance', 'mountain', 'match', 'redundant', 'lumpy', 'drain', 'eminent', 'steep', 'ski', 'phone', 'doll', 'paste', 'flash', 'wish', 'bitter', 'scare', 'hospital', 'drawer', 'efficacious', 'copy', 'vivacious', 'square', 'late', 'eggnog', 'strange', 'enormous', 'time', 'collar', 'ocean', 'awesome', 'detail', 'loose', 'change', 'soap', 'pinch', 'noiseless', 'stocking', 'base', 'chase', 'marvelous', 'mundane', 'neighborly', 'long-term', 'greasy', 'look', 'remain', 'detect', 'release', 'special', 'church', 'crow', 'invent', 'gate', 'introduce', 'chunky', 'silk', 'yak', 'tongue', 'retire', 'kneel', 'bird', 'meddle', 'frame', 'queen', 'follow', 'steer', 'fade', 'sick', 'physical', 'test', 'incandescent', 'add', 'old-fashioned', 'purpose', 'cook', 'pointless', 'numberless', 'harass', 'boat', 'jewel', 'swing', 'zephyr', 'successful', 'yell', 'notice', 'remarkable', 'sail', 'tire', 'glamorous', 'workable', 'tasteless', 'record', 'representative', 'educated']
    global word
    global counter
    global initial
    global cooldown
    global winner
    while 1:
        print(initial+cooldown+counter)
        if initial == 0:
            if cooldown <= 1:
                if cooldown:
                    if counter == 60:
                        word = random.choice(words)
                        winner = ''
                        print(word)
                        cooldown -= 1
                    continue
                time.sleep(1)
                counter -= 1
                if counter == 0:
                    counter = 60
                    cooldown = 5
            else:
                cooldown -= 1
                time.sleep(1)
        else:
            initial -= 1
            time.sleep(1)


def handler(c, addr):
    global word
    global counter
    global initial
    global cooldown
    global winner
    while 1:
        try:
            data = c.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            print(str(addr) + " recv: " + data)
            split = data.split(':')
            # If data is a tagged message
            if split[0][0] == '#':
                # Login
                if split[0] == "#login" and len(split) == 3:
                    with open("logins.txt", 'r') as f:
                        lines = [x.strip('\n') for x in f.readlines() if x != '\n']
                    if "{},{}".format(split[1], split[2]) in lines:
                        c.send("#loggedin".encode('utf-8'))
                    else:
                        c.send("#error:badlogin".encode('utf-8'))
                # Signup
                elif split[0] == "#signup" and len(split) == 3:
                    with open("logins.txt", 'r') as f:
                        lines = [x.strip('\n').split(',') for x in f.readlines() if x != '\n']
                    if not [x for x in lines if x[0] == split[1]]:
                        lines.append([split[1], split[2]])
                        with open("logins.txt", 'w') as f:
                            f.write('\n'.join([','.join(x) for x in lines]))
                        c.send("#signedup".encode('utf-8'))
                    else:
                        c.send("#error:conflict".encode('utf-8'))
                # Request word
                elif split[0] == "#getword":
                    print("sending", word.encode('utf-8'))
                    c.send(word.encode('utf-8'))
                elif split[0] == "#gettime":
                    if initial or cooldown or not word:
                        c.send(str(60).encode('utf-8'))
                    else:
                        c.send(str(counter).encode('utf-8'))
                elif split[0] == "#finished":
                    if not winner:
                        winner = split[1]
                    c.send("#winner:{}".format(winner).encode('utf-8'))
                elif split[0] == "#lost":
                    c.send("#winner:{}".format(winner).encode('utf-8'))
            if "close" == data:
                break

        except Exception as e:
            print(e)
            break

    c.close()
    print(addr, "- closed connection")

server = (host, port)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(server)

s.listen(5)

game_t = threading.Thread(target=Game)
game_t.start()

while 1:
    print("listening on", host, port)
    client, address = s.accept()
    print("... connected from", address)
    t = threading.Thread(target=handler, args=(client, address))
    t.start()
