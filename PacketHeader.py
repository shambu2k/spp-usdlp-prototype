from bitarray import bitarray
from bitarray.util import ba2int, int2ba

class PrimaryHeader:

    def __init__(self):
        self.primary_header = bitarray(48)
        self.primary_header.setall(0)

        self.primary_header_contents = {
            """3-bit Packet Version Number"""
            'pkt_ver': self.primary_header[0:3],

            """Packet Identification Field"""
            'pkt_type': self.primary_header[3],
            'sec_hdr_flg': self.primary_header[4],
            'apid': self.primary_header[5:16],

            """Packet Sequence Control"""
            'seq_flg': self.primary_header[16:18],
            'pkt_name': self.primary_header[18:32],

            """Packet Data Length"""
            'pkt_data_length': self.primary_header[32:48]
        }

        """This function returns the header contents in int"""
        def getField(self, field):
            if(field in self.primary_header_contents):
                return ba2int(self.primary_header_contents[field])
            else: return "Invalid field"

        def addSecondaryHeader(self, secondaryBitArray):
            self.primary_header.extend(secondaryBitArray)
        
        def resetSecondaryHeader(self, secondaryBitArray):
            if(len(self.primary_header) < 48):
                self.primary_header.extend(secondaryBitArray)
            else:
                self.primary_header[48:48+(len(secondaryBitArray))] = secondaryBitArray
            

class SecondaryHeader:
    def __init__(self, primaryHeader, tcf_len, adf_len):
        self.secondary_header = bitarray(tcf_len + adf_len)
        self.secondary_header_contents = {
            'time_code_field': bitarray(tcf_len),
            'ancillary_data_field': bitarray(adf_len)
        }
        primaryHeader.addSecondary(self.secondary_header)
    
    def setSecondaryHeader(self, primary_header, secondaryHeaderData):
        tcf, adf, tcflen, adflen = secondaryHeaderData.tcf, secondaryHeaderData.adf, secondaryHeaderData.tcflen, secondaryHeaderData.adflen 
        if(len(int2ba(tct)) > tcflen):
            return "Can't set, Time Code Field too big"
        elif(len(int2ba(adf)) > adflen):
            return "Can't set, Ancillary Field too big"
        else:
            self.secondary_header_contents['time_code_field'] = int2ba(adf)
            self.secondary_header_contents['ancillary_data_field'] = int2ba(tcf)
            self.secondary_header.extend(self.secondary_header_contents['time_code_field'])
            self.secondary_header.extend(self.secondary_header_contents['ancillary_data_field'])
            primary_header.resetSecondaryHeader(self.secondary_header)
