import random


TITLE = "Rogue Dice Arena"


def roll_dice(count: int, sides: int) -> int:
    return sum(random.randint(1, sides) for _ in range(count))


def enemy_for_round(round_no: int) -> dict:
    names = ["Rat King", "Rust Golem", "Night Coder", "Bug Hydra", "Null Wizard"]
    name = random.choice(names)
    hp = 12 + round_no * 4
    power = 4 + round_no
    return {"name": name, "hp": hp, "power": power}


def ask_choice(prompt: str, options: list[str]) -> str:
    options_lower = [o.lower() for o in options]
    while True:
        value = input(prompt).strip().lower()
        if value in options_lower:
            return value
        print(f"Pick one of: {', '.join(options)}")


def shop(player: dict) -> None:
    print("\nShop appears. Spend 4 gold:")
    print("1) +5 max HP")
    print("2) +1 attack die")
    print("3) +2 healing potion")
    if player["gold"] < 4:
        print("Not enough gold.")
        return

    choice = ask_choice("Choose 1/2/3 or skip: ", ["1", "2", "3", "skip"])
    if choice == "skip":
        return

    player["gold"] -= 4
    if choice == "1":
        player["max_hp"] += 5
        player["hp"] += 5
        print("Max HP increased.")
    elif choice == "2":
        player["atk_dice"] += 1
        print("Attack power increased.")
    else:
        player["potions"] += 2
        print("Potions stocked.")


def battle(player: dict, round_no: int) -> bool:
    enemy = enemy_for_round(round_no)
    print(f"\nRound {round_no}: {enemy['name']} appears (HP {enemy['hp']})")

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYou HP: {player['hp']}/{player['max_hp']} | Potions: {player['potions']} | Gold: {player['gold']}")
        print(f"Enemy HP: {enemy['hp']}")
        action = ask_choice("Action [attack/heal/run]: ", ["attack", "heal", "run"])

        if action == "run":
            print("You escaped, but lose 2 gold.")
            player["gold"] = max(0, player["gold"] - 2)
            return True

        if action == "heal":
            if player["potions"] <= 0:
                print("No potions left.")
            else:
                heal = roll_dice(2, 4)
                player["potions"] -= 1
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                print(f"You heal for {heal}.")

        if action == "attack":
            dmg = roll_dice(player["atk_dice"], 6)
            enemy["hp"] -= dmg
            print(f"You strike for {dmg}.")

        if enemy["hp"] > 0:
            enemy_dmg = roll_dice(1, enemy["power"])
            player["hp"] -= enemy_dmg
            print(f"{enemy['name']} hits you for {enemy_dmg}.")

    if player["hp"] <= 0:
        print("You were defeated.")
        return False

    reward = 3 + round_no
    player["gold"] += reward
    print(f"Victory. You gain {reward} gold.")
    return True


def main() -> None:
    print(f"=== {TITLE} ===")
    print("Survive 7 rounds to win.\n")

    player = {
        "hp": 24,
        "max_hp": 24,
        "atk_dice": 2,
        "potions": 2,
        "gold": 0,
    }

    for round_no in range(1, 8):
        if not battle(player, round_no):
            print("\nGame Over.")
            return
        if round_no % 2 == 0:
            shop(player)

    print("\nYou cleared the arena. Champion status unlocked.")


if __name__ == "__main__":
    random.seed()
    main()
