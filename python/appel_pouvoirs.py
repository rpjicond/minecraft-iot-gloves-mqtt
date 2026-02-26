from mcpi import block
import time

# Variable globale pour limiter les malus
last_malus_time = time.time()

def BP_index(mc, user1):
    """Superpouvoir : Creuser un trou sous le joueur."""
    try:
        pos = mc.entity.getTilePos(user1)
        mc.setBlock(pos.x, pos.y - 1, pos.z, 0)
        mc.postToChat("Superpower activated: Dig a hole (Index).")
    except Exception as e:
        mc.postToChat(f"Error in BP_index: {e}")

def BP_majeur(mc, user1, user2):
    """Malus : Creer un mur de lave autour de l'adversaire."""
    global last_malus_time
    try:
        if time.time() - last_malus_time >= 10:
            adversaire_id = user2 if user1 == user1 else user1
            adversaire_pos = mc.entity.getTilePos(adversaire_id)
            for x in range(adversaire_pos.x - 1, adversaire_pos.x + 2):
                for z in range(adversaire_pos.z - 1, adversaire_pos.z + 2):
                    mc.setBlock(x, adversaire_pos.y, z, 11)  # Lave
            last_malus_time = time.time()
            mc.postToChat("Trap activated: Lava wall (Major).")
        else:
            mc.postToChat("Trap not available. Wait 10 seconds.")
    except Exception as e:
        mc.postToChat(f"Error in BP_majeur: {e}")

def BP_annulaire(mc, user1):
    """Superpouvoir : Creer un ascenseur d'eau."""
    try:
        pos = mc.entity.getTilePos(user1)
        mc.setBlock(pos.x, pos.y + 1, pos.z, 8)
        mc.postToChat("Superpower activated: Water elevator (Annular).")
    except Exception as e:
        mc.postToChat(f"Error in BP_annulaire: {e}")

def BP_auriculaire(mc, user1, user2):
    """Superpouvoir : Creer un mur de TNT autour de l'adversaire."""
    global last_malus_time
    try:
        if time.time() - last_malus_time >= 10:
            adversaire_id = user2 if user1 == user1 else user1
            adversaire_pos = mc.entity.getTilePos(adversaire_id)
            for x in range(adversaire_pos.x - 1, adversaire_pos.x + 2):
                for z in range(adversaire_pos.z - 1, adversaire_pos.z + 2):
                    mc.setBlock(x, adversaire_pos.y, z, 46)  # TNT
            last_malus_time = time.time()
            mc.postToChat("Superpower activated: TNT wall (Auricular).")
        else:
            mc.postToChat("Trap not available. Wait 10 seconds.")
    except Exception as e:
        mc.postToChat(f"Error in BP_auriculaire: {e}")

def mega_pouvoir(mc, player_id, player_names):
    """Active un mega pouvoir pour le gagnant."""
    try:
        player_pos = mc.entity.getTilePos(player_id)
        # Crée un anneau de blocs de glowstone autour du joueur
        for x in range(-3, 4):  # Boucle pour créer un anneau de 7x7
            for z in range(-3, 4):
                mc.setBlock(player_pos.x + x, player_pos.y, player_pos.z + z, 89)  # Bloc de glowstone
        time.sleep(0.1)
        mc.postToChat(f"Mega power activated: {player_names[player_id]} !")
    except Exception as e:
        mc.postToChat(f"Error in mega_pouvoir: {e}")
