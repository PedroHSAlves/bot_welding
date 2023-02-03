from wellding_input import electrode_update
from psq_input import psq_update
from dadosbosch_input import dadosbosch_update
from alarms_input import alarms_update
import time
import msvcrt

star_time = time.time()
print("running program...")#Debug print

alarms_update()
psq_update()
electrode_update() 
dadosbosch_update()

print(f"End of execution, time elapsed:   {time.time() - star_time}")#Debug print
print("\nPress any key to finish the program...")

key_pressed = False
while not key_pressed and time.time() - star_time < 3600:
    if msvcrt.kbhit():
        msvcrt.getch()
        key_pressed = True

print("Closed program...")