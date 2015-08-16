# A module to hold any tools for checking types of proximity between objects.

class ProximityTools:

    def returnAdjacentTargets(self, caller, cmdstring, object1_adjective, object1_string, object1_list, object2_adjective, object2_string, object2_list, object3_adjective, object3_string, object3_list, object4_adjective, object4_string, object4_list):
        '''
        This returns a series of objects that match based on proximity. Before using
        this method, object1_list, object2_list, object3_list, and object4_list have to be defined
        using results from the parsing_tools.py's parser. The object string results from
        the parser and these lists are passed to this method. 
        An example of this can be found in sublocation_movement.py. 
        This also checks for cases where there are too many results and checks for 
        bad attempts. If a bad attempt is caught, the variable 'successful' will be
        returned as False, to be handled by the command that calls this method.
        '''

        # narrowing the object lists down based on proximity
        #caller.msg('object1_list: ' + str([obj.dbref for obj in object1_list]))
        #caller.msg('object2_list: ' + str([obj.dbref for obj in object2_list]))
        #caller.msg('object3_list: ' + str([obj.dbref for obj in object3_list]))
        #caller.msg('object4_list: ' + str([obj.dbref for obj in object4_list]))
        successful = True
        target_potential = []
        obj2_potential = []
        obj3_potential = []
        obj4_potential = []

        # identify potential objects for four objects specified
        if object4_list:
            # identify potential obj3s
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in object4_list]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in object4_list]
            obj3_potential = [obj for obj in object3_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj4: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj4: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('obj3_potential: ' + str([obj.dbref for obj in obj3_potential]))
            # identify potential obj2s
            obj2_potential = [obj for obj in object2_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj4: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj4: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('obj2_potential: ' + str([obj.dbref for obj in obj2_potential]))
            # identify potential obj4s by finding the one with obj2 near it and obj3 near it
            location_objects_nearby_obj2 = []
            [location_objects_nearby_obj2.extend(obj.db.location_objects_nearby) for obj in obj2_potential]
            objects_nearby_obj2 = []
            [objects_nearby_obj2.extend(obj.db.objects_nearby) for obj in obj2_potential]
            location_objects_nearby_obj3 = []
            [location_objects_nearby_obj3.extend(obj.db.location_objects_nearby) for obj in obj3_potential]
            objects_nearby_obj3 = []
            [objects_nearby_obj3.extend(obj.db.objects_nearby) for obj in obj3_potential]
            obj4_potential = [obj for obj in object4_list if obj in (location_objects_nearby_obj2 and location_objects_nearby_obj3) or obj in (objects_nearby_obj2 and objects_nearby_obj3)]
            #caller.msg('location_objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in location_objects_nearby_obj2]))
            #caller.msg('objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in objects_nearby_obj2]))
            #caller.msg('location_objects_nearby for obj3 potentials: ' + str([obj.dbref for obj in location_objects_nearby_obj3]))
            #caller.msg('objects_nearby for obj3 potentials: ' + str([obj.dbref for obj in objects_nearby_obj3]))
            #caller.msg('obj4_potential: ' + str([obj.dbref for obj in obj4_potential]))
            # identify object1 from the obj4_potential list
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in obj4_potential]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in obj4_potential]
            target_potential = [obj for obj in object1_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj4 potentials: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj4 potentials: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('target_potential: ' + str([obj.dbref for obj in target_potential]))
        # identify potential objects for three objects specified
        if object3_list:
            # identify potential obj2s
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in object3_list]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in object3_list]
            obj2_potential = [obj for obj in object2_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj3: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj3: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('obj2_potential: ' + str([obj.dbref for obj in obj2_potential]))
            # identify potential obj3s by finding the one with obj2 near it
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in obj2_potential]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in obj2_potential]
            obj3_potential = [obj for obj in object3_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('obj3_potential: ' + str([obj.dbref for obj in obj3_potential]))
            # identify object1 from that list
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in obj2_potential]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in obj2_potential]
            target_potential = [obj for obj in object1_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('target_potential: ' + str([obj.dbref for obj in target_potential]))
        # identify potential objects for two objects specified
        if object2_list and not object3_list:
            # identify potential obj2s
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in object1_list]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in object1_list]
            obj2_potential = [obj for obj in object2_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj1s: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj1s: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('obj2_potential: ' + str([obj.dbref for obj in obj2_potential]))
            # identify object1 from that list
            location_objects_nearby = []
            [location_objects_nearby.extend(obj.db.location_objects_nearby) for obj in obj2_potential]
            objects_nearby = []
            [objects_nearby.extend(obj.db.objects_nearby) for obj in obj2_potential]
            target_potential = [obj for obj in object1_list if obj in location_objects_nearby or obj in objects_nearby]
            #caller.msg('location_objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in location_objects_nearby]))
            #caller.msg('objects_nearby for obj2 potentials: ' + str([obj.dbref for obj in objects_nearby]))
            #caller.msg('target_potential: ' + str([obj.dbref for obj in target_potential]))
        # identify potential objects for one object specified
        if object1_list and not object2_list and not object3_list:
            # identify object1 
            target_potential = object1_list
            caller.msg('target_potential: ' + str([obj.dbref for obj in target_potential]))

        # catch bad attempts where there are no potential matches at this point
#        if not target_potential and object1_list:
#            caller.msg('You look around for a %s %s, but don''t see any.' %(object1_adjective, object1_string))
#            successful = False
#            return successful, target_potential, obj2_potential, obj3_potential
#        if not obj2_potential and object2_list:
#            caller.msg('You look around for a %s %s, but don''t see any.' %(object2_adjective, object2_string))
#            successful = False
#            return successful, target_potential, obj2_potential, obj3_potential
#        if not obj3_potential and object3_list:
#            caller.msg('You look around for a %s %s, but don''t see any.' %(object3_adjective, object3_string))
#            successful = False
#            return successful, target_potential, obj2_potential, obj3_potential

        m = 0
        caller.msg('mark 1')
        # identify potential objects by adjective string match
        adj_dic = {}
        if object1_adjective: 
            caller.msg('mark 2')
            for obj in target_potential:
                adj_lst = []
                for word_list in obj.db.adjective_list:
                    for word in word_list.split():
                        adj_lst.append(word)
                adj_dic[obj] = adj_lst
            if target_potential:
                target_potential = [obj for obj in target_potential if object1_adjective in obj.db.adjective_list or object1_adjective in adj_dic[obj]]
                if not target_potential:
                    caller.msg('You check there for a %s %s, but don''t see any.' %(object1_adjective, object1_string))
                    successful = False
                    return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        adj_dic = {}
        if object2_adjective: 
            caller.msg('mark 3')
            for obj in obj2_potential:
                adj_lst = []
                for word_list in obj.db.adjective_list:
                    for word in word_list.split():
                        adj_lst.append(word)
                adj_dic[obj] = adj_lst
            if obj2_potential:
                obj2_potential = [obj for obj in obj2_potential if object2_adjective in obj.db.adjective_list or object2_adjective in adj_dic[obj]]
                if not obj2_potential:
                    caller.msg('You look around for a %s %s, but don''t see any.' %(object2_adjective, object2_string))
                    successful = False
                    return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        adj_dic = {}
        if object3_adjective: 
            caller.msg('mark 4')
            for obj in obj3_potential:
                adj_lst = []
                for word_list in obj.db.adjective_list:
                    for word in word_list.split():
                        adj_lst.append(word)
                adj_dic[obj] = adj_lst
            if obj3_potential:
                obj3_potential = [obj for obj in obj3_potential if object3_adjective in obj.db.adjective_list or object3_adjective in adj_dic[obj]]
                if not obj3_potential:
                    caller.msg('You look around for a %s %s, but don''t see any.' %(object3_adjective, object3_string))
                    successful = False
                    return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        adj_dic = {}
        if object4_adjective: 
            caller.msg('mark 5')
            for obj in obj4_potential:
                adj_lst = []
                for word_list in obj.db.adjective_list:
                    for word in word_list.split():
                        adj_lst.append(word)
                adj_dic[obj] = adj_lst
            if obj4_potential:
                obj4_potential = [obj for obj in obj4_potential if object4_adjective in obj.db.adjective_list or object4_adjective in adj_dic[obj]]
                if not obj4_potential:
                    caller.msg('You look around for a %s %s, but don''t see any.' %(object4_adjective, object4_string))
                    successful = False
                    return successful, target_potential, obj2_potential, obj3_potential, obj4_potential

        # catch cases where there is more than one obj4_potential. This should be avoidable by
        #   having objects have specific identifiers when there are more than one in a room, like
        #   'east table', or by having unique descriptors like 'black table', and so on
        if object4_string and len(obj4_potential) > 1:
            caller.msg('mark 5')
            caller.msg('Which %s?' %(object4_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        # catch cases where there is more than one obj3_potential. This should be avoidable by
        #   having objects have specific identifiers when there are more than one in a room, like
        #   'east table', or by having unique descriptors like 'black table', and so on
        if object3_string and len(obj3_potential) > 1:
            caller.msg('mark 6')
            caller.msg('Which %s?' %(object3_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        # catch cases where there is more than one obj2_potential. This should be avoidable by
        #   having objects have specific identifiers when there are more than one in a room, like
        #   'east table', or by having unique descriptors like 'black table', and so on
        if object2_string and len(obj2_potential) > 1:
            caller.msg('mark 7')
            caller.msg('Which %s?' %(object2_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        # catch cases where there is more than one target_potential. This should be avoidable by
        #   having objects have specific identifiers when there are more than one in a room, like
        #   'east table', or by having unique descriptors like 'black table', and so on
        if len(target_potential) > 1:
            caller.msg('mark 8')
            caller.msg(cmdstring.capitalize() + ' which %s?' %(object1_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential

        # catch cases where the specified objects are not near each other
        obj1_string = 'The ' + object1_list[0].db.object_title
        if object2_list:
            obj2_string = 'the ' + object2_list[0].db.object_title
        if object3_list:
            obj3_string = 'the ' + object3_list[0].db.object_title
        if object4_list:
            obj4_string = 'the ' + object4_list[0].db.object_title
        if object1_adjective:
            obj1_string = 'The ' + object1_adjective + ' ' + object1_string
            if object2_adjective:
                if object2_list:
                    obj2_string = 'the ' + object2_adjective + ' ' + object2_string
            if object3_adjective:
                if object3_list:
                    obj3_string = 'the ' + object3_adjective + ' ' + object3_string
            if object4_adjective:
                if object4_list:
                    obj4_string = 'the ' + object4_adjective + ' ' + object4_string
        if 'character' in object1_list[0].tags.all() and caller.db.characters_met[object1_list[0]]:
            obj1_string = caller.db.characters_met[object1_list[0]]
        if object2_list and 'character' in object2_list[0].tags.all() and caller.db.characters_met[object2_list[0]]:
            obj2_string = caller.db.characters_met[object2_list[0]]
        if object3_list and 'character' in object3_list[0].tags.all() and caller.db.characters_met[object3_list[0]]:
            obj3_string = caller.db.characters_met[object3_list[0]]
        if object4_list and 'character' in object4_list[0].tags.all() and caller.db.characters_met[object4_list[0]]:
            obj4_string = caller.db.characters_met[object4_list[0]]
        # command has 4 objects specified
        if object4_list and (not obj2_potential or not obj3_potential or not obj4_potential or not target_potential):
            caller.msg('%s, %s, and %s are not near %s.' %(obj1_string, obj2_string, obj3_string, obj4_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        # command has 3 objects specified
        if object3_list and (not obj2_potential or not obj3_potential or not target_potential):
            caller.msg('%s and %s are not near %s.' %(obj1_string, obj2_string, obj3_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential
        # command has 2 objects specified
        if not object3_list and object2_list and (not obj2_potential or not target_potential):
            caller.msg('%s is not near %s.' %(obj1_string, obj2_string))
            successful = False
            return successful, target_potential, obj2_potential, obj3_potential, obj4_potential

        return successful, target_potential, obj2_potential, obj3_potential, obj4_potential



