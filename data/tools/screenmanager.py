
class Screen(object):

    def __init__(self):
        self.persist = {}
        self.done = False
        self.next = None

    def startup(self, persist):
        self.done = False
        self.persist = persist

    def cleanup(self):
        return self.persist

    def update(self):
        pass

    def get_event(self,event):
        pass

class ScreenManager(object):

    def __init__(self):
        self.states = {}
        self.previous = None
        self.current = None


    def setup_states(self,start_state,state_dict):
        self.current = start_state
        self.states = state_dict

    def flip_states(self,next_state):
        p = self.states[self.current].cleanup()
        self.current = next_state
        self.states[self.current].startup(p)



    def update(self,dt):
        if self.states[self.current].done == True:
            next_state = self.states[self.current].next
            self.flip_states(next_state)
        else:
            self.states[self.current].update(dt)


    def get_event(self,event):
        self.states[self.current].get_event(event)


    def draw(self,surface):
        self.states[self.current].draw(surface)

