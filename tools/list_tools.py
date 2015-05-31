# A collection of tools to use with lists.

class ListTools:

    # A method to remove duplicates from a list.
    def dedupeList(self, listobj):
        listobjtemp = listobj
        count1 = 0
        count2 = 0
        while count1 < len(listobjtemp):
            for count2 in range(len(listobjtemp)):
                while count2 < len(listobjtemp):
                    if (count1 <> count2) and (listobjtemp[count1] == listobjtemp[count2]):
                        listobjtemp.pop(count2)
                        count2 = -1
                    count2 += 1
            count1 += 1
        return listobjtemp


