
def starting_state():

    # State variables
    state = dict()
    state['Queue Length'] = 0
    state['Server Status'] = 0  # 0: Free, 1: Busy

    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'Arrival', 'Event Time': 0})  # This is an Event