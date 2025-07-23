#Kanna Yamamoto

# Smart Carpark System 

from datetime import datetime
import random

#Car class
class Car:
    def __init__(self, license_plate, model):
        self.license_plate = license_plate
        self.model = model
        self.entry_time = datetime.now()
        self.exit_time = None

    def exit(self):
        self.exit_time = datetime.now()

#Carpark class
class Carpark:
    def __init__(self, total_spaces):
        self.total_spaces = total_spaces
        self.cars = []
        self.temperature = self.read_temperature_from_file()

    def read_temperature_from_file(self):
        try:
            with open('temperature.txt', 'r') as f:
                return float(f.read().strip())
        except:
            return random.uniform(20.0, 30.0)

    def incoming_car(self, car):
        if len(self.cars) < self.total_spaces:
            self.cars.append(car)
            print(f"✅ {car.license_plate} entered at {car.entry_time.strftime('%H:%M:%S')}")
            self.log_event(f"Car entered: {car.license_plate}| Temp: {self.temperature}°C")
        else:
            print(" Carpark is full!")

    def outgoing_car(self, license_plate):
        for car in self.cars:
            if car.license_plate == license_plate:
                car.exit()
                self.cars.remove(car)
                print(f"🚗 {car.license_plate} exited at {car.exit_time.strftime('%H:%M:%S')}")
                self.log_event(f"Car exited: {car.license_plate}| Temp: {self.temperature}°C")
                return
        print(" Car not found!")

    def available_spaces(self):
        return self.total_spaces - len(self.cars)

    def display_status(self):
        print("=== Carpark Status ===")
        print(f"Available Spaces: {self.available_spaces()} / {self.total_spaces}")
        print(f"Current Temperature: {self.temperature:.1f} °C")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")

    def log_event(self, message):
        with open("log.txt", "a") as log_file:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{time_str}]{message}\n")

#Entry / Exit Sensor 
def simulate():
    carpark = Carpark(total_spaces=5)
    carpark.display_status()

    car1 = Car("ABC123", "Toyota")
    car2 = Car("XYZ789", "Honda")

    carpark.incoming_car(car1)
    carpark.incoming_car(car2)
    carpark.display_status()

    carpark.outgoing_car("ABC123")
    carpark.display_status()

if __name__ == '__main__':
    simulate()
