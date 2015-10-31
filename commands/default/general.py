"""
General Character commands usually availabe to all characters
"""
from django.conf import settings
from evennia.utils import utils, prettytable
#from src.commands.default.muxcommand import MuxCommand
from commands.default.muxcommand import MuxCommand
from tools.format_line import FormatLine as FL
from tools.text_tools import TextTools as TT
from tools.list_tools import ListTools as LT
from tools.parsing_tools import ParsingTools as PT
from tools.proximity_tools import ProximityTools as PxT
from evennia.utils import search
from evennia import search_object
import random as r


# limit symbol import for API
__all__ = ("CmdHome", "CmdLook", "CmdNick",
           "CmdInventory", "CmdGet", "CmdDrop", "CmdGive",
           "CmdSay", "CmdPose", "CmdAccess")

AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))


class CmdHome(MuxCommand):
    """
    move to your character's home location

    Usage:
      home

    Teleports you to your home location.
    """

    key = "home"
    locks = "cmd:perm(home) or perm(Builders)"

    def func(self):
        "Implement the command"
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("You have no home!")
        elif home == caller.location:
            caller.msg("You are already home!")
        else:
            caller.move_to(home)
            caller.msg("There's no place like home ...")

class CmdLook(MuxCommand):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls", "look at"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        args = self.args
        # added by MistDude to help with particle 'at' functionality
        args_list = str(args.split())

        # handling the use of 'at' particle
        if args_list.split()[0] == 'at':
            args = ''.join(args_list.remove('at'))
        # added by MistDude: if no argument when using particle 'at'
        #    show error message
        if self.cmdstring == 'look at' and not args:
            caller.msg("\nLook at what?")
            return
        if args:
            # Use search to handle duplicate/nonexistant results.
            looking_at_obj = caller.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("You have no location to look at!")
                return

        if not hasattr(looking_at_obj, 'return_appearance'):
            # this is likely due to us having a player instead
            looking_at_obj = looking_at_obj.character
        if not looking_at_obj.access(caller, "view"):
            caller.msg("Could not find '%s'." % args)
            return

        # the object's at_desc() method.
        looking_at_obj.at_desc(looker=caller)

        # Added by MistDude to use the format_line module functionalities. Might be
        #  changed, edited, w/e in the future.
        if (looking_at_obj in search.search_object_tag('room')) or (looking_at_obj in search.search_object_tag('exit')): 
            caller.msg(FL.breakLine(FL(),looking_at_obj.return_appearance(caller),'title'))
        if (looking_at_obj in search.search_object_tag('character') or looking_at_obj in search.search_object_tag('thing')): 
            caller.msg(FL.centerText(FL(),looking_at_obj.return_appearance(caller),'block'))

        # the object's at_desc() method.
        #looking_at_obj.at_desc(looker=caller)


class CmdNick(MuxCommand):
    """
    define a personal alias/nick

    Usage:
      nick[/switches] <nickname> = [<string>]
      alias             ''

    Switches:
      object   - alias an object
      player   - alias a player
      clearall - clear all your aliases
      list     - show all defined aliases (also "nicks" works)

    Examples:
      nick hi = say Hello, I'm Sarah!
      nick/object tom = the tall man

    A 'nick' is a personal shortcut you create for your own use. When
    you enter the nick, the alternative string will be sent instead.
    The switches control in which situations the substitution will
    happen. The default is that it will happen when you enter a
    command. The 'object' and 'player' nick-types kick in only when
    you use commands that requires an object or player as a target -
    you can then use the nick to refer to them.

    Note that no objects are actually renamed or changed by this
    command - the nick is only available to you. If you want to
    permanently add keywords to an object for everyone to use, you
    need build privileges and to use the @alias command.
    """
    key = "nick"
    aliases = ["nickname", "nicks", "@nick", "alias"]
    locks = "cmd:all()"

    def func(self):
        "Create the nickname"

        caller = self.caller
        switches = self.switches
        nicks = caller.nicks.get(return_obj=True)

        if 'list' in switches:
            table = prettytable.PrettyTable(["{wNickType",
                                             "{wNickname",
                                             "{wTranslates-to"])
            for nick in utils.make_iter(nicks):
                table.add_row([nick.db_category, nick.db_key, nick.db_strvalue])
            string = "{wDefined Nicks:{n\n%s" % table
            caller.msg(string)
            return
        if 'clearall' in switches:
            caller.nicks.clear()
            caller.msg("Cleared all aliases.")
            return
        if not self.args or not self.lhs:
            caller.msg("Usage: nick[/switches] nickname = [realname]")
            return
        nick = self.lhs
        real = self.rhs

        if real == nick:
            caller.msg("No point in setting nick same as the string to replace...")
            return

        # check so we have a suitable nick type
        if not any(True for switch in switches if switch in ("object", "player", "inputline")):
            switches = ["inputline"]
        string = ""
        for switch in switches:
            oldnick = caller.nicks.get(key=nick, category=switch)
            #oldnick = Nick.objects.filter(db_obj=caller.dbobj, db_nick__iexact=nick, db_type__iexact=switch)
            if not real:
                # removal of nick
                if oldnick:
                    # clear the alias
                    string += "\nNick '%s' (= '%s') was cleared." % (nick, oldnick)
                    caller.nicks.delete(nick, category=switch)
                else:
                    string += "\nNo nick '%s' found, so it could not be removed." % nick
            else:
                # creating new nick
                if oldnick:
                    string += "\nNick %s changed from '%s' to '%s'." % (nick, oldnick, real)
                else:
                    string += "\nNick set: '%s' = '%s'." % (nick, real)
                caller.nicks.add(nick, real, category=switch)
        caller.msg(string)


class CmdInventory(MuxCommand):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"

    def func(self):
        "check inventory"
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = prettytable.PrettyTable(["name", "desc"])
            table.header = False
            table.border = False
            for item in items:
                table.add_row(["{C%s{n" % item.name, item.db.desc and item.db.desc or ""])
            string = "{wYou are carrying:\n%s" % table
        self.caller.msg(string)


class CmdGet(MuxCommand):
    """
    pick up something from a room location
    a different command will be used to handle items inside
    of containers and more complex syntax

    Usage:
      get <obj> 

    Picks up an object from your location and puts it in
    your inventory.
    """
    key = "get"
    aliases = "grab"
    locks = "cmd:all()"

    #def func(self, *thing):
    def func(self):
        "implements the command."

        caller = self.caller

        obj = None

        # a list of the input words, not including the initial command string
        whole_string_list = self.args.split(' ')

        # getting a list of prepositions        
        prepositions = TT.prepositionList(TT())

        # checking if a preposition is used in the command
        preposition_used = [preposition for preposition in prepositions if preposition in whole_string_list] 
        # checking for invalid input where command ends in preposition
        if whole_string_list[len(whole_string_list)-1] in prepositions:
            caller.msg("You momentarily forget just what it was you were about to do.")
            return

        # getting objects in room key strings
        object_keys = [tmpobj.key for tmpobj in caller.location.contents]
        object_keys_string = ' '.join(object_keys)

        # getting objects in room alias strings
        object_aliases = [tmpobj.aliases.all() for tmpobj in caller.location.contents]
        object_aliases_list = []
        for element in object_aliases:
            for sub_element in element:
                for sub_sub_element in sub_element.split(' '):
                    object_aliases_list.append(sub_sub_element)

        # getting container contents in room keys strings
        location_objects = caller.search(caller.location).contents
        containers = [tmpobj for tmpobj in location_objects if '_stack' in tmpobj.key]
        containers_contents_keys = []
        containers_contents_keys_string = ''
        if containers:
            for container in containers:
                for tmpobj in container.contents:
                    containers_contents_keys.append(tmpobj.key)
            containers_contents_keys_string = ' '.join(containers_contents_keys)
            
        # if needed, below should also get container contents in room alias strings

        ''' IN PROGRESS : changing to using the parsing_tools parser '''
        # now we parse the command string to get the object, prepositions, and location
        #    strings:
        successful, num, adj1, obj1, prep1, adj2, obj2, prep2, adj3, obj3, prep3, adj4, obj4 = PT.parser(PT(), caller, self.cmdstring, self.args)
        if not successful:
            caller.msg('successful: ' + str(successful))
            caller.msg('num: ' + str(num))
            caller.msg('adj1: ' + str(adj1))
            caller.msg('obj1: ' + str(obj1))
            caller.msg('prep1: ' + str(prep1))
            caller.msg('adj2: ' + str(adj2))
            caller.msg('obj2: ' + str(obj2))
            caller.msg('prep2: ' + str(prep2))
            caller.msg('adj3: ' + str(adj3))
            caller.msg('obj3: ' + str(obj3))
            caller.msg('prep3: ' + str(prep3))
            caller.msg('adj4: ' + str(adj4))
            caller.msg('obj4: ' + str(obj4))
            return
        caller.msg('PARSING SUCCESS!!!')
        caller.msg('successful: ' + str(successful))
        caller.msg('num: ' + str(num))
        caller.msg('adj1: ' + str(adj1))
        caller.msg('obj1: ' + str(obj1))
        caller.msg('prep1: ' + str(prep1))
        caller.msg('adj2: ' + str(adj2))
        caller.msg('obj2: ' + str(obj2))
        caller.msg('prep2: ' + str(prep2))
        caller.msg('adj3: ' + str(adj3))
        caller.msg('obj3: ' + str(obj3))
        caller.msg('prep3: ' + str(prep3))
        caller.msg('adj4: ' + str(adj4))
        caller.msg('obj4: ' + str(obj4))

        # this code section is where we get the actual objects that fit the location object
        #   strings in the room. we also will catch bad attempts for the cases of bad prepositions
        #   and location/object combinations that do not match
        #### getting location 1 objects
        loc_objs_list_1 = []
        loc_objs_list_1 = [tmpobj for tmpobj in caller.location.contents if obj2 == tmpobj.key or obj2 in tmpobj.aliases.all()]
        caller.msg('loc_objs_list_1: ' + str([tmpobj.dbref + ' : ' + tmpobj.key for tmpobj in loc_objs_list_1]))
        #### getting location 2 objects
        loc_objs_list_2 = []
        loc_objs_list_2 = [tmpobj for tmpobj in caller.location.contents if obj3 == tmpobj.key or obj3 in tmpobj.aliases.all()]
        caller.msg('loc_objs_list_2: ' + str([tmpobj.dbref + ' : ' + tmpobj.key for tmpobj in loc_objs_list_2]))
        #### getting location 3 objects
        loc_objs_list_3 = []
        loc_objs_list_3 = [tmpobj for tmpobj in caller.location.contents if obj4 == tmpobj.key or obj4 in tmpobj.aliases.all()]
        caller.msg('loc_objs_list_3: ' + str([tmpobj.dbref + ' : ' + tmpobj.key for tmpobj in loc_objs_list_3]))
        #### getting target objects
        target_list = []
        ######## if not in a stack
        target_list = [tmpobj for tmpobj in caller.location.contents if obj1 == tmpobj.key or obj1 in tmpobj.aliases.all()]
        caller.msg('target_list: ' + str([tmpobj.dbref + ' : ' + tmpobj.key for tmpobj in target_list]))
        ######## if in a stack
        if not target_list:
            caller.msg('container_contents_keys_string: ' + containers_contents_keys_string)
            target_list = [r.choice(tmpobj.contents) for tmpobj in caller.location.contents if obj1 in containers_contents_keys_string and tmpobj.key.replace('_stack', '') in containers_contents_keys_string]
            caller.msg('target_list: ' + str([tmpobj.dbref + ' : ' + tmpobj.key for tmpobj in target_list]))
        #### validating by proximity and adjective
        successful, target_potential, obj2_potential, obj3_potential, obj4_potential = PxT.returnAdjacentTargets(PxT(), caller, self.cmdstring, adj1, obj1, target_list, adj2, obj2, loc_objs_list_1, adj3, obj3, loc_objs_list_2, adj4, obj4, loc_objs_list_3)
        caller.msg('adjacency success: ' + str(successful))
        if target_potential:
            caller.msg('target potential: ' + target_potential[0].dbref + ' : ' + target_potential[0].key)
        if obj2_potential:
            caller.msg('obj2_potential: ' + obj2_potential[0].dbref + ' : ' + obj2_potential[0].key)
        if obj3_potential:
            caller.msg('obj3_potential: ' + obj3_potential[0].dbref + ' : ' +  obj3_potential[0].key)
        if obj4_potential:
            caller.msg('obj4_potential: ' + obj4_potential[0].dbref + ' : ' +  obj4_potential[0].key)
        #### if there was a proximity error, don't continue
        if not successful:
            '''when testing, comment out the return'''
            return
        '''
        IN PROGRESS:
            ATTEMPTING TO FIGURE OUT HOW TO ALLOW GETTING SOMETHING FROM A CONTAINER AS THE FIRST LOCATION OBJ
            ALSO POSSIBLY VALIDATING BY THE TYPE OF COMMAND USED, LIKE 'GET...FROM' VERSUS 'GET...NEAR'
            ALSO FIX THE VALIDATION MESSAGES BELOW TO ACCOUNT FOR CHARACTER NAMES KNOWN see proximity_tools.py for ex
        '''
        #### validating prepositions on command
        #### validating prepositions on objects
        if obj2_potential:
            # validating prepositions used against supported prepositions on the location_objects
            if prep1 not in obj2_potential[0].db.valid_prepositions:
                caller.msg("You cannot get anything --" + prep1 + "-- the " + obj2_potential[0].key + ".")
                return
        if obj3_potential:
            # validating prepositions used against supported prepositions on the location_objects
            if prep2 not in obj3_potential[0].db.valid_prepositions:
                caller.msg("You cannot get anything --" + prep2 + "-- the " + obj3_potential[0].key + ".")
                return
        if obj4_potential:
            # validating prepositions used against supported prepositions on the location_objects
            if prep3 not in obj4_potential[0].db.valid_prepositions:
                caller.msg("You cannot get anything --" + prep3 + "-- the " + obj4_potential[0].key + ".")
                return
            
        ''' This is here for testing purposes '''
        #return
                
        ''' IN PROGRESS : changing to using the parsing_tools parser, current progress '''

        '''
        IN PROGRESS
        # this code section is for if no locations are specified, so the object or stack must be in the
        #   immediate vicinity of the character. If there is none within the character's objects_nearby
        #   property, but there are ones in the room, they have to specify which one. Eventually this will
        #   auto-move them to that location (not an actual move, but an emote will happen and their objects_nearby
        #   property will be updated) but they will have to try to get the item again. The idea being that first you
        #   approach the object, then you get it. This way if someone already has a pile of rocks by them, and it's
        #   the only source of rocks in the room, you can't just accidentally or purposely swipe their rock in one
        #   go... you first have to approach the spot (getting an indication to the the players that 'you approach
        #   the rock pile where Frito is standing'), then you can get the rocks.
        '''
        caller.msg('get command current progress start')
        caller.msg('target_potential: ' + str(target_potential))
        if not obj2_potential and not obj3_potential and not obj4_potential:
            obj_list = []
            inside_stack_flag = []
            caller.msg('inside stack flag 1: ' + str(inside_stack_flag))
            #### detect if we are trying to get an item that is in a stack in the room
            inside_stack_flag = [thing for thing in caller.location.contents if target_potential[0].key + '_stack' == thing.key]
            #### detect if we are trying to get an item that is in a stack near the getter
            inside_nearby_stack_flag = [thing for thing in caller.location.contents if target_potential[0].key + '_stack' == thing.key and thing in caller.db.objects_nearby and caller in thing.db.objects_nearby]
            #### detect if we are trying to get an item that is in a stack near another person, or people
            inside_someones_stack_flag = [thing for thing in caller.location.contents if target_potential[0].key + '_stack' == thing.key and [person for person in caller.location.contents if 'character' in person.tags.all() and person <> caller and thing in person.db.objects_nearby and person in thing.db.objects_nearby]] 
            caller.msg('inside stack flag 2: ' + str(inside_stack_flag))
            '''IN PROGRESS: now what to do here is check all these flags against each other to decide what to do next, then eventually
                the target_potential that is correct will be the item that the character picks up, most of this stuff below in the next
                couple of blocks needs to be totally updated still'''

            if inside_stack_flag:
                caller.msg('in inside_stack_flag')
                if len(inside_stack_flag) > 1: caller.msg('CHECK INSIDE_STACK_FLAG: ' + str([tmpobj.key for tmpobj in inside_stack_flag]))
                # this will allow you to get a stackable item from a stack
                #   in the room without directly interacting with the stack
                stack_nearby = [tmpobj for tmpobj in caller.db.objects_nearby if target_potential[0].key + '_stack' in tmpobj.tags.all()]
                if stack_nearby:
                    caller.msg('in if stack_nearby')
                    if len(stack_nearby) > 1: caller.msg('CHECK STACK_NEARBY: ' + str([tmpobj.key for tmpobj in stack_nearby]))
                    stack_nearby[0].db.objects_interacting_with.append(caller)
                    caller.msg('stack_nearby: ' + str(stack_nearby))
                    obj_list = stack_nearby[0].contents
                    obj = r.choice(obj_list)

            '''IN PROGRESS : making simple 'get' command work for stacks and non stacks'''
            if not inside_stack_flag:
                caller.msg('in not inside_stack_flag')
                # use this to check if we're using a valid object string and that there is a valid object nearby
                #object_exists = caller.search(target_potential[0].key,location=caller.location,exact=True,quiet=True)
                object_exists = [tmpobj for tmpobj in caller.db.objects_nearby if (target_potential[0].key == tmpobj.key or target_potential[0].key in tmpobj.aliases.all()) and tmpobj not in caller.contents]
                print 'object_exists: ' + str([tmpobj.key for tmpobj in object_exists])
                if object_exists:
                    #obj_in_location_tags = caller.search(target_potential[0].key,location=caller.location,exact=True,quiet=True)[0].tags.all()
                    #obj_in_location_key = caller.search(target_potential[0].key,location=caller.location,exact=True,quiet=True)[0].key
                    #obj_in_location_aliases = caller.search(target_potential[0].key,location=caller.location,exact=True,quiet=True)[0].aliases.all()
                    # mark if we are tyring to pick up a stack or not, True if
                    #  we are trying to interact with a stack, False if not
                    #stack_flag = 'container' in obj_in_location_tags and (target_potential[0].key in obj_in_location_key or target_potential[0].key in obj_in_location_aliases)
                    print 'object_exists: ' + str([tmpobj.key for tmpobj in object_exists])
                    stack_flag = [tmpobj for tmpobj in object_exists if 'container' in tmpobj.tags.all()]
                    print 'stack_flag: ' + str([tmpobj.key for tmpobj in stack_flag])
                    if stack_flag:
                        # this will allow you specify the stack-object you want to get
                        #   by also using the stack_size description to get it. 
                        stack_size_string = ' '.join(whole_string_list)
                        # now find the specific object desired
                        if stack_size_string:
                            #obj_list = [obj for obj in caller.location.contents if target_potential[0].key in obj.aliases.all() and obj.db.stack_size == stack_size_string]
                            obj_list = [tmpobj for tmpobj in stack_flag if tmpobj.db.stack_size == stack_size_string]
                            if obj_list:
                                obj = r.choice(obj_list)
                        else:
                            #obj_list = [obj for obj in caller.location.contents if target_potential[0].key in obj.aliases.all()]
                            obj_list = [tmpobj for tmpobj in stack_flag]
                            if obj_list:
                                obj = r.choice(obj_list)
                    # since it's not inside a stack, and not a stack itself, it is just a 'normal'
                    #    object
                    else:
                        #obj_list = [obj for obj in caller.location.contents if target_potential[0].key in obj.aliases.all() or target_potential[0].key == obj.key]
                        ''' change above code to use target_potential where needed '''
                        obj = target_potential[0]
        
        # catching bad attempts
        #self.msg('obj list: ' + ' '.join([obj.key for obj in obj_list]))
        if not target_potential:
            caller.msg("Get what?")
            return
        if not obj:
            caller.msg("There aren't any within reach.")
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if caller == obj.location:
            caller.msg("You already hold that.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return
            
        # adding support for stacks by changing which string displays
        #  as picked up depending on object type
        obj_string = obj.key
        if obj in search.search_object_tag('container'):
            obj_string = obj.db.stack_size + ' ' + obj.db.container_key    
        else:
            obj_string = 'a ' + obj.key

        # updating the object-being-moved's objects_interacting_with property
        obj.db.objects_interacting_with.insert(0,caller)
        obj.db.objects_interacting_with = LT.dedupeList(LT(), obj.db.objects_interacting_with)

        # making the move
        caller.msg('obj at move: ' + str(obj.key) + " " + str(obj.dbref))
        obj.move_to(caller, quiet=True)

        # displaying the resulting messages
        caller.msg("You pick up %s." % obj_string)
        caller.location.msg_contents("%s picks up %s." %
                                        (caller.name,
                                         obj_string),
                                         exclude=caller)

        '''NEED TO IMPLEMENT if the caller is attempting to get something that
            they aren't near to, automatically make them 'move' near to that
            object by updating their sub locations and auto emotting'''
        # updating the caller's objects_nearby and location_objects_nearby as
        #   needed:


        # calling hook method
        obj.at_get(caller)


class CmdDrop(MuxCommand):
    """
    drop something

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"

    def func(self):
        "Implement command"

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
        results = caller.search(self.args, location=caller, quiet=True)

        # now we send it into the error handler (this will output consistent
        # error messages if there are problems).
        obj = AT_SEARCH_RESULT(caller, self.args, results, False,
                              nofound_string="You aren't carrying %s." % self.args,
                              multimatch_string="You carry more than one %s:" % self.args)
        if not obj:
            return

        # adding support for stacks by changing which string displays
        #  as dropped depending on object type
        obj_string = obj.key
        if obj in search.search_object_tag('container'):
            obj_string = obj.db.stack_size + ' ' + obj.db.container_key    

        # updating the object-being-moved's objects_interacting_with property
        obj.db.objects_interacting_with.insert(0,caller)
        obj.db.objects_interacting_with = LT.dedupeList(LT(), obj.db.objects_interacting_with)

        # making the move
        obj.move_to(caller.location, quiet=True)
        caller.msg("You drop %s." % (obj_string,))
        caller.location.msg_contents("%s drops %s." %
                                         (caller.name, obj_string),
                                         exclude=caller)

        # Call the object script's at_drop() method.
        obj.at_drop(caller)


class CmdGive(MuxCommand):
    """
    give away something to someone

    Usage:
      give <inventory obj> = <target>

    Gives an items from your inventory to another character,
    placing it in their inventory.
    """
    key = "give"
    locks = "cmd:all()"

    def func(self):
        "Implement give"

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Usage: give <inventory object> = <target>")
            return
        to_give = caller.search(self.lhs)
        target = caller.search(self.rhs)
        if not (to_give and target):
            return
        if target == caller:
            caller.msg("You keep %s to yourself." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("You are not holding %s." % to_give.key)
            return
        # give object
        caller.msg("You give %s to %s." % (to_give.key, target.key))
        to_give.move_to(target, quiet=True)
        target.msg("%s gives you %s." % (caller.key, to_give.key))


class CmdSay(MuxCommand):
    """
    speak as your character

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        "Run the say command"

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # calling the speech hook on the location
        speech = caller.location.at_say(caller, speech)

        # Feedback for the object doing the talking.
        caller.msg('You say, "%s{n"' % speech)

        # Build the string to emit to neighbors.
        emit_string = '%s says, "%s{n"' % (caller.name,
                                               speech)
        caller.location.msg_contents(emit_string,
                                     exclude=caller)


class CmdPose(MuxCommand):
    """
    strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """
    key = "pose"
    aliases = [":", "emote"]
    locks = "cmd:all()"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        "Hook function"
        if not self.args:
            msg = "What do you want to do?"
            self.caller.msg(msg)
        else:
            msg = "%s%s" % (self.caller.name, self.args)
            self.caller.location.msg_contents(msg)


class CmdAccess(MuxCommand):
    """
    show your current game access

    Usage:
      access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """
    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:all()"

    def func(self):
        "Load the permission groups"

        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY
        string = "\n{wPermission Hierarchy{n (climbing):\n %s" % ", ".join(hierarchy_full)
        #hierarchy = [p.lower() for p in hierarchy_full]

        if self.caller.player.is_superuser:
            cperms = "<Superuser>"
            pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.player.permissions.all())

        string += "\n{wYour access{n:"
        string += "\nCharacter {c%s{n: %s" % (caller.key, cperms)
        if hasattr(caller, 'player'):
            string += "\nPlayer {c%s{n: %s" % (caller.player.key, pperms)
        caller.msg(string)
