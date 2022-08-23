from PyQt6.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout

class PlayinCard(QWidget):
    def __init__(self, Function:str, subfunction1 = None, subfunction2 = None, subfunction3 = None, subfunction4 = None):
        super(PlayinCard, self).__init__()
        self.setObjectName("PlayinCard")

        self.pc_layout = QVBoxLayout()
        self.setLayout(self.pc_layout)

        self.pc_mainfunction = QPushButton()
        self.pc_mainfunction.setObjectName('PC_main')
        self.pc_mainfunction.setText(Function)

        self.pc_subfunction1 = QPushButton()
        self.pc_subfunction1.setObjectName('PC_sub1')
        self.pc_subfunction1.setText(subfunction1)
        self.pc_subfunction2 = QPushButton()
        self.pc_subfunction2.setObjectName('PC_sub2')
        self.pc_subfunction2.setText(subfunction2)
        self.pc_subfunction3 = QPushButton()
        self.pc_subfunction3.setObjectName('PC_sub3')
        self.pc_subfunction3.setText(subfunction3)
        self.pc_subfunction4 = QPushButton()
        self.pc_subfunction4.setObjectName('PC_sub4')
        self.pc_subfunction4.setText(subfunction4)

        self.pc_layout.addWidget(self.pc_mainfunction)
        self.pc_layout.addWidget(self.pc_subfunction1)
        self.pc_layout.addWidget(self.pc_subfunction2)
        self.pc_layout.addWidget(self.pc_subfunction3)
        self.pc_layout.addWidget(self.pc_subfunction4)


