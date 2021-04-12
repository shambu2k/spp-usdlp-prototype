from PacketHeader import PrimaryHeader, SecondaryHeader

class Packet:
    
    def __init__(self, secondaryHeaderData = None, user_data_field = None):
        if(self.checkUserDataField(secondaryHeaderData, user_data_field)):
            primaryHeader = PrimaryHeader().primary_header
            self.packet = bitarray()
            self.packet.extend(primaryHeader)
            if(primaryHeader.getField(sec_hdr_flg)):
                secondaryHeader = SecondaryHeader()
                if(secondaryHeaderData != None):
                    secondaryHeader.setSecondaryHeader(primaryHeader, secondaryHeaderData)
                else:
                    return "Secondary Header Data Invalid"
                self.packet.extend(secondaryHeader)
                self.packet.extend(user_data_field)
            else:
                self.packet.extend(user_data_field)
        else:
            return "Nothing to initialize"
    
    def checkUserDataField(secondaryHeaderData = None, user_data_field):
        if(secondaryHeaderData==None and user_data_field == None):
            return False
        elif(secondaryHeaderData!=None and user_data_field == None)
            return False
        elif(secondaryHeaderData!=None and (len(user_data_field) > 65536*8 or len(user_data_field) < 1):
            return False
        else: return True

            
