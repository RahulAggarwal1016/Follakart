import time


# Creates class object for the PID controller
class PID:
    """
        Parameters:
            @param kproportional = proportional gain
            @param kintegral = integral gain
            @param kderivative  = dereivative gainn
            @param maximum_integral = maximum magnitude of integral to prevent integral windup
            @param maximum_output = maximum PWM output possible

            @return => void function
    """

    def __init__(self, kproportional, kintegral, kderivative, maximum_integral, minimum_output, maximum_output):
        self.kp = kproportional
        self.ki = kintegral
        self.kd = kderivative
        self.integral = 0
        self.max_integral = maximum_integral
        self.min_out = minimum_output  # Below this and motors won't spin
        self.max_out = maximum_output
        self.past_positions = [0, 0]  # Stores past positions of the object for derivative calculations
        self.measurement_time = [time.time(), 0]
        # print("PID Controller Constructed") # Debugging purposes

    """
        Parameters:
            @param current = current value between ball and car
            @param desired = deisred value

            @return = PWM value for motors (motor power)
    """

    def get_output(self, current, desired):
        # print("Getting output") # Debugging purposes
        print("INput vlaues: ", str(current), " ", str(desired))

        error = abs(desired - current)

        # Determines derivative value
        self.past_positions[1] = self.past_positions[0]
        self.past_positions[0] = current

        self.measurement_time[1] = self.measurement_time[0]
        self.measurement_time[0] = time.time()

        # print(str(self.measurement_time[1]))

        derivative = current - self.past_positions[1]

        # Determines integral value
        self.integral = self.integral + error

        if self.integral > self.max_integral:
            self.integral = self.max_integral
        elif self.integral < self.max_integral * -1:
            self.integral = self.max_integral * -1

        # If error is less than a specified amount, then integral value is dropped to reduce speed
        if abs(error) < 10 and error != 0:
            self.integral = round(self.integral / 4)
        # If error is zero, output is set to zero
        elif error == 0:
            self.integral = 0
            derivative = 0

        # Calculates required motor output and ensures it stays within min and max values
        motor_output = round(error * self.kp + self.integral * self.ki + derivative * self.kd)
        print("Raw value: ", str(motor_output))

        if motor_output < self.min_out:
            motor_output = self.min_out
        elif motor_output > self.max_out:
            motor_output = self.max_out

        print("Values: ", str(error), "; ", str(self.integral), "; ", str(derivative))
        print("Output: ", str(motor_output))
        print()

        return motor_output  # Returns the required PWM value




