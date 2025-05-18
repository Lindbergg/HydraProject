class Cycle:
    def __init__(self, players, hydras):
        self.players = players      # List[Player]
        self.hydras = hydras        # List[Hydra]
        self.current_value = 0      # Total worth from killed heads

    def apply_assignment(self, assignment):
        self.current_value = 0

        # Reset all hydra heads and players
        for hydra in self.hydras:
            hydra.reset()

        for player in self.players:
            player.attacks_left = 3

        # Apply attack assignments
        for player in self.players:
            attacks = assignment.get(player.name, [])
            for hydra_name, head_name in attacks:
                if player.attacks_left <= 0:
                    break

                hydra = next((h for h in self.hydras if h.name == hydra_name), None)
                if not hydra:
                    continue

                head = next((hd for hd in hydra.heads if hd.name == head_name), None)
                if not head or head.health <= 0:
                    continue

                damage = player.DamageToHead(hydra, head)
                if damage <= 0:
                    continue

                actual_damage = min(damage, head.health)
                head.health -= actual_damage
                player.attacks_left -= 1

                if head.health <= 0:
                    head.health = 0
                    self.current_value += head.worth
                    hydra.on_head_killed()

        # Return total health left across all hydras
        total_health_left = sum(
            head.health for hydra in self.hydras for head in hydra.heads if head.health > 0
        )
        return total_health_left, self.current_value
