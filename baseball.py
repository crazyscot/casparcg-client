#!/usr/bin/env python3
#
# This file was contributed to Mediary's Caspar Client by Jason Bowles,
# under the same license terms as the rest of the package.
# https://github.com/crazyscot/casparcg-client/pull/10
#

import scorebug
import wx
import scoreextra
import amcp
import sys, time, threading
import configurable
from configurable import ConfigItem
from widget import Widget

Template_bug = ConfigItem(label='Bug Template', helptext='Caspar template to use to put score up as a bug')
Template_banner = ConfigItem(label='Banner Template', helptext='Caspar template to use to put score up as a banner')

class BaseballScore(scorebug.ScoreBug):
    '''
   
    '''
    config_section='baseball'
    ui_label='Baseball'
    use_banner = False
    
    def __init__(self, parent, config):
        self.inning = 1
        super().__init__(parent, config)
        self.extractrl.SetValue(f"INN 1")
    
    @property
    def outs(self):
        return self.parent.widget_instances['Beneath Score Bug (clashes with Timer)']

    def createSecondLine(self,sizer):
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        self.addButton(line2,'+1', lambda e: self.score(1, 1), True)
        line2.AddSpacer(10)
        self.addButton(line2,'-1', lambda e: self.score(1, -1))
        line2.AddStretchSpacer(1)
        line2.AddSpacer(2)
        self.addButton(line2,'END INNING', lambda e: self.end_inning(), True)
        line2.AddSpacer(2)
        self.addButton(line2,'+INN', lambda e: self.update_inning(1), True)
        line2.AddSpacer(2)
        self.addButton(line2,'-INN', lambda e: self.update_inning(-1), True)
        line2.AddSpacer(2)
        self.addButton(line2,'FINAL SCORE', lambda e: self.show_final(), True)
        line2.AddSpacer(2)
        line2.AddStretchSpacer(1)
        line2.AddSpacer(10)
        self.addButton(line2,'+1', lambda e: self.score(2, 1), True)
        line2.AddSpacer(10)
        self.addButton(line2,'-1', lambda e: self.score(2, -1))
        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)
    
    def show_final(self):
        self.outs.do_anim_off(None)
        self.do_anim_off(None)
        t = threading.Timer(0.5,self.show_banner)
        t.start()
        
    def end_inning(self):
        self.outs.do_anim_off(None)
        self.do_anim_off(None)
        t = threading.Timer(0.2,self.show_inn_banner )
        t.start()
    
    def show_inn_banner(self):
        endInn = f"End of Inning: {self.inning}"
        self.show_banner(textValue=endInn)
        self.inning = self.inning + 1
        self.extractrl.SetValue(f"INN {self.inning}")
        self.outs.setOuts()
    
    def show_banner(self, textValue='FINAL SCORE'):
        self.use_banner = True
        self.extractrl.SetValue(textValue)
        self.do_anim_on(None)
        self.use_banner = False
        self.extractrl.SetValue(f"INN {self.inning}")
         
    def update_inning(self,innValue):
        self.inning = self.inning + innValue
        self.extractrl.SetValue(f"INN {self.inning}")
        self.do_update(None)
    
    def do_anim_off(self, event):
        self.outs.do_anim_off(event)
        return super().do_anim_off(event)
    
    def template(self):
        sel = self.bb_choices[self.bb_choice.GetSelection()]
        if sel=='Bug' and not self.use_banner:
            d = self.my_default_config[Template_bug.label]
            self.outs.do_anim_on(None)
            return self.config.get(self.config_section, Template_bug.label, self.my_default_config[Template_bug.label])
        else:
            return self.config.get(self.config_section, Template_banner.label, self.my_default_config[Template_banner.label])
        
class BaseballOuts(scoreextra.ScoreExtra):
    '''
    '''
    def __init__(self, parent, config):
        self.outs = 0
        super().__init__(parent, config, uiLabel='Baseball Outs')
    
    def createControl(self, sizer):
        #self.text = wx.TextCtrl(self,2,value=f"INN {self.inning_num}")
        #sizer.Add(self.text,2,flag=wx.Expand)
        sizer.AddStretchSpacer(1)
        self.addButton(sizer,'0 OUTS', self.zeroOut)
        sizer.AddStretchSpacer(1)
        self.addButton(sizer,'1 OUT', self.oneOut)
        sizer.AddStretchSpacer(1)
        self.addButton(sizer,'2 OUTS', self.twoOut)
    
    def templateData(self):
        rv = amcp.jsondata({
            'line1': str(f"OUTS - {self.outs}"),
            })
        return rv
    
    def setOuts(self,inOuts=0):
        self.outs = inOuts
    
    def zeroOut(self,event):
        self.outs = 0
        self.do_anim_on(event)
    
    def oneOut(self,event):
        self.outs = 1
        self.do_update(event)
    
    def twoOut(self,event):
        self.outs = 2
        self.do_update(event)
        
class BaseballRecorder(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section = 'recording_file_name'
    ui_label = 'RECORD GAME'
    my_default_config={'Template': 'mediary/recording', 'Layer': 109, 'FileName': 'baseball_overlay.mp4'}
    def __init__(self, parent, config):
        super(BaseballRecorder,self).__init__(parent,label=self.ui_label)
        self.parent = parent
        self.config = config
        self.filename = self.config.get(self.config_section, 'FileName', 'baseball_overlay.mp4') #'baseball_overlay.mp4'
        self.recording = False

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        line1 = wx.BoxSizer(wx.HORIZONTAL)

        self.createControl(line1)

        # Then: Fade On, Fade Off, Update
        line1.AddStretchSpacer(1)
        self.addButton(line1,'RECORD', self.do_record)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'STOP RECORDING', self.stop_record)
        line1.AddStretchSpacer(1)
        
        sizer.Add(line1, 0, wx.EXPAND)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def createControl(self, sizer):
        self.text = wx.TextCtrl(self, 2, value=self.filename)
        sizer.Add(self.text, 2, flag=wx.EXPAND)
        
    def do_record(self,event):
        '''
        ADD 1-1 FILE baseball_overlay.mp4 -codec:v h264_nvenc -profile:v high444p -pixel_format:v yuv444p -preset:v default
        '''
        self.filename = self.text.GetValue()
        self.recording = True
        self.parent.transact(f"ADD 1-1 FILE {self.filename} -codec:v h264_nvenc -profile:v high444p -pixel_format:v yuv444p -preset:v default")
        
    def stop_record(self,event):
        if self.recording:
            self.parent.transact("REMOVE 1-1 FILE")
            self.recording = False
        
        

class BaseballAction(wx.StaticBox, Widget):

    my_configurations=[configurable.Template,configurable.Layer]
    config_section='lowerthird'
    ui_label='Baseball Action'
    my_default_config={'Template': 'mediary/lowerthird', 'Layer': 101}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(BaseballAction, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config
        self.current_action_text = "Play Ball!!!"

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)
            
        safe = wx.BoxSizer(wx.HORIZONTAL)
        out = wx.BoxSizer(wx.HORIZONTAL)
        bases = wx.BoxSizer(wx.HORIZONTAL)
        err = wx.BoxSizer(wx.HORIZONTAL)

        batter_safe = {'BB':'Walk',
                       '1B':'Single',
                  '2B':'Double',
                  '3B':'Triple',
                  "HR":"Home Run"}
        
        batter_out = {'K':'Strike Out',
                  'FB':'Fly Out',
                  'GB':'Ground Out',
                  'DP':'Double Play',
                  'FC':'Fielders Choice',
                  'IF':"Infield Fly",
                  'SAC':'Sacrifice'}
        
        baserunner = {'SB':'Stolen Base',
                  'CS':'Caught Stealing',
                  'WP':'Wild Pitch',
                  'PB': 'Passed Ball',
                  'PK': 'Picked Off',
                  "BK": "Balk"}
        
        error = {'E':'Error',
                 "BI":"Batter Interference",
                 "CI":"Catcher Interference",
                 "RI":"Runner Interference"}
        
        #self.addAction(inner,'PK', 'Picked Off')

        sizer.AddSpacer(15)
        #sizer.Add(inner, flag=wx.EXPAND)
        safe.AddSpacer(10)
        safe.Add(wx.StaticText(self, wx.ID_ANY, 'Batter Safe'))
        safe.AddSpacer(42)
        self.addActionGroup(sizer,safe,batter_safe)
        
        out.AddSpacer(10)
        out.Add(wx.StaticText(self, wx.ID_ANY, 'Batter Out'))
        out.AddSpacer(40)
        self.addActionGroup(sizer,out,batter_out)
        
        bases.AddSpacer(10)
        bases.Add(wx.StaticText(self,wx.ID_ANY,"BaseRunner Plays"))
        bases.AddSpacer(10)
        self.addActionGroup(sizer,bases,baserunner)
        
        err.AddSpacer(10)
        err.Add(wx.StaticText(self,wx.ID_ANY,"Errors/Misplays"))
        err.AddSpacer(20)
        self.addActionGroup(sizer,err,error)
        sizer.AddSpacer(20)

        sizer.AddStretchSpacer()
    
    def addActionGroup(self,sizer,spacer,plays):
        for play in list(plays.keys()):
            self.addAction(spacer,play,plays[play])
        sizer.Add(spacer,0,wx.EXPAND)
        
    def addAction(self, line, label, text):
        btn = self.addButton(line,label,lambda e: self.playAction(text))
        btn.SetToolTip(text)
        #line.AddStretchSpacer(1)
        

    def playAction(self,actionText,sleepTime=5):
        self.current_action_text = actionText
        self.do_anim_on(None)
        if sleepTime is not None:
            t = threading.Timer(sleepTime,self.removeAction)
            t.start()
    
    def removeAction(self):
        self.do_remove(None)

    def templateData(self):
        return amcp.jsondata({
            'name': self.current_action_text,
            'title': '',
            'colourB': '#000000',
            'colourA': '#ffffff',
            })

if __name__=='__main__':
    import wxclient
    # This is the set of widgets to load when this script is invoked directly.
    wxclient.run_app([BaseballScore, BaseballOuts, BaseballAction,BaseballRecorder])
