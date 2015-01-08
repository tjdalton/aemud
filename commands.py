import globals

class Commands:
	def move(self,player,input):
		try:
			exit = player.room.exits[input[0].lower()]
			player.room.enterRoom(player,exit)
		except:
			return "Unknown command"
	def dig(self,player,input):
		if len(input) < 3:
			return "DIG: DIG <direction> <room ID>"
		newroom = globals.world.findRoomByID(input[2].upper())
		if newroom is None:
			return "Room {} does not exist".format(input[2].upper())
		else:
			return player.room.addExit(input[1].lower(), newroom)
			
	def create(self,player,input):
		if len(input) < 3:
			return "CREATE: CREATE <room id> <description>"
		globals.world.rooms[input[1].upper()] = globals.room.Room(input[1].upper()," ".join(input[2:]))
		return "Room {} created.".format(input[1].upper())
		
	def look(self,player, input):
		player.sendLine(player.room.description)
		if len(player.room.exits) > 0:
				player.sendLine("There are exits to the:")
		listexits = []
		for dir in player.room.exits:
			listexits.append(dir)
		player.sendLine(", ".join(listexits))
	l = look

	def help(self,player,input):
		if len(input) < 2:
			return "HELP: HELP <command>"
		try:
			function = getattr(self,input[1])
			if input[1] == "help":
				raise AttributeError
			return function(player,input)
		except AttributeError:
			return self.help(player,input[1])
			
	def commands(self,player,input):
		dict = Commands.__dict__
		commands = []
		for item in dict:
			if callable(dict[item]):
				commands.append(item.upper())
		return "Available commands: " + " ".join(commands)
	def quit(self,player,input):
		player.transport.loseConnection()
		
