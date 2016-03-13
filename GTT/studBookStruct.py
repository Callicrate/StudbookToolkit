from collections import OrderedDict
from datetime import *


class studbook:
    """These objects are base object for GTT. All reader and writer modules in
    this project use this to data structure for translating data from one
    format to another.

    Leveraging the capabilities of this project does not require any
    understanding of this data structure but if you are looking to create a new
    reader or writer you just need to read into and write from this structure
    """

    def __init__(self):
        """Initialize an studbook: object.

        Returns:
           studbook:
        """
        self.numberOfRecords = 0
        self.directory = []
        self.header = []

    # assuming each entry in the list is a complete record, add all the records to the studbook
    def addRecordsFromList(self, listOfRecords):
        """Read in a list of records and add them all to this object

        Args:
           listOfRecords (list):  Each element of the list is a list
           representing an entire row of data. In each internal list each
           element is a single column.

        Returns:
           nothing
        """
        for record in listOfRecords:
            sbr = _StudbookRecord()
            sbr.PopulateAllData(record)
            self.addRecord(sbr)

    # add a single record to the studbook based on template chick data (and provided $sire & $dam)
    def addChickRecord(self, sire, dam):
        """append a single record to this object based on a template chick data and input variables

        Args:
           sire (str): name of the sire to be considered (FIXME: check that these are supposed to be string/names)

           dam (str): name of the dam to be considered (FIXME: check that these are supposed to be string/names)

        Returns:
           nothing
        """
        sbr = _StudbookRecord()
        sbr.populateNewChickData(dam, sire)
        self.addRecord(sbr)

    # add a single record of type studbookRecord
    def addRecord(self, record):
        """append a single record to this object

        Args:
           record (_StudbookRecord): object to add to this object

        Returns:
           nothing
        """
        if isinstance(record, _StudbookRecord):
            self.directory.append(record)
        else:
            print "ERROR: records can only be of type studbookRecord!"

    # assume that $move is (a list) a move line from Moves.dbf
    # return "ADDED" if it was added, "PRESENT" if already there, "FAIL" otherwise
    def addMove(self, move):
        """dunno

        Args:
           move (list): dunno

        Returns:
           ADDED (str): means something
           FAIL (str): means something
           PRESENT (str): means something
        """

        mSTUD_ID = move[0]
        for record in self.directory:
            if record.data['STUD_ID'] == mSTUD_ID:
                returnValue = record.hasMove(move)
                if returnValue == -1:
                    record.addMove(move)
                    return "ADDED"
                else:
                    return "PRESENT @ index", str(returnValue)
        return "FAIL"

    # headers are a simple list (to be printed 1-entry per row)
    def addHeader(self, data):
        """ headers are, for now, data that is known to be needed at the top of
        an excel file or DBF file. this needs to be generalized since those two
        things are not the only data-types in the world but that is where we
        are for now.

        Args:
           data (list):  each element of the list represents a single column of
           data (in excel). This variable represents a single row of data
           (again, in excel)

        Returns:
           nothing
        """

        self.header.append(data)


class _StudbookRecord:
    """These objects are the internal records inside studbook: objects. These
    objects should not be needed to be used directly by translators and can be
    considered internal/private objects
    """

    def __init__(self):
        """Initialize a studbookRecord: object"""

        self.created = False
        self.myMoves = []

        # default data used below s what a theoretical chick would end up needing. We currently assume that
        # a real animal will be COMPLETELY filled out when added
        self.data = OrderedDict([
                    ('STUD_ID', ''),
                    ('DAM_ID', ''),
                    ('SIRE_ID', ''),
                    ('BDATE', datetime.today().date()),
                    ('BIRTH_EST', ''),
                    ('SEX', 5),
                    ('ID', ''),
                    ('DID', ''),
                    ('SID', ''),
                    ('DATEIN', datetime.today().date()),
                    ('IN_EST', ''),
                    ('DATEOUT', ''),
                    ('OUT_EST', ''),
                    ('DEATHDATE', ''),
                    ('DEATH_EST', ''),
                    ('LOCATION', 'CHICK'),
                    ('LOCAL_ID', ''),
                    ('INSTCODE', ''),
                    ('SOCIALGRP', ''),
                    ('SELECTED', 'TRUE'),
                    ('DEAD', 'FALSE'),
                    ('DAM_ID_TMP', ''),
                    ('SIRE_IDTMP', ''),
                    ('INBREED', 0),
                    ('AGE', 0),
                    ('KNOWN', -1),
                    ('INBREED_KN', -1),
                    ('MK', -1),
                    ('MK_KN', -1),
                    ('KV', -1),
                    ('KV_KN', -1),
                    ('VX', -1),
                    ('GU_ALL', -1),
                    ('GU_DESC', -1),
                    ('PR_LOST', 0),
                    ('COMMENT', '2016_HYPO_CHICK')
                    ])

    def PopulateAllData(self, inputList):
        """given list: input, populate all internal data with the list. This
        function is EXTREMELY dependant on the data being in the right order
        in the input list. Currently no data validation of any kind is going on
        USE AT YOUR OWN RISK.

        Args:
           inputList (list):  each element of this list represents an internal data element of studbookRecord:

        Returns:
           nothing
        """

        if self.created:
            print "ERROR, Trying to re-assign the values for this record (this is way bad!)"

        i = 0
        for key in self.data.keys():
            self.data[key] = inputList[i]
            i += 1

        self.created = True

    def populateNewChickData(self, DAM_ID, SIRE_ID):
        """given a dam and sire (maw & paw) fill out this record with what the
        chick would be. We're currently really only using default values for a
        chick and adding the DAM and SIRE, not a lot of math is going on here
        to guess what a chick should 'be'

        Args:
           DAM_ID (str):  identifier of the DAM

           SIRE_ID (str): identifier of the SIRE

        Returns:
           nothing
        """

        if self.created:
            print "ERROR, Trying to re-assign the values for this record (this is way bad!)"

        self.data['DAM_ID'] = DAM_ID
        self.data['SIRE_ID'] = SIRE_ID
        self.data['STUD_ID'] = "H"+str(DAM_ID)+"_16"

        self.created = True


    # does this record have a move that matches $move
    # return -1 if not present, otherwise return the index of which move matches
    def hasMove(self, move):
        """each studbookRecord has internal data representing 'moves', we are
        checking this record to see if we have a move that matches the input
        argument

        Args:
           move (list):  a move record

        Returns:
           int: Return the index of the match in this object's move list when
           found. If no match found then return -1
        """

        counter = 0
        for sMove in self.myMoves:
            counter += 1
            i = 0
            match = True
            while i < len(sMove):
                if not sMove[i] == move[i]:
                    match = False
                    break
                i += 1
            if match:
                return counter-1  # index is 1 less than counter
        return -1  # no matches found, return -1


    # blindly add $move to self.myMoves (without checking if $move
    # already is in this record)
    def addMove(self, move):
        """Without checking if it already exists, add the input argument to
        this object's move list.

        Args:
           move (list): move record to add

        Returns:
           nothing
        """

        self.myMoves.append(move)

    def returnExcelFormat(self):
        """return a list that is formatted for output to ExcelWriter. This is
        the wrong way to go about it of course, this object should just output
        data and the onus should be on ExcelWriter to format it however but
        that's where we are today

        Returns:
           list:
        """

        returnMe = []

        # first, get the 'main' row of data
        row = []
        for key in self.data.keys():
            row.append(self.data[key])
        returnMe.append(row)

        # now get all the 'moves' rows
        row = []
        for move in self.myMoves:
            returnMe.append(move)

        return returnMe
