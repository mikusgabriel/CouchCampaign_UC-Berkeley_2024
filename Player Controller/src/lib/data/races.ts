const races = {
    Human: {
        name: "Human",
        description: "Versatile and ambitious, humans are known for their adaptability.",
        "ability-buffs": [
            { name: "Strength", bonus: 1 },
            { name: "Dexterity", bonus: 1 },
            { name: "Constitution", bonus: 1 },
            { name: "Intelligence", bonus: 1 },
            { name: "Wisdom", bonus: 1 },
            { name: "Charisma", bonus: 1 },
        ],
        skills: ["Perception", "Athletics"],
    },
    Elf: {
        name: "Elf",
        description: "Graceful and wise, elves are known for their long lives and keen senses.",
        "ability-buffs": [{ name: "Dexterity", bonus: 2 }],
        skills: ["Perception", "Stealth"],
    },
    Dwarf: {
        name: "Dwarf",
        description: "Stout and sturdy, dwarves are known for their resilience and craftsmanship.",
        "ability-buffs": [{ name: "Constitution", bonus: 2 }],
        skills: ["History", "Athletics"],
    },
    Halfling: {
        name: "Halfling",
        description: "Small and nimble, halflings are known for their luck and bravery.",
        "ability-buffs": [{ name: "Dexterity", bonus: 2 }],
        skills: ["Stealth", "Acrobatics"],
    },
    Dragonborn: {
        name: "Dragonborn",
        description: "Strong and proud, dragonborn are known for their draconic heritage.",
        "ability-buffs": [
            { name: "Strength", bonus: 2 },
            { name: "Charisma", bonus: 1 },
        ],
        skills: ["Intimidation", "Athletics"],
    },
    Gnome: {
        name: "Gnome",
        description: "Inventive and curious, gnomes are known for their quick minds and affinity for magic.",
        "ability-buffs": [{ name: "Intelligence", bonus: 2 }],
        skills: ["Arcana", "Investigation"],
    },
    "Half-Elf": {
        name: "Half-Elf",
        description: "Blending the features of humans and elves, half-elves are known for their versatility and charm.",
        "ability-buffs": [
            { name: "Charisma", bonus: 2 },
            { name: "Strength", bonus: 1 },
            { name: "Dexterity", bonus: 1 },
        ],
        skills: ["Persuasion", "Deception"],
    },
    "Half-Orc": {
        name: "Half-Orc",
        description: "Strong and fierce, half-orcs are known for their combat prowess and resilience.",
        "ability-buffs": [
            { name: "Strength", bonus: 2 },
            { name: "Constitution", bonus: 1 },
        ],
        skills: ["Intimidation", "Athletics"],
    },
    Tiefling: {
        name: "Tiefling",
        description: "Descended from infernal heritage, tieflings are known for their dark magic and resilience.",
        "ability-buffs": [
            { name: "Charisma", bonus: 2 },
            { name: "Intelligence", bonus: 1 },
        ],
        skills: ["Arcana", "Deception"],
    },
} as const;

export default races;
export type RaceKey = keyof typeof races;
export type Race = (typeof races)[RaceKey];
