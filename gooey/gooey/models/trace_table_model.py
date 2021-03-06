from PyQt5.QtCore import (QModelIndex, QAbstractTableModel, Qt)
from models.trace import Trace


class TraceTableModel(QAbstractTableModel):
    def __init__(self, parent=None, traces=None):
        super(TraceTableModel, self).__init__(parent)

        if traces is None:
            self.traces = []
        else:
            self.traces = traces


    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows this model holds. """
        return len(self.traces)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns this model holds. """
        # Documentation seem to always return a hard coded value. Probably in case self.traces is empty.
        return 5

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data.
            If not returning data, return None
        """

        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.traces):
            return None

        if role == Qt.DisplayRole:
            time = self.traces[index.row()].time
            can_id = self.traces[index.row()].can_id
            data = self.traces[index.row()].data
            rxtx = self.traces[index.row()].rxtx
            dlc = self.traces[index.row()].dlc

            if index.column() == 0:
                return time
            elif index.column() == 1:
                return can_id
            elif index.column() == 2:
                return rxtx
            elif index.column() == 3:
                return dlc
            elif index.column() == 4:
                return data

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed """

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Time"
            elif section == 1:
                return "CAN-ID"
            elif section == 2:
                return "RX/TX"
            elif section == 3:
                return "Length"
            elif section == 4:
                return "Data"

        return None

    def insertRow(self, trace, index=QModelIndex()):
        """ Insert a row into the model. """

        position = len(self.traces)
        self.beginInsertRows(QModelIndex(), position, position)
        self.traces.insert(position, trace)
        self.endInsertRows()
        return True

    def removeRow(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """

        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self.traces[position:position+rows]
        self.endRemoveRows()

        return True

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given index
            and role 
        """

        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.traces):
            trace = self.traces[index.row()]
            if index.column() == 0:
                trace.time = value
            elif index.column() == 1:
                trace.can_id = value
            elif index.column() == 2:
                trace.rxtx = value
            elif index.column() == 3:
                trace.dlc = value
            elif index.column() == 4:
                trace.data = value
            else:
                False

            self.dataChanged.emit(index, index)
            return True

        return False


    def flags(self, index):
        """ Set the item flags at the given index. """

        if not index.isValid():
            return Qt.ItemIsEnabled

        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
