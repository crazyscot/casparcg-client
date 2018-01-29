import scorebug
import wx
import configurable

RugbyCode = configurable.ListConfigItem('Code', 'Which rugby code\'s scoring rules', ['Union','League'])

ScoresByCode = {
        'Union': { 'try': 5, 'convertedtry': 7, 'penalty': 3, 'dropgoal': 3 },
        'League': { 'try': 4, 'convertedtry': 6, 'penalty': 2, 'dropgoal': 1 },
}

class RugbyScoreBug(scorebug.ScoreBug):
    config_section='rugby'
    ui_label='Rugby score bug'
    my_configurations=[configurable.Template,configurable.Layer, RugbyCode]
    my_default_config={'Template': 'mediary/scorebug', 'Layer': 102, RugbyCode.label: 'Union'}

    def createSecondLine(self,sizer):
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        # Penalty and drop goal cannot be merged as league scores them differently...
        # Conversion and penalty cannot be merged as union scores them differently...
        self.addButton(line2, 'TRY', lambda e: self.score(1, 'try'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'TRY+CONV', lambda e: self.score(1, 'convertedtry'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'PEN', lambda e: self.score(1, 'penalty'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'DROP', lambda e: self.score(1, 'dropgoal'), True)

        line2.AddStretchSpacer(1)

        self.addButton(line2, 'TRY', lambda e: self.score(2, 'try'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'TRY+CONV', lambda e: self.score(2, 'convertedtry'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'PEN', lambda e: self.score(2, 'penalty'), True)
        line2.AddSpacer(10)
        self.addButton(line2, 'DROP', lambda e: self.score(2, 'dropgoal'), True)

        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)

    def code(self):
        return self.config.get(self.config_section, RugbyCode.label, RugbyScoreBug.my_default_config[RugbyCode.label])

    def score(self,team,event):
        delta = ScoresByCode[self.code()][event]
        super(RugbyScoreBug, self).score(team, delta)
