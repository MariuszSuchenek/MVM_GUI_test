class ESP32BaseAlarm:
    '''
    The base ESP Alarm Class
    '''

    alarm_to_string = {
        0: "Alarm name",
    }

    def __init__(self, number):
        '''
        Constructor

        arguments:
        - the number obtained from the ESP
        '''
        self.number = number

    def __bool__(self):
        return self.number != 0

    def __str__(self):
        return 'All alarms: ' + ' - '.join(self.strerror_all())

    def unpack(self):
        '''
        Unpacks the number obtained from the ESP
        '''

        self.alarms = list(filter(lambda x: x, [ self.number & (1<<test) for test in range(32)]))

        print('Found alarms', self.alarms)

        return self.alarms


    def strerror(self, n):
        '''
        Returns a string with the error
        specified by n

        arguments:
        - n: the error number (unpacked)
        '''
        if not hasattr(self, 'alarms'):
            self.unpack()

        if n in self.alarm_to_string:
            return self.alarm_to_string[n]
        else:
            return 'Unknown error'

    def strerror_all(self, append_err_no=False):
        '''
        Same as strerror, but returns a list
        in case of multiple errors

        arguments:
        - append_err_no: if True, also adds the err number
        '''
        if not hasattr(self, 'alarms'):
            self.unpack()

        str_error = []
        for n in self.alarms:

            s = self.strerror(n)

            if append_err_no:
                s += ' (code: '
                s += str(n)
                s += ')'

            str_error.append(s)

        return str_error



class ESP32Alarm(ESP32BaseAlarm):

    alarm_to_string = {
        # From the ESP
        1 << 0: "Gas pressure too low",
        1 << 1: "Gas pressure too high",
        1 << 2: "Internal pressure too low (internal leakage)",
        1 << 3: "Internal pressure too high",
        1 << 4: "Out of battery power",
        1 << 5: "Leakage in gas circuit",
        1 << 6: "Obstruction in idraulic circuit",
        1 << 7: "Partial obstruction in idraulic circuit",
        # From the GUI
        1 << 8: "Pressure to patient mouth too low",
        1 << 9: "Pressure to patient mouth too high",
        1 << 10: "Inpiratory flux too low",
        1 << 11: "Inpiratory flux too high",
        1 << 12: "Expiratory flux too low",
        1 << 13: "Expiratory flux too high",
        1 << 14: "Tidal volume too low",
        1 << 15: "Tidal volume too high",
        1 << 16: "O2 too low",
        1 << 17: "O2 too high",
        1 << 18: "PEEP too low",
        1 << 19: "PEEP too high",
        1 << 20: "Respiratory rate too low",
        1 << 21: "Respiratory rate too high",

        # from the ESP
        1 << 29: "GUI alarm raised",
        1 << 30: "GUI watchdog not reset",
        1 << 31: "System failure",
    }

class ESP32Warning(ESP32BaseAlarm):

    alarm_to_string = {
        # From the ESP
        1 << 0: "Oxygen sensor requires calibration",
        1 << 1: "Disconnected from power outlet",
    }
