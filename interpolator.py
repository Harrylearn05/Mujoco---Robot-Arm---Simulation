import numpy as np

class Interpolator:
    @staticmethod
    def lerp(start, end, t):
        #Linear Interpolator
        t = np.clip(t, 0.0, 1.0)
        return start + (end - start) * t

    @staticmethod
    def smoothstep(start, end, t):
        # Third degree Interpolator (Smoothstep)
        t = np.clip(t, 0.0, 1.0)
        t_smooth = 3 * t**2 - 2 * t**3
        return start + (end - start) * t_smooth

    @staticmethod
    def smootherstep(start, end, t):
        # Fifth degree Interpolator (Smoothstep)
        t = np.clip(t, 0.0, 1.0)
        t_smoother = 6 * t**5 - 15 * t**4 + 10 * t**3
        return start + (end - start) * t_smoother

    @staticmethod
    def get_t(elapsed, duration, start_time=0.0):
        # Support function to calculate normalized t from 0.0 to 1.0
        if duration <= 0:
            return 1.0
        t = (elapsed - start_time) / duration
        return np.clip(t, 0.0, 1.0)