"""

Template module for Exits

Copy this module up one level and name it as you like, then
use it as a template to create your own Exits.

To make the default commands (such as @dig/@open) default to creating exits
of your new type, change settings.BASE_EXIT_TYPECLASS to point to
your new class, e.g.

settings.BASE_EXIT_TYPECLASS = "game.gamesrc.objects.myexit.MyExit"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
from ev import Exit as DefaultExit


class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the 'destination' property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use at_object_creation instead)
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg 'force_init'
                              should force a rebuild of the cmdset, this is triggered
                              by the @alias command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute err_traverse is not defined.

    Relevant hooks to overload (compared to other types of Objects):
    at_before_traverse(traveller) - called just before traversing
    at_after_traverse(traveller, source_loc) - called just after traversing
    at_failed_traverse(traveller) - called if traversal failed for some reason. Will
                                    not be called if the attribute 'err_traverse' is
                                    defined, in which case that will simply be echoed.
    """

    def return_appearance(self,looker):
       return self.destination.return_appearance(looker)


#    def at_object_leave(self, moved_obj, target_location):
#        """
#        Called just before an object leaves from inside this object
#
#        moved_obj - the object leaving
#        target_location - where the object is going.
#        """
#        pass
#
#    def at_object_receive(self, moved_obj, source_location):
#        """
#        Called after an object has been moved into this object.
#
#        moved_obj - the object moved into this one
#        source_location - where moved_object came from.
#        """
#        pass
#
#    def at_before_traverse(self, traversing_object):
#        """
#        Called just before an object uses this object to
#        traverse to another object (i.e. this object is a type of Exit)
#
#        The target location should normally be available as self.destination.
#        """
#        pass
#
#    def at_traverse(self, traversing_object, target_location):
#        """
#        This hook is responsible for handling the actual traversal, normally
#        by calling traversing_object.move_to(target_location). It is normally
#        only implemented by Exit objects. If it returns False (usually because
#        move_to returned False), at_after_traverse below should not be called
#        and instead at_failed_traverse should be called.
#        """
#        pass
#
#    def at_after_traverse(self, traversing_object, source_location):
#        """
#        Called just after an object successfully used this object to
#        traverse to another object (i.e. this object is a type of Exit)
#
#        The target location should normally be available as self.destination.
#        """
#        pass
#
#    def at_failed_traverse(self, traversing_object):
#        """
#        This is called if an object fails to traverse this object for some
#        reason. It will not be called if the attribute err_traverse is defined,
#        that attribute will then be echoed back instead.
#        """
#        pass
#
#
#    def at_msg_receive(self, text=None, **kwargs):
#        """
#        This hook is called whenever someone
#        sends a message to this object.
#
#        Note that from_obj may be None if the sender did
#        not include itself as an argument to the obj.msg()
#        call - so you have to check for this. .
#
#        Consider this a pre-processing method before
#        msg is passed on to the user sesssion. If this
#        method returns False, the msg will not be
#        passed on.
#        Input:
#            msg = the message received
#            from_obj = the one sending the message
#        Output:
#            boolean True/False
#        """
#        return True
#
#    def at_msg_send(self, text=None, to_obj=None, **kwargs):
#        """
#        This is a hook that is called when /this/ object
#        sends a message to another object with obj.msg()
#        while also specifying that it is the one sending.
#
#        Note that this method is executed on the object
#        passed along with the msg() function (i.e. using
#        obj.msg(msg, from_obj=caller) will then launch caller.at_msg())
#        and if no object was passed, it will never be called.
#        """
#        pass
#
#
