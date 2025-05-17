class Cycle:
    def __init__(self, players, hydra):
        self.players = players  # list of Player objects
        self.hydra = hydra      # list of Hydra objects

    def apply_assignment(self, assignment):
        # assignment: dict {player_name: list of (hydra_name, head_name)}

        # Reset hydra heads health and players attacks_left
        for hydra in self.hydra:
            for head in hydra.heads:
                head.reset()  # you may need a method to restore initial HP

        for player in self.players:
            player.attacks_left = 3

        total_kills = 0
        total_valle = 0

        for player in self.players:
            attacks = assignment.get(player.name, [])
            for (hydra_name, head_name) in attacks:
                if player.attacks_left <= 0:
                    break
                hydra = next((h for h in self.hydra if h.name == hydra_name), None)
                if hydra is None:
                    continue
                head = next((hd for hd in hydra.heads if hd.name == head_name), None)
                if head is None or head.health <= 0:
                    continue
                damage = player.DamageToHead(hydra, head)
                if damage <= 0:
                    continue

                actual_damage = min(damage, head.health)
                head.health -= actual_damage
                player.attacks_left -= 1

                if head.health <= 0:
                    total_kills += 1
                    total_valle += head.worth
                    hydra.HeadKilled()

        return total_valle
