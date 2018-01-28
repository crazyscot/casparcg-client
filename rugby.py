import scorebug
import wx

class RugbyScoreBug(scorebug.ScoreBug):
    config_section='rugby'
    ui_label='Rugby score bug'

    def createSecondLine(self,sizer):
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        # Penalty and drop goal cannot be merged as league scores them differently...
        # Conversion and penalty cannot be merged as union scores them differently...
        self.addButton(line2, 'TRY', lambda e: self.score_try(1), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'CONV', lambda e: self.score_conv(1), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'PEN', lambda e: self.score_pen(1), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'DROP', lambda e: self.score_drop(1), True)

        line2.AddStretchSpacer(1)
        line2.Add(wx.StaticText(self, label='Remember to press Update'))
        line2.AddStretchSpacer(1)

        self.addButton(line2, 'TRY', lambda e: self.score_try(2), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'CONV', lambda e: self.score_conv(2), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'PEN', lambda e: self.score_pen(2), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'DROP', lambda e: self.score_drop(2), True)

        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)

    def score(self,team,points):
        if team==1:
            self.score1 += points
        else:
            self.score2 += points
        self.update_display()

    def score_try(self, team):
        self.score(team, 5)
    def score_conv(self, team):
        self.score(team, 2)
    def score_pen(self, team):
        self.score(team, 3)
    def score_drop(self, team):
        self.score(team, 3)
