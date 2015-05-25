# This module contains commands useful for developers.

from game.gamesrc.commands.command import *
from src.utils import search

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
    nearby <Frito>
    nearby <menhir>
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





