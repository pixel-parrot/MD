"""
Example command set template module.

To create new commands to populate the cmdset, see
examples/command.py.

To extend the character command set:
  - copy this file up one level to gamesrc/commands and name it
    something fitting.
  - change settings.CMDSET_CHARACTER to point to the new module's
    CharacterCmdSet class
  - import/add commands at the end of CharacterCmdSet's add() method.

To extend Player cmdset:
  - like character set, but point settings.PLAYER on your new cmdset.

To extend Unloggedin cmdset:
  - like default set, but point settings.CMDSET_UNLOGGEDIN on your new cmdset.

To add a wholly new command set:
  - copy this file up one level to gamesrc/commands and name it
    something fitting.
  - add a new cmdset class
  - add it to objects e.g. with obj.cmdset.add(path.to.the.module.and.class)

"""

#from evennia import CmdSet, Command
#from evennia.commands.cmdset import CmdSet
from evennia import default_cmds
from evennia.commands.default import player
# adding menu driven system test
from evennia.contrib.menusystem import CmdMenuTest
from commands.character_creation import CharacterCreationSystem
# adding developer commands
from commands.developer_commands import *
# adding default commands
from commands.default import *
# adding new general commands
from commands.sublocation_movement import SublocationMovement


#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

# CUSTOM COMMAND SETS START AFTER EXAMPLES BELOW-------------------

class ExampleCmdSet(CmdSet):
    """
    Implements an empty, example cmdset.
    """

    key = "ExampleSet"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base Command object.
        It prints some info.
        """
        self.add(Command())


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    This is an example of how to overload the default command
    set defined in src/commands/default/cmdset_character.py.

    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_CHARACTER to point
    to this class.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_character
        super(CharacterCmdSet, self).at_cmdset_creation()

        #
        # any commands you add below will overload the default ones.
        #
        #self.add(menusystem.CmdMenuTest())
        #self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())
        self.add(general.CmdGet())
        self.add(general.CmdLook())
        self.add(general.CmdDrop())

        self.add(SublocationMovement())

        # delete or change this later!!!
        self.add(CharacterCreationSystem())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    This is an example of how to overload the command set of the
    unloggedin commands, defined in
    src/commands/default/cmdset_unloggedin.py.

    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_UNLOGGEDIN to
    point to this class.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_unloggedin
        super(UnloggedinCmdSet, self).at_cmdset_creation()

        #
        # any commands you add below will overload the default ones.
        #


class PlayerCmdSet(default_cmds.PlayerCmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "DefaultPlayer"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_ooc
        super(PlayerCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #

        # commands available to wizards
        self.add(DeleteLastBatch())
        self.add(RunBatchCode())
        self.add(DisplayProperties())
        self.add(ListObjectsByName())
        self.add(ListObjectsNearby())
        self.add(TempCmd())

        # commands generally available 
        self.add(CmdMenuTest())
        self.add(CharacterCreationSystem())

	

class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    Sets up the unlogged cmdset.
    Useful for making commands for character creation and things like that.
    """
    key = "DefaultSession"
    priority = -20

    def at_cmdset_creation(self):
        "Populate the cmdset"
        self.add(player.CmdSessions())

# CUSTOM COMMAND SETS START HERE--------------------------------------
#class DeveloperCommandSet(PlayerCmdSet):
#    """
#    Implements an empty, example cmdset.
#    """
#
#    key = "DeveloperCommandSet"
#    priority = 11
#
#    def at_cmdset_creation(self):
#        """
#        This is the only method defined in a cmdset, called during
#        its creation. It should populate the set with command instances.
#
#        As and example we just add the empty base Command object.
#        It prints some info.
#        """
#        self.add(DeleteLastBatch())
#
#
#class CharacterCmdSet(default_cmds.CharacterCmdSet):
#    """
#    This is an example of how to overload the default command
#    set defined in src/commands/default/cmdset_character.py.
#
#    Here we copy everything by calling the parent, but you can
#    copy&paste any combination of the default command to customize
#    your default set. Next you change settings.CMDSET_CHARACTER to point
#    to this class.
#    """
#    key = "DefaultCharacter"
#
#    def at_cmdset_creation(self):
#        """
#        Populates the cmdset
#        """
#        # calling setup in src.commands.default.cmdset_character
#        super(CharacterCmdSet, self).at_cmdset_creation()
#
#        #
#        # any commands you add below will overload the default ones.
#        #
#        #self.add(menusystem.CmdMenuTest())
#        #self.add(lineeditor.CmdEditor())
#        #self.add(misc_commands.CmdQuell())
#
#
#class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
#    """
#    This is an example of how to overload the command set of the
#    unloggedin commands, defined in
#    src/commands/default/cmdset_unloggedin.py.
#
#    Here we copy everything by calling the parent, but you can
#    copy&paste any combination of the default command to customize
#    your default set. Next you change settings.CMDSET_UNLOGGEDIN to
#    point to this class.
#    """
#    key = "DefaultUnloggedin"
#
#    def at_cmdset_creation(self):
#        """
#        Populates the cmdset
#        """
#        # calling setup in src.commands.default.cmdset_unloggedin
#        super(UnloggedinCmdSet, self).at_cmdset_creation()
#
#        #
#        # any commands you add below will overload the default ones.
#        #
#
#
#class PlayerCmdSet(default_cmds.PlayerCmdSet):
#    """
#    This is set is available to the player when they have no
#    character connected to them (i.e. they are out-of-character, ooc).
#    """
#    key = "DefaultPlayer"
#
#    def at_cmdset_creation(self):
#        """
#        Populates the cmdset
#        """
#        # calling setup in src.commands.default.cmdset_ooc
#        super(PlayerCmdSet, self).at_cmdset_creation()
#        #
#        # any commands you add below will overload the default ones.
#        #
