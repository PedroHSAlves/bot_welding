from wellding_input import electrode_update
from psq_input import psq_update
from dadosbosch_input import dadosbosch_update
from alarms_input import alarms_update
import time

star_time = time.time()
print("running program...")#Debug print

alarms_update()
dadosbosch_update()
psq_update()
electrode_update()

print(f"end code  {time.time() - star_time}")#Debug print