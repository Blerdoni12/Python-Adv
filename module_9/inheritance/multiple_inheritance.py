class Vertebrate:
    def __init__(self,backbone=True):
        self.has_backbone = backbone

    def vertebrate_info(self):
        print("Vertebrates have backbones")

class Aquatic:
    def __init__(self,habitat="Water"):
        self.habitat = habitat

    def aquatic_info(self):
        print("Aquatic animals live in water.")

class Fish(Vertebrate, Aquatic):
    def __init__(self,species,backbone=True, habitat="Water"):
        super().__init__(backbone=True )
        self.habitat = habitat
        self.species = species

    def fish_info(self):
        print(f"The {self.species} is a type of fish found in {self.habitat}.")

    def swim(self):
        print("The fish is swimming")

goldfish = Fish("Goldfish")
print(goldfish.has_backbone)
print(goldfish.habitat)
goldfish.vertebrate_info()
goldfish.aquatic_info()
goldfish.fish_info()
goldfish.swim()
