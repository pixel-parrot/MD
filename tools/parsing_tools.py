# Parsing related tools. 

import re
from tools.text_tools import TextTools as TT
from tools.list_tools import ListTools as LT

class ParsingTools:

    # The general parser.
    def parser(self, caller, cmdstring, args):
        '''
        This parses the input string and returns string-matches for a numeric argument
            as well as adjectives, objects, and prepositions in the order below. The 
            first value it returns is always a boolean flagging whether the parsing was
            successful.
                successful
                numeric argument
                adjectives 1
                object 1
                prepositions 1
                adjectives 2
                object 2
                prepositions 2
                adjectives 3
                object 3
                prepositions 3
                adjectives 4
                object 4

        After importing this into a command module, it is always used with
            the general format of:

        successful, num1, adj1, obj1, prep1, adj2, obj2, prep2, adj3, obj3, prep3, adj4, obj4 = ParsingTools.parser(ParsingTools(), self.caller, self.cmdstring, self.args)

        After that, command-specific object identifcation and preposition validation can be done
            in the command's func method using the variables holding the returned values.

        This parser catches bad-attempts at the input-string-level, but object-specific and command-specific
            bad attempt catching will need to be done in the command's func method.

        This is only for objects in the same 'room'. We'll need a
            similar module for interactions between remote objects
            (or just give an optional end-argument that defines a different mode)
        '''

        # initializing strings
        successful = True
        numeric_string = ''
        object_string_1 = ''
        object_string_2 = ''
        object_string_3 = ''
        object_string_4 = ''
        adjective_string_1 = ''
        adjective_string_2 = ''
        adjective_string_3 = ''
        adjective_string_4 = ''
        preposition_string_1 = ''
        preposition_string_2 = ''
        preposition_string_3 = ''

        # removing articles from the input string
        args_original = args.strip()
        args = args.strip()
        articles = TT.articleList(TT())
        caller.msg('args1: ' + args)
        for word in args_original.split():
            if word in articles:
                for word2 in args.split():
                    if word2 == word:
                        args = args.replace(word2, '', 1)
                        args = args.replace('  ', ' ', 1)
                        break
            continue
        args = args.strip()
        caller.msg('args2: ' + args)

        # getting the arguments
        prepositions = TT.prepositionList(TT())
        preps = '|'.join(prepositions)
        raw_list = [string.strip() for string in re.split('\\s?(\d*)[\\s?(.*?)]\\s?('+preps+')?\\s?(.*?)\\s?('+preps+')?\\s?(.*?)\\s?('+preps+')?\\s?(.*?)', args) if string]
        #caller.msg('raw_list: ' + str(raw_list))

        # extracting numeric argument if any:
        if raw_list[0].isdigit():
            numeric_string = raw_list.pop(0)

        # extracting the prepositions used
        preps_used = []
        working_list = raw_list
        for phrase in raw_list:
            prep_count = 0
            for word in phrase.split():
                if word in prepositions:
                    prep_count += 1
            if prep_count == len(phrase.split()):
                preps_used.append(working_list.pop(working_list.index(phrase)))
        for phrase in preps_used:
            if len(preps_used) == 1:
                preposition_string_1 = preps_used[0]
            if len(preps_used) == 2:
                preposition_string_1 = preps_used[0]
                preposition_string_2 = preps_used[1]
            if len(preps_used) == 3:
                preposition_string_1 = preps_used[0]
                preposition_string_2 = preps_used[1]
                preposition_string_3 = preps_used[2]

        # getting a list of objects in the caller's location that are contained by either containers
        #   or sitting on a surface (which is just a different sort of container-like object)
        contained_lists = []
        contained_lists.extend([container.contents for container in caller.location.contents if 'container' in container.tags.all() or 'surface' in container.tags.all()])
        contained = []
        [contained.extend(obj) for obj in contained_lists]

        # extracting the local object keys: this would be everything contained by the caller's location,
        #   anything contained by a stack in the caller's location, anything sitting on a surface in the
        #   caller's location, and finally the location itself
        all_local_keys = [obj.key for obj in caller.location.contents]
        all_local_keys.extend(obj.key for obj in contained if contained)
        all_local_keys.append(caller.location.key)
        #caller.msg('all local keys: ' + str(all_local_keys))

        # extracting the local object aliases: this would be everything contained by the caller's location,
        #   anything contained by a stack in the caller's location, anything sitting on a surface in the
        #   caller's location, and finally the location itself
        all_local_aliases_list = [obj.aliases.all() for obj in caller.location.contents if obj.aliases.all()]
        [all_local_aliases_list.extend(obj.aliases.all()) for obj in contained if contained] 
        all_local_aliases = []
        [all_local_aliases.extend(lst) for lst in all_local_aliases_list]
        #caller.msg('all local aliases: ' + str(all_local_aliases))

        # extracting potential-object strings
        object_strings = []
        #caller.msg('working list: ' + str(working_list))
        for phrase in working_list:
            obj_string = ''
            for word in phrase.split():
                if word in ''.join(all_local_keys) or word in ''.join(all_local_aliases):
                    if not obj_string:
                        obj_string = word
                    else:
                        obj_string = obj_string + ' ' + word
            #caller.msg('obj_string: ' + obj_string)
            if obj_string in all_local_keys or obj_string in all_local_aliases:
                object_strings.append(obj_string)
            else:
                object_strings.append('')
        #caller.msg('object_strings: ' + str(object_strings))
        object_strings_temp = [string for string in object_strings if string]
        #caller.msg('object_strings_temp: ' + str(object_strings_temp))
        for phrase in object_strings_temp:
            if len(object_strings_temp) == 1:
                object_string_1 = object_strings_temp[0].strip()
            if len(object_strings_temp) == 2:
                object_string_1 = object_strings_temp[0].strip()
                object_string_2 = object_strings_temp[1].strip()
            if len(object_strings_temp) == 3:
                object_string_1 = object_strings_temp[0].strip()
                object_string_2 = object_strings_temp[1].strip()
                object_string_3 = object_strings_temp[2].strip()
            if len(object_strings_temp) == 4:
                object_string_1 = object_strings_temp[0].strip()
                object_string_2 = object_strings_temp[1].strip()
                object_string_3 = object_strings_temp[2].strip()
                object_string_4 = object_strings_temp[3].strip()
        #caller.msg('obj string 1: ' + object_string_1)
        #caller.msg('obj string 2: ' + object_string_2)
        #caller.msg('obj string 3: ' + object_string_3)
        #caller.msg('obj string 4: ' + object_string_4)

        # extracting adjective strings
        adjective_strings = []
        adjective_strings_temp = []
        #caller.msg('working list: ' + str(working_list))
        for i,phrase in enumerate(working_list):
            adjstring = phrase.replace(object_strings[i],'')
            if adjstring:
                adjective_strings_temp.insert(i,adjstring)
            else:
                adjective_strings_temp.insert(i,'END')
        #caller.msg('adjective strings_temp: ' + str(adjective_strings_temp))
        counter = 0
        for word in adjective_strings_temp:
            if counter == 0:
                adj_temp_list = []
                adj_temp = ''
            if word <> 'END':
                adj_temp_list.append(word)
                counter = counter + 1
            else:
                counter = 0
                adj_temp = ' '.join(adj_temp_list)
                adjective_strings.append(adj_temp)
        # removing adjectives from working_list
        #for word in adjective_strings_temp:
        #    if word in working_list:
        #        working_list.remove(word)
        #caller.msg('adjective strings: ' + str(adjective_strings))
        for phrase in adjective_strings:
            if len(adjective_strings) == 1:
                adjective_string_1 = adjective_strings[0].strip()
            if len(adjective_strings) == 2:
                adjective_string_1 = adjective_strings[0].strip()
                adjective_string_2 = adjective_strings[1].strip()
            if len(adjective_strings) == 3:
                adjective_string_1 = adjective_strings[0].strip()
                adjective_string_2 = adjective_strings[1].strip()
                adjective_string_3 = adjective_strings[2].strip()
            if len(adjective_strings) == 4:
                adjective_string_1 = adjective_strings[0].strip()
                adjective_string_2 = adjective_strings[1].strip()
                adjective_string_3 = adjective_strings[2].strip()
                adjective_string_4 = adjective_strings[3].strip()
        #caller.msg('adj string 1: ' + adjective_string_1)
        #caller.msg('adj string 2: ' + adjective_string_2)
        #caller.msg('adj string 3: ' + adjective_string_3)
        #caller.msg('adj string 4: ' + adjective_string_4)


        # catching bad attempts
        if successful == True and adjective_string_1 in prepositions:
            caller.msg(cmdstring.capitalize() + ' what?')
            successful = False
        if successful == True and not object_string_1:
            caller.msg(cmdstring.capitalize() + ' what?')
            successful = False
        if successful == True and preposition_string_1 and not object_string_2:
            caller.msg(cmdstring.capitalize() + ' what?')
            #caller.msg(cmdstring.capitalize() + ' ' + object_string_1 + ' ' + preposition_string_1 + ' what?')
            successful = False
        if successful == True and preposition_string_2 and not object_string_3:
            caller.msg(cmdstring.capitalize() + ' what?')
            #caller.msg(cmdstring.capitalize() + ' ' + object_string_1 + ' ' + preposition_string_1 + ' ' + object_string_2 + ' ' + preposition_string_2 + ' what?')
            successful = False
        if successful == True and preposition_string_3 and not object_string_4:
            caller.msg(cmdstring.capitalize() + ' what?')
            #caller.msg(cmdstring.capitalize() + ' ' + object_string_1 + ' ' + preposition_string_1 + ' ' + object_string_2 + ' ' + preposition_string_2 + ' what?')
            successful = False

        return successful, numeric_string, adjective_string_1, object_string_1, preposition_string_1, adjective_string_2, object_string_2, preposition_string_2, adjective_string_3, object_string_3, preposition_string_3, adjective_string_4, object_string_4
