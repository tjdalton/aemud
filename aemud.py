from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, task

import globals
from commands import Commands

commands = Commands()	
class Chat(LineReceiver):
    def __init__(self, users):
		self.users = users
		self.name = None
		self.state = "GETNAME"
		self.room = globals.world.rooms["START"]
		self.room.mobs[self.name] = self
		self.description = "A person."
    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_INPUT(line)

    def handle_GETNAME(self, name):
		if self.users.has_key(name):
			self.sendLine("Name taken, please choose another.")
			return
		self.sendLine("Welcome, %s!" % (name,))
		self.name = name
		self.users[name] = self
		self.state = "CHAT"
		self.room.enterRoom(self,self.room)

    def handle_INPUT(self, message):
		input = message.split(" ");
		function = getattr(commands,input[0].lower(), commands.move)
		line = function(self,input)
		if line != "" and line != None:
			self.sendLine(line)


class ChatFactory(Factory):

	def __init__(self):
		self.users = {} # maps user names to Chat instances
		self.lc = task.LoopingCall(globals.world.tick)
		self.lc.start(1)
	def buildProtocol(self, addr):
		return Chat(self.users)
		
reactor.listenTCP(8123, ChatFactory())
reactor.run()
