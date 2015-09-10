# popup.selectChannel
# Tim Crowson, March 2015

# This is an example of using basic model view programming with a custom filter for
# searching through a list of items and performing an operation on the selection.

# The overall data flow goes something like this:
#   1-  Gather all the data you want to search through. In this case it's just a list of strings (channel names)
#   2-  Feed that data into a model object, in this case a QStringListModel
#   3-  Display this model's data in a view (QListView in this case). But rather than display it directly,
#       first feed the data into a proxy model (QSortFilterProxyModel), and then feed the proxy model into the view.
#   4- Implement a simple event (changing the text in the search field) to trigger
#       an update to the proxy's filter, using a regex as the filter rule.
#   5- Process the selected data and do something with it.


import lx
import lxu
import modo

from PySide.QtGui import *
from PySide.QtCore import *


class CustomStringModel(QStringListModel):
    '''
    Custom Qt Data model derived from a simple string list, from which
    we'll populate our view widget.

    Simple implementations can get by with QStringListModel objects,
    but more complex ones will require other data models, such as
    QAbstractTableModel, for example.
    '''
    def __init__(self, data=[], parent=None):
        ''' '''
        super(CustomStringModel, self).__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        ''' '''
        return len(self._data)

    def data(self, index, role=None):
        ''' '''
        row = index.row()
        column = index.column()
        value = self._data[row]
        if role == Qt.DisplayRole:
            return value


class Popup(QDialog):
    '''
     pop-up search field
    '''
    def __init__(self):
        '''
        Constructor
        '''
        QDialog.__init__(self)

        # since exec_() is unstable, use setModal()
        # Turns out setModal() may also be unstabe, so...
        #self.setModal(True)

        # ensure the widget it deleted when closed
        self.setAttribute(Qt.WA_DeleteOnClose)

        # remove the window frame, ensure pop-up look and feel
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        # gather data to display in our listView
        self.selection = modo.Scene().selected[0]
        self.channels = self.selection.channelNames

        # create a label
        self.label = QLabel('Select a channel...')
        self.label.setAlignment(Qt.AlignCenter)

        # create a search field and set it to accept custom events
        self.lineEdit = QLineEdit('', self)
        self.lineEdit.installEventFilter(self)
        
        # create a non-editable list view and set it to accept custom events
        self.listView = QListView()
        self.listView.setFixedWidth(200)
        self.listView.installEventFilter(self)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # set up a data model with a proxy so we can filter it
        self.listModel = CustomStringModel(self.channels)
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.listModel)
        
        # set the model on the listView
        self.listView.setModel(self.proxyModel)

        # create a layout and add our widgets to it
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.listView)

        # set connections   
        self.lineEdit.textChanged.connect(self.updateList)
        self.lineEdit.returnPressed.connect(self.process_selection)
        self.listView.doubleClicked.connect(self.process_selection)

        # set the layout and focus on the search field
        self.setLayout(self.layout)
        self.lineEdit.setFocus()

    def updateList(self):
        '''
        Update the filtering on the QListView
        '''
        # define an expression to check against
        self.regExp = QRegExp(self.lineEdit.text(), Qt.CaseInsensitive, QRegExp.FixedString)

        # apply the regex as a filter, which will update the listView
        self.proxyModel.setFilterRegExp(self.regExp)
        
        # keep the top-most item highlighted
        self.listView.setCurrentIndex(self.listView.model().index(0,0))

    def eventFilter(self, widget, event):
        '''
        Catch specific events to create a streamlined behavior.
        '''
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if widget == self.lineEdit and key == Qt.Key_Down:
                self.listView.setFocus()
                self.listView.setCurrentIndex(self.listView.model().index(1,0))
                return True

            if widget is self.listView and key == Qt.Key_Backspace:
                self.lineEdit.setFocus()
                return True

            if widget is self.listView and key == Qt.Key_Return:
                self.process_selection()
                return True

            return False
        return False

    def process_selection(self):
        '''
        Process the selection.
        '''
        index = self.listView.currentIndex()
        
        if index.isValid():
            data = str(self.proxyModel.data(index))
            try:
                lx.eval('select.channel  {%s:%s} set' %(self.selection.Ident(), data))
            except:
                modo.dialogs.alert('Failed', 'Unable to select the channels. See Event Log for details', dtype='warning')
        self.close()


class SelectChannel ( lxu.command.BasicCommand ):
    '''
    Custom Command to spawn the popup.
    '''
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Interact(self):
        '''
        Boilerplate
        '''

    def cmd_Flags(self):
        '''
        Provide an undo context
        '''
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        '''
        Display the pop-up search field.
        '''
        if len(modo.Scene().selected) > 0:
            self.popup = Popup()

            # Move the dialog to the cursor position
            self.popup.move( QCursor().pos() )

            # Using exec_() causes instabilities, so we'll use show() instead
            # and set the dialog as modal in its constructor via setModal()
            self.popup.show()


# Bless this mess!
lx.bless(SelectChannel, "popup.selectChannel")

