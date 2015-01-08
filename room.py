import globals

directions = {"nw":"se", "se":"nw", "e":"w", "w":"e", "s":"n", "n":"s", "ne":"sw","sw":"ne"}
class Room:
	def __init__(self, id, description):
		self.description = description
		self.id = id
		self.exits = {}
		self.mobs = {}
		self.items = {}
		self.test = globals.world
		
	def addExit(self, direction, room):
		self.exits[direction] = room
		try:
			room.exits[directions[direction]]
		except KeyError:
			otherside = globals.world.findRoomByID(room.id)
			otherside.addExit(directions[direction],self)
		return "An exit to the {}  leading to {} has been created".format(direction,room.description)
	def addMob(self, mob):
		self.mobs[mob.id] = mob
		
	def enterRoom(self,player,room):
		player.room = room
		for name, protocol in player.users.iteritems():
			if protocol.room == player.room and len(room.mobs) > 1:
				if protocol == player:
					protocol.sendLine("You see another person here")
				if protocol != player:
					protocol.sendLine("A {} enters".format(player.description))
			if protocol == player:
				protocol.sendLine(player.room.description)
		if len(player.room.exits) > 0:
			player.sendLine("There are exits to the:")
		listexits = []
		for dir in player.room.exits:
			listexits.append(dir)
			
		player.sendLine(", ".join(listexits))