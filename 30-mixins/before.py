from __future__ import annotations
from dataclasses import dataclass


@dataclass
class GameCharacter:
    name: str
    hp: int
    level: int

    def compute_damage(self) -> int:
        return self.level * 10

    def attack(self, target: GameCharacter) -> None:
        damage = self.compute_damage()
        target.hp -= damage
        if isinstance(target, Knight):
            damage -= target.shield
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        if target.hp <= 0:
            print(f"{target.name} has been defeated!")


@dataclass
class PowerUp:
    damage: int


@dataclass
class Knight(PowerUp, GameCharacter):
    shield: int = 100

    def compute_damage(self) -> int:
        return self.level * 10 + self.damage


@dataclass
class Spell:
    damage: int
    mana_cost: int


@dataclass
class Wizard(Spell, GameCharacter):
    mana: int = 100

    def compute_damage(self) -> int:
        if self.mana < self.mana_cost:
            return self.level * 100
        else:
            self.mana -= self.mana_cost
            return self.level * 10 + self.damage


def main() -> None:
    knight = Knight("Sir Foo", 1000, 10, 100, 100)
    wizard = Wizard("Archibald", 1000, 5, 100, 100)
    knight.attack(wizard)
    wizard.attack(knight)
    knight.attack(wizard)
    wizard.attack(knight)
    knight.attack(wizard)
    wizard.attack(knight)


if __name__ == "__main__":
    main()
