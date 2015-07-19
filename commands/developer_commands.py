# This module contains commands useful for developers.

from commands.command import *
from evennia.utils import search

class TempCmd(Command):
    '''
    A temporary developer command to do something.
    This one is used to reinitialize objects and locations for
        location tracking testing.
    '''
    key = "reset"
    locks = "cmd:perm(Wizards)"
    help_category = "development"

    def func(self):
        self.caller.execute_cmd("@py self.db.location_objects_nearby = [self.search('Frito')]")
        self.caller.execute_cmd("@py self.db.objects_nearby = [self.search('Frito')]")
        self.caller.execute_cmd("@py self.search('Frito').db.location_objects_nearby = [self]")
        self.caller.execute_cmd("@py self.search('Frito').db.objects_nearby = [self]")
        self.caller.execute_cmd("@py self.search('BeefSupreme').db.location_objects_nearby = [self.search('#25')]")
        self.caller.execute_cmd("@py self.search('BeefSupreme').db.objects_nearby = [self.search('#25')]")
        self.caller.execute_cmd("@py self.search('#25').db.location_objects_nearby = [self.search('BeefSupreme')]")
        self.caller.execute_cmd("@py self.search('#25').db.objects_nearby = [self.search('BeefSupreme')]")


class DeleteLastBatch(Command):
    """
    Inherit from this if you want to create your own
    command styles. Note that Evennia's default commands
    use MuxCommand instead (next in this module)

    Note that the class's __doc__ string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    """
    # these need to be specified

    key = 'DeleteLastBatch'
    aliases = ["dbat"]
    locks = "cmd:perm(Wizards)"
    help_category = "development"

    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    # (we don't implement hook method access() here, you don't need to
    #  modify that unless you want to change how the lock system works
    #  (in that case see src.commands.command.Command))

    def at_pre_cmd(self):
        """
        This hook is called before self.parse() on all commands
        """
        pass

    def parse(self):
        """
        This method is called by the cmdhandler once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from self.func() (see below)

        The following variables are available to us:
           # class variables:

           self.key - the name of this command ('mycommand')
           self.aliases - the aliases of this cmd ('mycmd','myc')
           self.locks - lock string for this command ("cmd:all()")
           self.help_category - overall category of command ("General")

           # added at run-time by cmdhandler:

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following self.cmdstring.
           self.cmdset - the cmdset from which this command was picked. Not
                         often used (useful for commands like 'help' or to
                         list all available commands etc)
           self.obj - the object on which this command was defined. It is often
                         the same as self.caller.
        """
        pass

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.

        This will delete all of the last files created from running @batchcode, as
            long as you set up the attributes correctly in the batch file at the end.
        """

        self.caller.execute_cmd('@del ' + self.caller.db.fbat + '-' + self.caller.db.lbat)

        #self.caller.msg("Command called!")

    def at_post_cmd(self):
        """
        This hook is called after self.func().
        """
        pass

class RunBatchCode(DeleteLastBatch):
    '''
    Runs the batch code file specified below. Change which file it points
    to here whenever you are working a lot with a certain batch file.
    '''

    key = 'RunBatchCode'
    aliases = ['bc']
    locks = 'cmd:perm(Wizards)'
    help_category = 'development'

    def func(self):
        self.caller.execute_cmd('@batchcode test_batch')


class DisplayProperties(Command):
    '''
    Temporary tool to show objects_interacting_with, objects_nearby, and location_objects_nearby.

    Use the dbref as the argument.
    '''

    key = 'display properties'
    aliases = ['dp']
    locks = 'cmd:perm(Wizards)'
    help_category = 'development'

    def func(self):
        args = self.args.split()

        self.msg('objects interacting with: ' + str([obj.key + ' ' + obj.dbref for obj in search.search_object(args[0])[0].db.objects_interacting_with]))
        self.msg('objects nearby: ' + str([obj.key + ' ' + obj.dbref for obj in search.search_object(args[0])[0].db.objects_nearby]))
        self.msg('location objects nearby: ' + str([obj.key + ' ' + obj.dbref for obj in search.search_object(args[0])[0].db.location_objects_nearby]))

        
class ListObjectsByName(Command):
    '''
    lists objects that match the tag and/or name:
    syntax:
    list <tag> <name/alias>
    usage examples:
    # lists all objects with the tag 'character'
    list character
    # lists all characters named Frito
    list character frito
    # lists rooms
    list room
    # lists rooms called nexus
    list room nexus

    '''

    key = 'list objects'
    aliases = ['list']
    locks = 'cmd:perm(Wizards)'
    help_category = 'development'
    

    def func(self):
        args = self.args.split()
        tag = args[0]
        name = ' '.join(args[1:])
        caller = self.caller
        caller.msg(str([obj.key + ' : ' + obj.dbref for obj in search.search_object_tag(tag) if name in obj.key.lower() or name in obj.aliases.all()]))


class ListObjectsNearby(Command):
    '''
    Tool to list location_objects_nearby and objects_nearby.
    The caller must be in the same room as the objects queried.
    You can search by key or dbref.
    syntax:
    nearby <object>
    usage examples:
    nearby Frito
    nearby menhir
    '''

    key = 'list nearby'
    aliases = ['nearby']
    locks = 'cmd:perm(Wizards)'
    help_category = 'development'

    def func(self):
        target = self.args.split()[0]
        caller = self.caller
        for obj in [obj for obj in caller.location.contents if target == obj.key or target in obj.aliases.all() or target == obj.dbref]:
            caller.msg('location objects nearby: \n' + str([loc.key + ' : ' + loc.dbref for loc in obj.db.location_objects_nearby]))
        for obj in [obj for obj in caller.location.contents if target == obj.key or target in obj.aliases.all() or target == obj.dbref]:
            caller.msg('objects nearby: \n' + str([loc.key + ' : ' + loc.dbref for loc in obj.db.objects_nearby]))


class Create(Command):
    '''
    IN PROGRESS
    '''
    '''
    This is the tool used from inside the MUD to create any object desired. This command is menu
     based. When using the command you are prompted to specify various required or optional
     properties on an object. Details on valid input at each prompt should be included when
     updating this command. The prompts on this command should be based on the same properties
     specified for the 'at_creation' type methods of any object. Any new non-temporary
     properties of an object should be explicity specified in that object's main file, as well
     as added to this command. Some properties like the basic tag for an object will be done
     automatically, but there can be optional prompts to add additional tags, for example.
     
    This command takes no arguments.
    
    Usage:
        create
    '''

    key = 'create'
    aliases = ['cre']
    locks = 'cmd:perm(Wizards)'
    help_category = 'development'

    # path choice node
#    def makePathNode(self):
#        self.caller.msg('in makePathNode')
#        node = MenuNode('START',
#                         text = 'Object type:',
#                         links = ['END', 'END', 'END'],
#                         keywords = ['Object', 'NPC', 'Room'],
#                         callback = lambda self: Create.gotoChosenPath(Create(), self.caller, self.caller.db.menuvar))
#        return node

    # path choice node
    def makePathNode(self):
        self.caller.msg('in makePathNode')
        node = MenuNode(key = 'START',
                         text = 'Object type:',
                         links = ['END', 'END', 'END'],
                         keywords = ['Object', 'NPC', 'Room'],
                         callback = lambda self: Create.setChosenPath(Create(), self.caller))
        return node

    # setting initial path choice
    def setChosenPath(self, player):
        player.msg('in setChosenPath')
        player.db.next_node = 'setVariableNode'

    def makeSetVariableNode(self, next_node, choice):
        self.caller.msg('in makeSetVariableNode')
        self.caller.db.previous_choice = choice
        if next_node == 'setVariableNode':
            key = 'START'
        else:
            key = 'INACTIVE'
        node = MenuNode(key,
                         text = 'Reticulating Splines...',
                         links = ['END'],
                         linktexts = [' to Continue'],
                         keywords = ['1'],
                         callback = lambda self: Create.gotoChosenPath(Create(), self.caller, self.caller.db.previous_choice))
        return node

    # path choice
    def gotoChosenPath(self, player, choice):
        # choice references self.caller.db.menuvar in the main logic at the bottom
        self.caller.msg('in gotoChosenPath')
        if choice == 'Object':
            pass
        
        if choice == 'NPC':
            pass

        if choice == 'Room':
            player.db.next_node = 'roomNodeMain'

    def makeObjectNodeMain(self, next_node, choice):
        pass

    def makeNPCNodeMain(self, next_node, choice):
        pass

    def makeRoomNodeMain(self, next_node):
        if next_node == 'roomNodeMain':
            key = 'START'
        else:
            key = 'INACTIVE'

        text = 'Room type:'
        links = ['END','END']
        linktexts = [' ', ' ']
        keywords = ['Outdoor', 'Indoor']

        set_links = []
        set_linktexts = []
        set_keywords = []

        set_links.extend(links[0:3])
        set_linktexts.extend(linktexts[0:3])
        set_keywords.extend(keywords[0:3])
        
        node = MenuNode(key, 
                        text = text,
                        links = set_links,
                        linktexts = set_linktexts,
                        keywords = set_keywords,
                        callback = lambda self: Create.setChosenRoomType(Create(), self.caller)) 
        return node

    def setChosenRoomType(self, player):
        player.msg('in setChosenRoomType')
        player.db.next_node = 'setVariableNode2'

    def makeSetVariableNode2(self, next_node, choice):
        self.caller.msg('in makeSetVariableNode')
        self.caller.db.previous_choice = choice
        if next_node == 'setVariableNode2':
            key = 'START'
        else:
            key = 'INACTIVE'
        node = MenuNode('START',
                         text = 'Reticulating Splines...',
                         links = ['END'],
                         linktexts = [' to Continue'],
                         keywords = ['1'],
                         callback = lambda self: Create.gotoChosenRoomType(Create(), self.caller, self.caller.db.previous_choice))
        return node

    def gotoChosenRoomType(self, player, choice):
        if choice == 'Outdoor':
            player.db.next_node = 'roomNodeOutdoorMain'

        if choice == 'Indoor':
            player.db.next_node = 'roomNodeIndoorMain'

    def makeRoomNodeOutdoorMain(self, next_node):
        if next_node == 'roomNodeOutdoorMain':
            key = 'START'
        else:
            key = 'INACTIVE'

        text = 'Outdoor Room Type:'
        links = ['END', 'END', 'END', 'END']
        linktexts = ['For example, plains or flats.', 'For example, an old-growth forest.', 'For example, a thick forest.', 'For example, a canyon.']
        keywords = ['Open', 'Canopy', 'Thicket', 'Walled']

        set_links = []
        set_linktexts = []
        set_keywords = []

        set_links.extend(links[0:5])
        set_linktexts.extend(linktexts[0:5])
        set_keywords.extend(keywords[0:5])

        node = MenuNode(key, 
                        text = text,
                        links = set_links,
                        linktexts = set_linktexts,
                        keywords = set_keywords,
                        callback = lambda self: Create.setChosenOutdoorType(Create(), self.caller)) 
        return node

    def setChosenOutdoorType(self, player):
        player.msg('in setOutdoorRoomType')
        player.db.next_node = 'setVariableNode3'

    def makeSetVariableNode3(self, next_node, choice):
        self.caller.msg('in makeSetVariableNode')
        self.caller.db.previous_choice = choice
        if next_node == 'setVariableNode3':
            key = 'START'
        else:
            key = 'INACTIVE'
        node = MenuNode('START',
                         text = 'Reticulating Splines...',
                         links = ['END'],
                         linktexts = [' to Continue'],
                         keywords = ['1'],
                         callback = lambda self: Create.gotoChosenOutdoorType(Create(), self.caller, self.caller.db.previous_choice))
        return node

    def gotoChosenOutdoorType(self, player, choice):
        if choice == 'Open':
            player.db.next_node = 'roomNodeOutdoorOpen'
        if choice == 'Canopy':
            player.db.next_node = 'roomNodeOutdoorCanopy'
        if choice == 'Thicket':
            player.db.next_node = 'roomNodeOutdoorThicket'
        if choice == 'Walled':
            player.db.next_node = 'roomNodeOutdoorWalled'

    def makeRoomNodeOutdoorOpen(self, next_node):
        if next_node == 'roomNodeOutdoorOpen':
            key = 'START'
        else:
            key = 'INACTIVE'

        text = 'Select "Continue" to enter the room key:'
        links = ['END']
        linktexts = ['Enter the room key next.']
        keywords = ['Continue']

        set_links = []
        set_linktexts = []
        set_keywords = []

        set_links.extend(links[0:1])
        set_linktexts.extend(linktexts[0:1])
        set_keywords.extend(keywords[0:1])

        node = MenuNode(key,
                        text = text,
                        links = set_links,
                        linktexts = set_linktexts,
                        keywords = set_keywords,
                        callback = lambda self: Create.editOutdoorOpenRoomAlias(Create(), self.caller)) 
        return node

    def gotoEditOutdoorOpenRoomAlias(self, player, choice):
        player.db.next_node = 'roomNodeOutdoorAliasEntry'
        '''IN PROGRESS'''
        # DELETE THIS BELOW ONE LINE
        player.db.next_node = 'exitNode'
        player.db.outdoor_room_key = raw_input()

    
    def makeExitNode(self, next_node, choice):
        if next_node == 'exitNode':
            key = 'START'
        else:
            key = 'INACTIVE'
        
        node = MenuNode(key,
                        text = "All done!",
                        links = ['END'],
                        keywords = ['Exit'],
                        callback = lambda self: Create.exitNode(Create(), self.caller))

        return node

    def exitNode(self, player):
        player.db.next_node = 'DONE'

    def func(self):
        'Object Creation System'
        
        self.caller.msg('in func')

        if not self.args:
            self.caller.msg('in nonargs')
            startNode = self.makePathNode()
            setVar1 = self.makeSetVariableNode(self.caller.db.next_node, self.caller.db.menuvar)
            roomNodeMain = self.makeRoomNodeMain(self.caller.db.next_node)
            setVar2 = self.makeSetVariableNode2(self.caller.db.next_node, self.caller.db.menuvar)
            roomNodeOutdoorMain = self.makeRoomNodeOutdoorMain(self.caller.db.next_node)
            setVar3 = self.makeSetVariableNode3(self.caller.db.next_node, self.caller.db.menuvar)
            roomNodeOutdoorOpen = self.makeRoomNodeOutdoorOpen(self.caller.db.next_node)
            exitNode = self.makeExitNode(self.caller.db.next_node, self.caller.db.menuvar)

            if self.caller.db.next_node <> 'exitNode':
                self.caller.msg('in not exitNode')
                menu = MenuTree(self.caller, nodes = (startNode, setVar1, roomNodeMain, setVar2, roomNodeOutdoorMain, setVar3, roomNodeOutdoorOpen, exitNode), exec_end = "cre")
            else:
                self.caller.msg('in else')
                menu = MenuTree(self.caller, nodes = (startNode, setVar1, roomNodeMain, setVar2, roomNodeOutdoorMain, setVar3, roomNodeOutdoorOpen, exitNode))

            self.caller.msg('pre menu start')
            menu.start()
                                                      


