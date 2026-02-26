from mcpi.minecraft import Minecraft
from mcpi import block
import time
import math
import paho.mqtt.client as mqtt
from appel_pouvoirs import BP_index, BP_majeur, BP_annulaire, BP_auriculaire, mega_pouvoir

# Connexion à Minecraft
mc = Minecraft.create()

# Chronomètre pour limiter les malus
last_malus_time = time.time()

# Identification des joueurs
players = mc.getPlayerEntityIds()
if len(players) >= 2:
    user1 = players[0]  # Premier joueur
    user2 = players[1]  # Deuxième joueur
else:
    mc.postToChat("Two players must be connected to use powers.")
    exit()

# Associer les noms aux IDs des joueurs
player_names = {
    user1: "user1",
    user2: "user2"
}

# Texte d'introduction en anglais
mc.postToChat("Welcome to the game!")
mc.postToChat("The rules are simple: Find the diamond before your opponent.")
mc.postToChat("You can use superpowers and traps against your opponent.")
mc.postToChat("Traps can only be used every 10 seconds.")
mc.postToChat("To win the game, stand on the diamond and activate the mega power!")

# Calculer la position centrale pour le diamant
player1_pos = mc.entity.getTilePos(user1)
player2_pos = mc.entity.getTilePos(user2)
diamond_x = (player1_pos.x + player2_pos.x) // 2
diamond_y = (player1_pos.y + player2_pos.y) // 2
diamond_z = (player1_pos.z + player2_pos.z) // 2

# Placer le diamant
mc.setBlock(diamond_x, diamond_y, diamond_z, block.DIAMOND_BLOCK)
mc.postToChat("A diamond has been placed! Find it to win the game!")

# Fonction pour trouver l'adversaire
def get_adversaire(player_id):
    """Retourne l'ID de l'adversaire."""
    return user2 if player_id == user1 else user1

# Fonction pour calculer la distance entre un joueur et le diamant
def distance_to_diamond(player_id):
    player_pos = mc.entity.getTilePos(player_id)
    return math.sqrt((player_pos.x - diamond_x) ** 2 + (player_pos.y - diamond_y) ** 2 + (player_pos.z - diamond_z) ** 2)

# Fonction pour vérifier la direction du joueur
def check_direction(player_id, prev_distance):
    curr_distance = distance_to_diamond(player_id)
    print(f"Player {player_names[player_id]}: Previous Distance = {prev_distance}, Current Distance = {curr_distance}")
    if curr_distance < prev_distance:
        mc.postToChat(f"{player_names[player_id]} is getting closer to the diamond!")
    elif curr_distance > prev_distance:
        mc.postToChat(f"{player_names[player_id]} is getting farther from the diamond!")
    return curr_distance

# Gestion de la connexion MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("gant1/#")
    client.subscribe("gant2/#")

# Gestion des messages MQTT
def on_message(client, userdata, msg):
    topic = msg.topic
    print(f"Message reçu : {topic}")
    if topic == "gant1/index":
        BP_index(mc, user1)
    elif topic == "gant1/majeur":
        BP_majeur(mc, user1, user2)
    elif topic == "gant1/annulaire":
        BP_annulaire(mc, user1)
    elif topic == "gant1/auriculaire":
        BP_auriculaire(mc, user1, user2)
    elif topic == "gant2/index":
        BP_index(mc, user2)
    elif topic == "gant2/majeur":
        BP_majeur(mc, user2, user1)
    elif topic == "gant2/annulaire":
        BP_annulaire(mc, user2)
    elif topic == "gant2/auriculaire":
        BP_auriculaire(mc, user2, user1)

# Initialisation du client MQTT
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("rpi", "craft") #Connexion sécurisée avec mot de passe
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()  # Démarre le client MQTT en mode non bloquant

# Boucle principale du jeu
game_running = True
winner_id = None
prev_distance_user1 = distance_to_diamond(user1)
prev_distance_user2 = distance_to_diamond(user2)

while game_running:
    for player_id in players:
        # Vérifier si un joueur est au-dessus du diamant
        player_pos = mc.entity.getTilePos(player_id)
        print(f"Player {player_names[player_id]} position: {player_pos}")
        if (player_pos.x == diamond_x and
            player_pos.z == diamond_z and
            player_pos.y == diamond_y + 1):
            print(f"Player {player_names[player_id]} is on the diamond!")
            winner_id = player_id
            game_running = False
            break

        # Vérifier si le joueur se rapproche ou s'éloigne du diamant
        if player_id == user1:
            prev_distance_user1 = check_direction(player_id, prev_distance_user1)
        elif player_id == user2:
            prev_distance_user2 = check_direction(player_id, prev_distance_user2)

    # Pause pour éviter une surcharge CPU
    time.sleep(1)

# Annonce du gagnant
if winner_id:
    winner_name = player_names[winner_id]
    mc.postToChat(f"{winner_name} has won by standing on the diamond!")
    # Supprimer le diamant
    mc.setBlock(diamond_x, diamond_y, diamond_z, block.AIR)
    mega_pouvoir(mc, winner_id, player_names)  # Activer le mega pouvoir
else:
    mc.postToChat("No one won the game.")
