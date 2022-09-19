import RPi.GPIO as GPIO
import time
import smtplib
import _thread
import cred

try:
    need_clean = False

    MSG  = '\nDoor was '
    DOOR_MSG = {True:'opened', False:'closed'}

    print('Setting up SMS...')
    def send_msg(closed:bool):
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login( cred.FROM, cred.PASS )
        str_print =''.join([MSG, DOOR_MSG[opened], ' at ',
                            time.strftime('%I:%M:%S %p')])
        print(str_print)
        server.sendmail(cred.FROM, cred.TO, str_print)
        server.quit()



    print('Setting up hardware...')
    PIN = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    next_state = True

    need_clean = True

    print('Ready!')
    while True:
        if GPIO.input(PIN) == next_state:
            _thread.start_new_thread(send_msg, (next_state,))
            next_state = not next_state
        time.sleep(0.8)
        
except KeyboardInterrupt:
    GPIO.cleanup() #For Keyboard Interrupt exit
    need_clean = False

if need_clean:    
    GPIO.cleanup() #For normal exit
print('\nEnd!')
