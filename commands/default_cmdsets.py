"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
# added stuff below

from evennia.commands.default import player
# adding basic commands
from commands.default.general import *
# adding menu driven system test
from evennia.contrib.menusystem import CmdMenuTest
from commands.character_creation import CharacterCreationSystem
# adding developer commands
from commands.developer_commands import *
# adding default commands
from commands.default.cmdset_character import *
from commands.default.cmdset_player import *
from commands.default.cmdset_session import *
from commands.default.cmdset_unloggedin import *
# adding new general commands
from commands.sublocation_movement import SublocationMovement


#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
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


class PlayerCmdSet(default_cmds.PlayerCmdSet):
    """
    This is the cmdset available to the Player at all times. It is
    combined with the `CharacterCmdSet` when the Player puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultPlayer"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
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
        self.add(Create())

        # commands generally available 
        self.add(CmdMenuTest())
        self.add(CharacterCreationSystem())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
