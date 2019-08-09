import numpy as np
import blosc

class State:

    IMAGE_SIZE = 84
    useCompression = False

    @staticmethod
    def setup(args):
        State.useCompression = args.compress_replay

    def stateByAddingScreen(self, screen, frameNumber):
        screen = np.dot(screen, np.array([.299, .587, .114])).astype(np.uint8)
        screen.resize((State.IMAGE_SIZE, State.IMAGE_SIZE, 1))
        
        if State.useCompression:
            screen = blosc.compress(
                np.reshape(screen, State.IMAGE_SIZE * State.IMAGE_SIZE).tobytes(), typesize=1)

        newState = State()
        if hasattr(self, 'screens'):
            newState.screens = self.screens[:3]
            newState.screens.insert(0, screen)
        else:
            newState.screens = [screen, screen, screen, screen]
        return newState
    
    def getScreens(self):
        if State.useCompression:
            s = []
            for i in range(4):
                s.append(np.reshape(np.fromstring(
                    blosc.decompress(
                        self.screens[i]), dtype=np.uint8), (State.IMAGE_SIZE, State.IMAGE_SIZE, 1)))
        else:
            s = self.screens
        return np.concatenate(s, axis=2)
