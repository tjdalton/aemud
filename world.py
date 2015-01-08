import globals
class World:
	
	def __init__(self):
		self.rooms = {}
		self.rooms["START"] = globals.room.Room("START","A boring starting room")
		
	def findRoomByID(self,id):
		try:
			return self.rooms[id]
		except KeyError:
			return None
	def tick(self):
		print "tick"