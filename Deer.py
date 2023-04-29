import time
import threading

HEALTH_CHECKPOINTS = [0, 33, 66]  # a deer's status changes when its health reaches or goes below these thresholds


class Deer:
    """Facilitates creating and maintaining the deer"""

    def __init__(self, name="Deer"):
        """
        Create a new Deer object.
        self.status = 0: deer is dead
        self.status = 1: deer is sad
        self.status = 2: deer is neutral
        self.status = 3: deer is happy
        """
        self.status = 3
        self.health = 100
        self.name = name
        self.on_fire = False

    def set_on_fire(self, health_loss=5, num_secs=1):
        """
        Sets the deer on fire. The deer loses health_loss health for every num_secs seconds.
        """
        self.on_fire = True
        checkpoint_index = 2
        while self.on_fire and self.health > 0:
            print(f"{self.name} is now at {self.health} health with {self.status} status")  # temporary indicator for deer's health
            time.sleep(num_secs)
            self.health -= health_loss
            if HEALTH_CHECKPOINTS[checkpoint_index - 1] < self.health <= HEALTH_CHECKPOINTS[checkpoint_index]:
                self.status -= 1
                checkpoint_index -= 1
        self.adjust_health_and_status()

    def put_out_fire(self):
        """
        Puts the deer out of fire.
        """
        self.on_fire = False
        self.adjust_health_and_status()

    def is_dead(self):
        """
        Return whether the deer is dead.
        """
        return self.health == 0

    def adjust_health_and_status(self):
        if self.health <= 0:
            self.status = 0
            self.health = 0


if __name__ == "__main__":
    """Examples of how to use the Deer object"""

    """EXAMPLE 1"""
    # set a new Deer object
    print("DEER 1")
    deer1 = Deer()

    # create and execute a new deer thread where the timer starts
    deer_thread = threading.Thread(target=deer1.set_on_fire)
    deer_thread.daemon = True
    deer_thread.start()

    # let the deer burn for 11 seconds
    time.sleep(11)
    deer1.put_out_fire()
    print(f"Name: {deer1.name}, Health: {deer1.health}, Status: {deer1.status}")

    """EXAMPLE 2"""
    print("\nDEER 2 (named Bob)")
    deer2 = Deer("Bob")

    deer_thread = threading.Thread(target=deer2.set_on_fire, args=(30, 1))
    deer_thread.daemon = True
    deer_thread.start()
    deer_thread.join()

    print(f"Name: {deer2.name}, Health: {deer2.health}, Status: {deer2.status}")
