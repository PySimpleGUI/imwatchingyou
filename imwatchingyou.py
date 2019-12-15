import PySimpleGUI as sg
import inspect
import textwrap
from time import sleep

version = __version__ = '2.3.0 Released 14-Dec-2019'

"""
    A "Live Debugging Tool" - "Watch" your code without stopping it.  Graphical user interface
    Cointains a "REPL" that you can use to run code, etc
"""

PSGDebugLogo = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

red_x = b"R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="

COLOR_SCHEME = 'LightGreen'

WIDTH_VARIABLES = 23
WIDTH_RESULTS = 46

WIDTH_WATCHER_VARIABLES = 20
WIDTH_WATCHER_RESULTS = 60

WIDTH_LOCALS = 80
NUM_AUTO_WATCH = 9

MAX_LINES_PER_RESULT_FLOATING = 4
MAX_LINES_PER_RESULT_MAIN      = 3

POPOUT_WINDOW_FONT = 'Sans 8'

class Debugger():

    debugger = None

    #     #                    ######
    ##   ##   ##   # #    #    #     # ###### #####  #    #  ####   ####  ###### #####
    # # # #  #  #  # ##   #    #     # #      #    # #    # #    # #    # #      #    #
    #  #  # #    # # # #  #    #     # #####  #####  #    # #      #      #####  #    #
    #     # ###### # #  # #    #     # #      #    # #    # #  ### #  ### #      #####
    #     # #    # # #   ##    #     # #      #    # #    # #    # #    # #      #   #
    #     # #    # # #    #    ######  ###### #####   ####   ####   ####  ###### #    #

    def __init__(self):
        self.watcher_window = None  # type: Window
        self.popout_window = None  # type: Window
        self.local_choices = {}
        self.myrc = ''
        self.custom_watch = ''
        self.locals = {}
        self.globals = {}
        self.popout_choices = {}


    # Includes the DUAL PANE (now 2 tabs)!  Don't forget REPL is there too!
    def _build_main_debugger_window(self, location=(None, None)):
        sg.ChangeLookAndFeel(COLOR_SCHEME)

        def InVar(key1):
            row1 = [sg.T('    '),
                    sg.I(key=key1, size=(WIDTH_VARIABLES, 1)),
                    sg.T('', key=key1 + 'CHANGED_', size=(WIDTH_RESULTS, 1)), sg.B('Detail', key=key1 + 'DETAIL_'),
                    sg.B('Obj', key=key1 + 'OBJ_'), ]
            return row1

        variables_frame = [InVar('_VAR0_'),
                           InVar('_VAR1_'),
                           InVar('_VAR2_'), ]

        interactive_frame = [[sg.T('>>> '), sg.In(size=(83, 1), key='_REPL_',
                                tooltip='Type in any "expression" or "statement"\n and it will be disaplayed below.\nPress RETURN KEY instead of "Go"\nbutton for faster use'),
                              sg.B('Go', bind_return_key=True, visible=True)],
                             # [sg.T('CODE >>> ', justification='r', size=(9, 1)), sg.In(size=(83, 1), key='_CODE_', tooltip='Use for things like import or other statements / lines of code')],
                             [sg.Multiline(size=(93, 26), key='_OUTPUT_', autoscroll=True, do_not_clear=True)], ]

        autowatch_frame = [[sg.Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                            sg.Button('Clear All Auto Watches'),
                            sg.Button('Show All Variables', key='_SHOW_ALL_'),
                            sg.Button('Locals', key='_ALL_LOCALS_'),
                            sg.Button('Globals', key='_GLOBALS_'),
                            sg.Button('Popout', key='_POPOUT_')]]

        variable_values =  [[sg.T('', size=(WIDTH_WATCHER_VARIABLES, 1), key='_WATCH%s_' % i),
                               sg.T('', size=(WIDTH_WATCHER_RESULTS, MAX_LINES_PER_RESULT_MAIN), key='_WATCH%s_RESULT_' % i,
                                    )] for i in range(NUM_AUTO_WATCH)]

        var_layout = []
        for i in range(NUM_AUTO_WATCH):
            var_layout.append([sg.T('', size=(WIDTH_WATCHER_VARIABLES, 1), key='_WATCH%s_' % i),
              sg.T('', size=(WIDTH_WATCHER_RESULTS, MAX_LINES_PER_RESULT_MAIN), key='_WATCH%s_RESULT_' % i,
                    )])

        col1 = [
            # [sg.Frame('Auto Watches', autowatch_frame+variable_values, title_color='blue')]
            [sg.Frame('Auto Watches', autowatch_frame+var_layout, title_color='blue')]
        ]

        col2 = [
            [sg.Frame('Variables or Expressions to Watch', variables_frame, title_color='blue'), ],
            [sg.Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue'), ]
        ]

        # Tab based layout
        layout = [[sg.TabGroup([[sg.Tab('Variables', col1), sg.Tab('REPL & Watches', col2)]])],
                  [sg.Button('', image_data=red_x, key='_EXIT_', button_color=None),]]

        # ------------------------------- Create main window -------------------------------
        window = sg.Window("I'm Watching You Debugger", layout, icon=PSGDebugLogo, margins=(0, 0), location=location).Finalize()
        window.Element('_VAR1_').SetFocus()
        self.watcher_window = window
        sg.ChangeLookAndFeel('SystemDefault')           # set look and feel to default before exiting
        return window

    #     #                    #######                               #
    ##   ##   ##   # #    #    #       #    # ###### #    # #####    #        ####   ####  #####
    # # # #  #  #  # ##   #    #       #    # #      ##   #   #      #       #    # #    # #    #
    #  #  # #    # # # #  #    #####   #    # #####  # #  #   #      #       #    # #    # #    #
    #     # ###### # #  # #    #       #    # #      #  # #   #      #       #    # #    # #####
    #     # #    # # #   ##    #        #  #  #      #   ##   #      #       #    # #    # #
    #     # #    # # #    #    #######   ##   ###### #    #   #      #######  ####   ####  #

    def _refresh_main_debugger_window(self, mylocals, myglobals):
        if not self.watcher_window:     # if there is no window setup, nothing to do
            return False
        event, values = self.watcher_window.Read(timeout=1)
        if event in (None, 'Exit', '_EXIT_'):  # EXIT BUTTON / X BUTTON
            try:
                self.watcher_window.Close()
            except: pass
            self.watcher_window = None
            return False
        # ------------------------------- Process events from REPL Tab -------------------------------
        cmd = values['_REPL_']                  # get the REPL entered
        # BUTTON - GO (NOTE - This button is invisible!!)
        if event == 'Go':  # GO BUTTON
            self.watcher_window.Element('_REPL_').Update('')
            self.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)

            try:
                result = eval('{}'.format(cmd), myglobals, mylocals)
            except Exception as e:
                try:
                    result = exec('{}'.format(cmd), myglobals, mylocals)
                except Exception as e:
                    result = 'Exception {}\n'.format(e)

            self.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(result), append=True, autoscroll=True)
        # BUTTON - DETAIL
        elif event.endswith('_DETAIL_'):  # DETAIL BUTTON
            var = values['_VAR{}_'.format(event[4])]
            try:
                result = str(eval(str(var), myglobals, mylocals))
            except:
                result = ''
            sg.PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + result, title=var, non_blocking=True)
        # BUTTON - OBJ
        elif event.endswith('_OBJ_'):  # OBJECT BUTTON
            var = values['_VAR{}_'.format(event[4])]
            expression = 'sg.ObjToStringSingleObj({})'.format(var)
            try:
                result = str(eval(expression, myglobals, mylocals))
            except:
                result = ''
            sg.PopupScrolled(str(var) + '\n' + result, title=var, non_blocking=True)
        # ------------------------------- Process Watch Tab -------------------------------
        # BUTTON - Choose Locals to see
        elif event == '_LOCALS_':  # Show all locals BUTTON
            self._choose_auto_watches(mylocals)
        # BUTTON - Locals (quick popup)
        elif event == '_ALL_LOCALS_':
            self._display_all_vars(mylocals)
        # BUTTON - Globals (quick popup)
        elif event == '_GLOBALS_':
            self._display_all_vars(myglobals)
        # BUTTON - clear all
        elif event == 'Clear All Auto Watches':
            if sg.PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
                self.local_choices = {}
                self.custom_watch = ''
        # BUTTON - Popout
        elif event == '_POPOUT_':
            if not self.popout_window:
                self._build_floating_window()
        # BUTTON - Show All
        elif event == '_SHOW_ALL_':
            for key in self.locals:
                self.local_choices[key] = not key.startswith('_')

        # -------------------- Process the manual "watch list" ------------------
        for i in range(3):
            key = '_VAR{}_'.format(i)
            out_key = '_VAR{}_CHANGED_'.format(i)
            self.myrc = ''
            if self.watcher_window.Element(key):
                var = values[key]
                try:
                    result = eval(str(var), myglobals, mylocals)
                except:
                    result = ''
                self.watcher_window.Element(out_key).Update(str(result))
            else:
                self.watcher_window.Element(out_key).Update('')

        # -------------------- Process the automatic "watch list" ------------------
        slot = 0
        for key in self.local_choices:
            if key == '_CUSTOM_WATCH_':
                continue
            if self.local_choices[key]:
                self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(key)
                try:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot), silent_on_error=True).Update(mylocals[key])
                except:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update('')
                slot += 1

            if slot + int(not self.custom_watch in (None, '')) >= NUM_AUTO_WATCH:
                break
        # If a custom watch was set, display that value in the window
        if self.custom_watch:
            self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(self.custom_watch)
            try:
                self.myrc = eval(self.custom_watch, myglobals, mylocals)
            except:
                self.myrc = ''
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(self.myrc)
            slot += 1
        # blank out all of the slots not used (blank)
        for i in range(slot, NUM_AUTO_WATCH):
            self.watcher_window.Element('_WATCH{}_'.format(i)).Update('')
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

        return True     # return indicating the window stayed open

    ######                                 #     #
    #     #  ####  #####  #    # #####     #  #  # # #    # #####   ####  #    #
    #     # #    # #    # #    # #    #    #  #  # # ##   # #    # #    # #    #
    ######  #    # #    # #    # #    #    #  #  # # # #  # #    # #    # #    #
    #       #    # #####  #    # #####     #  #  # # #  # # #    # #    # # ## #
    #       #    # #      #    # #         #  #  # # #   ## #    # #    # ##  ##
    #        ####  #       ####  #          ## ##  # #    # #####   ####  #    #

    ######                                    #                     #     #
    #     # #    # #    # #####   ####       # #   #      #         #     #   ##   #####   ####
    #     # #    # ##  ## #    # #          #   #  #      #         #     #  #  #  #    # #
    #     # #    # # ## # #    #  ####     #     # #      #         #     # #    # #    #  ####
    #     # #    # #    # #####       #    ####### #      #          #   #  ###### #####       #
    #     # #    # #    # #      #    #    #     # #      #           # #   #    # #   #  #    #
    ######   ####  #    # #       ####     #     # ###### ######       #    #    # #    #  ####
    # displays them into a single text box

    def _display_all_vars(self, dict):
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        out_text = 'All of your Vars'
        longest_line = max([len(key) for key in dict])
        line = []
        sorted_dict = {}
        for key in sorted(dict.keys()):
            sorted_dict[key] = dict[key]
        for key in sorted_dict:
            value = dict[key]
            wrapped_list = textwrap.wrap(str(value), 60)
            wrapped_text = '\n'.join(wrapped_list)
            out_text += '{} - {}\n'.format(key, wrapped_text)
            if cur_col + 1 == num_cols:
                cur_col = 0
                num_lines += len(wrapped_list)
            else:
                cur_col += 1
        sg.ScrolledTextBox(out_text, non_blocking=True)

 #####                                        #     #
#     # #    #  ####   ####   ####  ######    #  #  #   ##   #####  ####  #    #
#       #    # #    # #    # #      #         #  #  #  #  #    #   #    # #    #
#       ###### #    # #    #  ####  #####     #  #  # #    #   #   #      ######
#       #    # #    # #    #      # #         #  #  # ######   #   #      #    #
#     # #    # #    # #    # #    # #         #  #  # #    #   #   #    # #    #
 #####  #    #  ####   ####   ####  ######     ## ##  #    #   #    ####  #    #

#     #                                                       #     #
#     #   ##   #####  #   ##   #####  #      ######  ####     #  #  # # #    #
#     #  #  #  #    # #  #  #  #    # #      #      #         #  #  # # ##   #
#     # #    # #    # # #    # #####  #      #####   ####     #  #  # # # #  #
 #   #  ###### #####  # ###### #    # #      #           #    #  #  # # #  # #
  # #   #    # #   #  # #    # #    # #      #      #    #    #  #  # # #   ##
   #    #    # #    # # #    # #####  ###### ######  ####      ## ##  # #    #

    def _choose_auto_watches(self, my_locals):
        sg.ChangeLookAndFeel(COLOR_SCHEME)
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        layout = [[sg.Text('Choose your "Auto Watch" variables', font='ANY 14', text_color='red')]]
        longest_line = max([len(key) for key in my_locals])
        line = []
        sorted_dict = {}
        for key in sorted(my_locals.keys()):
            sorted_dict[key] = my_locals[key]
        for key in sorted_dict:
            line.append(sg.CB(key, key=key, size=(longest_line, 1),
                              default=self.local_choices[key] if key in self.local_choices else False))
            if cur_col + 1 == num_cols:
                cur_col = 0
                layout.append(line)
                line = []
            else:
                cur_col += 1
        if cur_col:
            layout.append(line)

        layout += [
            [sg.Text('Custom Watch (any expression)'), sg.Input(default_text=self.custom_watch, size=(40, 1), key='_CUSTOM_WATCH_')]]
        layout += [
            [sg.Ok(), sg.Cancel(), sg.Button('Clear All'), sg.Button('Select [almost] All', key='_AUTO_SELECT_')]]

        window = sg.Window('All Locals', layout, icon=PSGDebugLogo).Finalize()

        while True:  # event loop
            event, values = window.Read()
            if event in (None, 'Cancel'):
                break
            elif event == 'Ok':
                self.local_choices = values
                self.custom_watch = values['_CUSTOM_WATCH_']
                break
            elif event == 'Clear All':
                sg.PopupQuickMessage('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True,
                                     text_color='red', font='ANY 18')
                for key in sorted_dict:
                    window.Element(key).Update(False)
                window.Element('_CUSTOM_WATCH_').Update('')
            elif event == 'Select All':
                for key in sorted_dict:
                    window.Element(key).Update(False)
            elif event == '_AUTO_SELECT_':
                for key in sorted_dict:
                    window.Element(key).Update(not key.startswith('_'))

        # exited event loop
        window.Close()
        sg.ChangeLookAndFeel('SystemDefault')

    ######                            #######
    #     # #    # # #      #####     #       #       ####    ##   ##### # #    #  ####
    #     # #    # # #      #    #    #       #      #    #  #  #    #   # ##   # #    #
    ######  #    # # #      #    #    #####   #      #    # #    #   #   # # #  # #
    #     # #    # # #      #    #    #       #      #    # ######   #   # #  # # #  ###
    #     # #    # # #      #    #    #       #      #    # #    #   #   # #   ## #    #
    ######   ####  # ###### #####     #       ######  ####  #    #   #   # #    #  ####

    #     #
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
     ## ##  # #    # #####   ####  #    #

    def _build_floating_window(self, location=(None, None)):
        if self.popout_window:              # if floating window already exists, close it first
            self.popout_window.Close()
        sg.ChangeLookAndFeel('Topanga')
        num_cols = 2
        width_var = 15
        width_value = 30
        layout = []
        line = []
        col = 0
        # self.popout_choices = self.local_choices      # commented out so that ALL locals will be shown
        self.popout_choices = {}                        # make sure all none _ variables shown
        if self.popout_choices == {}:                   # if nothing chosen, then choose all non-_ variables
            for key in sorted(self.locals.keys()):
                self.popout_choices[key] = not key.startswith('_')

        width_var = max([len(key) for key in self.popout_choices])
        for key in self.popout_choices:
            if self.popout_choices[key] is True:
                value = str(self.locals.get(key))
                h = min(len(value)//width_value + 1, MAX_LINES_PER_RESULT_FLOATING)
                line += [sg.Text(f'{key}', size=(width_var, 1), font=POPOUT_WINDOW_FONT),
                         sg.Text(' = ', font=POPOUT_WINDOW_FONT),
                         sg.Text(value, key=key, size=(width_value, h), font=POPOUT_WINDOW_FONT)]
                if col + 1 < num_cols:
                    line += [sg.VerticalSeparator(), sg.T(' ')]
                col += 1
            if col >= num_cols:
                layout.append(line)
                line = []
                col = 0
        if col != 0:
            layout.append(line)
        layout = [[sg.Column(layout), sg.Column(
            [[sg.Button('', key='_EXIT_', image_data=red_x, button_color=('#282923', '#282923'), border_width=0)]])]]

        self.popout_window = sg.Window('Floating', layout, alpha_channel=0, no_titlebar=True, grab_anywhere=True,
                                           element_padding=(0, 0), margins=(0, 0), keep_on_top=True,
                                       right_click_menu=['&Right', ['Debugger::RightClick', 'Exit::RightClick']], location=location ).Finalize()
        if location == (None, None):
            screen_size = self.popout_window.GetScreenDimensions()
            self.popout_window.Move(screen_size[0] - self.popout_window.Size[0], 0)
        self.popout_window.SetAlpha(1)

        sg.ChangeLookAndFeel('SystemDefault')
        return True

    ######
    #     # ###### ###### #####  ######  ####  #    #
    #     # #      #      #    # #      #      #    #
    ######  #####  #####  #    # #####   ####  ######
    #   #   #      #      #####  #           # #    #
    #    #  #      #      #   #  #      #    # #    #
    #     # ###### #      #    # ######  ####  #    #

    #######
    #       #       ####    ##   ##### # #    #  ####
    #       #      #    #  #  #    #   # ##   # #    #
    #####   #      #    # #    #   #   # # #  # #
    #       #      #    # ######   #   # #  # # #  ###
    #       #      #    # #    #   #   # #   ## #    #
    #       ######  ####  #    #   #   # #    #  ####

    #     #
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
     ## ##  # #    # #####   ####  #    #

    def _refresh_floating_window(self):
        if not self.popout_window:
            return
        for key in self.popout_choices:
            if self.popout_choices[key] is True and key in self.locals:
                if key is not None:
                    self.popout_window.Element(key, silent_on_error=True).Update(self.locals.get(key))
        event, values = self.popout_window.Read(timeout=1)
        if event in (None, '_EXIT_', 'Exit::RightClick'):
            self.popout_window.Close()
            self.popout_window = None
        elif event == 'Debugger::RightClick':
            show_debugger_window()


# 888     888                                .d8888b.         d8888 888 888          888      888
# 888     888                               d88P  Y88b       d88888 888 888          888      888
# 888     888                               888    888      d88P888 888 888          888      888
# 888     888 .d8888b   .d88b.  888d888     888            d88P 888 888 888  8888b.  88888b.  888  .d88b.
# 888     888 88K      d8P  Y8b 888P"       888           d88P  888 888 888     "88b 888 "88b 888 d8P  Y8b
# 888     888 "Y8888b. 88888888 888         888    888   d88P   888 888 888 .d888888 888  888 888 88888888
# Y88b. .d88P      X88 Y8b.     888         Y88b  d88P  d8888888888 888 888 888  888 888 d88P 888 Y8b.
#  "Y88888P"   88888P'  "Y8888  888          "Y8888P"  d88P     888 888 888 "Y888888 88888P"  888  "Y8888

# 8888888888                            888    d8b
# 888                                   888    Y8P
# 888                                   888
# 8888888    888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b
# 888        888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K
# 888        888  888 888  888 888      888    888 888  888 888  888 "Y8888b.
# 888        Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88
# 888         "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'


def show_debugger_window(location=(None, None)):
    '''
    Display the main debugger window with its 2 tabs
    :return:
    '''
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame

    if not debugger.watcher_window:
        debugger.watcher_window = debugger._build_main_debugger_window(location=location)
    return True


def show_debugger_popout_window(location=(None, None)):
    '''
    Display the popout window in the upper right corner of screen
    :return:
    '''
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame = inspect.getframeinfo(prev_frame)
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if debugger.popout_window:
        debugger.popout_window.Close()
        debugger.popout_window = None
    debugger._build_floating_window(location=location)



def refresh_debugger():
    '''
    MUST be called periodically (once a second?) to update the main and floating windows
    :return: bool - True if OK, False if debugger window was closed. (not important to know usually)
    '''
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    sg.Window.read_call_from_debugger = True
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    debugger._refresh_floating_window() if debugger.popout_window else None
    rc = debugger._refresh_main_debugger_window(debugger.locals, debugger.globals) if debugger.watcher_window else False
    sg.Window.read_call_from_debugger = False
    return rc


def main():
    print('Running the test harness... you should normally not see this. Import rather than run this package')
    show_debugger_window()
    i = 0
    while True:
        sleep(.1)
        refresh_debugger()
        i += 1

if __name__ == '__main__':
    main()
    