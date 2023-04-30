import time
import threading

HEALTH_CHECKPOINTS = [0, 49, 99]  # a deer's status changes when its health reaches or goes below these thresholds


class Deer:
    """Facilitates creating and maintaining the deer"""

    def __init__(self):
        """
        Create a new Deer object.
        self.status == 0: deer is dead
        self.status == 1: deer is sad
        self.status == 2: deer is neutral
        self.status == 3: deer is happy
        """
        self.status = 3
        self.health = 100
        self.on_fire = False
        self.checkpoint_index = 2

    def set_on_fire(self, health_loss=5, num_secs=1):
        """
        Sets the deer on fire. The deer loses health_loss health for every num_secs seconds.
        """
        self.on_fire = True
        while self.on_fire and self.health > 0:
            time.sleep(num_secs)
            self.health -= health_loss
            if HEALTH_CHECKPOINTS[self.checkpoint_index - 1] < self.health <= HEALTH_CHECKPOINTS[self.checkpoint_index]:
                self.status -= 1
                self.checkpoint_index -= 1
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

    def get_status(self):
        """
        Return status of deer.
        """
        return self.status

    def get_health(self):
        """
        Return health of deer.
        """
        return self.health

    def is_on_fire(self):
        """
        Return whether the deer is on fire.
        """
        return self.on_fire

    def adjust_health_and_status(self):
        """
        Helper method.
        """
        if self.health <= 0:
            self.status = 0
            self.health = 0
