from dbfpy import dbf


class SPARKSReader:
    """These objects can be used to read SPARKS formatted files. SPARKS uses
    the dBase format for data storage

    For more information on SPARKS see
    http://www2.isis.org/support/SPARKS/Pages/home.aspx

    For more information on dBase see https://en.wikipedia.org/wiki/.dbf
    """

    def __init__(self, filename):
        """Initialize an excelReader: object.

        Args:
           filename (str):  name of the file to read from

        Returns:
           SPARKSReader:
        """

        self.db = dbf.Dbf(filename)
        self.fieldNames = self.db.fieldNames

    def getRecordsAsList(self):
        """read all records from this file into a (2-dimensional) list. Each
        element of the list is list representing an entire row of data. In
        each internal list each element is a single column.

        Returns:
           list:
        """

        return_me = []
        for record in self.db:
            return_me.append(record.fieldData)
        return return_me