import State
import random
def starting_state():

    # initialize all state variables
    state = State()

    # Starting FEL
    future_event_list = list()

    r = random.random()
    is_alone = 1 if r < 0.3 else 0

    future_event_list.append({'Event Type': 'Arrival','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event
    return state, future_event_list

