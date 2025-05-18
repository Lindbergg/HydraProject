class Hydra:
    def __init__(self, name, heads):
        self.name = name        # str
        self.heads = heads      # List[Head]

    def reset(self):
        for head in self.heads:
            head.reset()

    def is_alive(self):
        return any(head.health > 0 for head in self.heads)

    def on_head_killed(self):
        # Update the worth of all remaining heads
        for head in self.heads:
            if head.health > 0:
                head.updateWorth()

    def total_health_left(self):
        return sum(head.health for head in self.heads if head.health > 0)

    def __hash__(self):
        return hash(self.name)
