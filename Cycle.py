class Cycle:
    def __init__(self, players, hydras):
        self.players = players  # List[Player] instances
        self.hydras = hydras    # List[Hydra] instances
        self.current_value = 0  # Total value gained from defeated heads

    def apply_assignment(self, assignment):
        """
        Applies a set of attack assignments and calculates the resulting hydra health
        and the value earned from defeating heads.
        """
        self.current_value = 0 

        # Reset the state of all hydra heads and player attack counts
        for hydra in self.hydras:
            hydra.reset()

        for player in self.players:
            player.attacks_left = 3

        # Process each player's assigned attacks
        for player in self.players:
            attacks = assignment.get(player.name, [])

            for hydra_name, head_name in attacks:
                if player.attacks_left <= 0:
                    break  # No attacks left for this player

                # Find the target hydra and head
                hydra = next((h for h in self.hydras if h.name == hydra_name), None)
                if not hydra:
                    continue

                head = next((hd for hd in hydra.heads if hd.name == head_name), None)
                if not head or head.health <= 0:
                    continue  # Head not found or already defeated

                # Calculate and apply damage
                damage = player.DamageToHead(hydra, head)
                if damage <= 0:
                    continue  # No effective damage

                actual_damage = min(damage, head.health)
                head.health -= actual_damage
                player.attacks_left -= 1

                if head.health <= 0:
                    head.health = 0
                    self.current_value += head.worth
                    hydra.on_head_killed()

        # Calculate total remaining health across all hydras
        total_health_left = sum(
            head.health for hydra in self.hydras for head in hydra.heads if head.health > 0
        )

        return total_health_left, self.current_value
