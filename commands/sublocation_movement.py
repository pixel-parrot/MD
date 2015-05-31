from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia import utils
from evennia.commands.default.building import CmdDestroy as CD
from md.tools.list_tools import ListTools as LT
from md.tools.text_tools import TextTools as TT
from md.tools.parsing_tools import ParsingTools as PT
from md.tools.proximity_tools import ProximityTools as PxT


class SublocationMovement(BaseCommand):
    """
    Note that the class's __doc__ string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.
    """

    key = "approach"
    aliases = ["stand by", "stand beside", "stand near", "stand next to", "stand against", "go to", "go toward", "go towards", "go near", "go next to", "go by", "go beside", "walk to", "walk next to", "walk near", "walk toward", "walk beside", "move by", "move to", "move near", "move next to", "move toward", "move towards"]
    locks = "cmd:all()"
    help_category = "movement"

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
        Allows neutral movement to a room sub-location. Sub-locations are defined by
            objects in the room that are StationaryObjects, Exits? (not yet implemented),
            Characters, Mobile Non-Character Objects? (not yet implemented), and so on.
        Using this will update the caller's location_objects_nearby property and
            objects_nearby property, as appropriate.
        """

        caller = self.caller

        #self.caller.msg("cmdstring: " + self.cmdstring)
        #self.caller.msg("args: " + self.args)

        # getting the prepositions used, object strings and adjective strings
        successful, num1, adj1, obj1, prep1, adj2, obj2, prep2, adj3, obj3 = PT.parser(PT(), caller, self.cmdstring, self.args)
        # if parsing was not successful, don't continue
        if not successful:
            #caller.msg('successful: ' + str(successful))
            #caller.msg('num1: ' + str(num1))
            #caller.msg('adj1: ' + str(adj1))
            #caller.msg('obj1: ' + str(obj1))
            #caller.msg('prep1: ' + str(prep1))
            #caller.msg('adj2: ' + str(adj2))
            #caller.msg('obj2: ' + str(obj2))
            #caller.msg('prep2: ' + str(prep2))
            #caller.msg('adj3: ' + str(adj3))
            #caller.msg('obj3: ' + str(obj3))
            return

        # getting a list of potential object matches for the obj1, obj2, and obj3 strings
        object1_list = [obj for obj in caller.location.contents if obj1 == obj.key or obj1 in obj.aliases.all()]
        object2_list = [obj for obj in caller.location.contents if obj2 == obj.key or obj2 in obj.aliases.all()]
        object3_list = [obj for obj in caller.location.contents if obj3 == obj.key or obj3 in obj.aliases.all()]

        # getting potential targets based on proximity
        successful, target_potential, obj2_potential, obj3_potential = PxT.returnAdjacentTargets(PxT(), caller, self.cmdstring, adj1, obj1, object1_list, adj2, obj2, object2_list, adj3, obj3, object3_list)
        # if there was a proximity error, don't continue
        if not successful:
            return
        
        # remove any references to the mover from any location_objects_nearby and objects_nearby
        for obj in caller.db.location_objects_nearby:
            if obj.db.location_objects_nearby:
                if caller in obj.db.location_objects_nearby:
                    obj.db.location_objects_nearby.remove(caller)
                if caller in obj.db.objects_nearby:
                    obj.db.objects_nearby.remove(caller)
        for obj in caller.db.objects_nearby:
            if obj.db.objects_nearby:
                if caller in obj.db.objects_nearby:
                    obj.db.objects_nearby.remove(caller)
                if caller in obj.db.location_objects_nearby:
                    obj.db.location_objects_nearby.remove(caller)

        # make the move
        if len(target_potential) == 1:
            target = target_potential[0]
            #caller.msg('final target: ' + str(target.dbref) + ': ' + str(target.key))
            target2 = False
            target3 = False
            if obj2_potential:
                target2 = obj2_potential[0]
                #caller.msg('final target 2: ' + str(target2.dbref) + ': ' + str(target2.key))
            if obj3_potential:
                target3 = obj3_potential[0]
                #caller.msg('final target 3: ' + str(target3.dbref) + ': ' + str(target3.key))
        ##### update the mover's locations
        if target.db.location_objects_nearby:
            caller.db.location_objects_nearby = [target.db.location_objects_nearby[0]]
        if 'character' in target.tags.all():
            caller.db.location_objects_nearby.append(target)
        caller.db.objects_nearby = [target.location]
        caller.db.objects_nearby.append(target)
        ##### update the target's objects_nearby and location_objects_nearby as needed
        if 'character' in caller.tags.all():
            target.db.location_objects_nearby.append(caller)
        target.db.objects_nearby.append(caller)
        target.db.location_objects_nearby = LT.dedupeList(LT(), target.db.location_objects_nearby)
        target.db.objects_nearby = LT.dedupeList(LT(), target.db.objects_nearby)
        ######## also update the closest location_object that the target is near to now
        ########    also have the mover
        if 'character' in caller.tags.all():
            target.db.location_objects_nearby[0].db.location_objects_nearby.append(caller)
        target.db.location_objects_nearby[0].db.objects_nearby.append(caller)
        target.db.location_objects_nearby[0].db.location_objects_nearby = LT.dedupeList(LT(), target.db.location_objects_nearby[0].db.location_objects_nearby)
        target.db.location_objects_nearby[0].db.objects_nearby = LT.dedupeList(LT(), target.db.location_objects_nearby[0].db.objects_nearby)
        ##### update the target2's objects_nearby and location_objects_nearby as needed
        if target2:
            if 'character' in caller.tags.all():
                target2.db.location_objects_nearby.append(caller)
                target2.db.location_objects_nearby = LT.dedupeList(LT(), target2.db.location_objects_nearby)
            target2.db.objects_nearby.append(caller)
            target2.db.objects_nearby = LT.dedupeList(LT(), target2.db.objects_nearby)
        ##### update the target3's objects_nearby and location_objects_nearby as needed
        if target3:
            if 'character' in caller.tags.all():
                target3.db.location_objects_nearby.append(caller)
                target3.db.location_objects_nearby = LT.dedupeList(LT(), target3.db.location_objects_nearby)
            target3.db.objects_nearby.append(caller)
            target3.db.objects_nearby = LT.dedupeList(LT(), target3.db.objects_nearby)

        # announce the move
        ##### announce the move to the player
        ######### if the target is a PC or NPC with a name
        ######### placeholder system for handling which name to show the caller
        if 'character' in target.tags.all() and caller.db.characters_met[target]:
            caller.msg('You %s %s.' %(self.cmdstring, caller.db.characters_met[target]))
        ######### if the target is a thing, animal, or unnamed PC or NPC
        else:
            caller.msg('You %s the %s.' %(self.cmdstring, target.db.object_title))
        ##### announce the move to the target
        ######### get the correct form of the commandstring's verb
        verb = self.cmdstring.split()[0]
        verb = TT.pluralKey(TT(), verb)
        cmdstring_tail = ' '.join(self.cmdstring.split()[1:]).strip()
        if cmdstring_tail: 
            cmdstring_tail = ' ' + cmdstring_tail
        if 'character' in target.tags.all():
            if 'character' in caller.tags.all() and target.db.characters_met[caller]:
                target.msg('%s %s you.' %(target.db.characters_met[caller], verb + cmdstring_tail))
            else:
                target.msg('The %s %s you.' %(caller.db.object_title, verb + cmdstring_tail))
        ##### announce the move to players in the room
        ######### gather all players in the room so we can send them the correct namestring
        #########   for a target and caller if they know their name
        characters_in_room = [obj for obj in caller.location.contents if 'character' in obj.tags.all() and (obj <> caller and obj <> target and obj <> target2 and obj <> target3)]
        for char in characters_in_room:
            caller_string = 'The ' + caller.db.object_title
            if 'character' in caller.tags.all() and char.db.characters_met[caller]:
                caller_string = char.db.characters_met[caller]
            target_string = 'the ' + target.db.object_title
            if 'character' in target.tags.all() and char.db.characters_met[target]:
                target_string = char.db.characters_met[target]
            if target2:
                target2_string = 'the ' + target2.db.object_title
                if 'character' in target2.tags.all() and char.db.characters_met[target2]:
                    target2_string = char.db.characters_met[target2]
            if target3:
                target3_string = 'the ' + target3.db.object_title
                if 'character' in target3.tags.all() and char.db.characters_met[target3]:
                    target3_string = char.db.characters_met[target3]
            if target3:
                char.msg('%s %s %s and %s near %s.' %(caller_string, verb + cmdstring_tail, target_string, target2_string, target3_string))
            if not target3 and target2:
                char.msg('%s %s %s near %s.' %(caller_string, verb + cmdstring_tail, target_string, target2_string))
            if not target2 and not target3:
                char.msg('%s %s %s.' %(caller_string, verb + cmdstring_tail, target_string))


    def at_post_cmd(self):
        """
        This hook is called after self.func().
        """
        pass


