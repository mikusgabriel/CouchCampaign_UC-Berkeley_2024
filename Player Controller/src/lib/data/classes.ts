const classes = {
    Barbarian: {
        name: "Barbarian",
        description: "A fierce warrior of primitive background who can enter a battle rage.",
        UseSpells: false,
        SpellcastingAbility: null,
        skills: ["Athletics", "Intimidation", "Survival"],
        savingThrows: ["Strength", "Constitution"],
    },
    Bard: {
        name: "Bard",
        description: "An inspiring magician whose power echoes the music of creation.",
        UseSpells: true,
        SpellcastingAbility: "Charisma",
        skills: ["Performance", "Persuasion", "Deception"],
        savingThrows: ["Dexterity", "Charisma"],
    },
    Cleric: {
        name: "Cleric",
        description: "A priestly champion who wields divine magic in service of a higher power.",
        UseSpells: true,
        SpellcastingAbility: "Wisdom",
        skills: ["Insight", "Medicine", "Religion"],
        savingThrows: ["Wisdom", "Charisma"],
    },
    Druid: {
        name: "Druid",
        description: "A priest of the Old Faith, wielding the powers of nature and adopting animal forms.",
        UseSpells: true,
        SpellcastingAbility: "Wisdom",
        skills: ["Animal Handling", "Nature", "Survival"],
        savingThrows: ["Intelligence", "Wisdom"],
    },
    Fighter: {
        name: "Fighter",
        description: "A master of martial combat, skilled with a variety of weapons and armor.",
        UseSpells: false,
        SpellcastingAbility: null,
        skills: ["Athletics", "Perception", "Intimidation"],
        savingThrows: ["Strength", "Constitution"],
    },
    Monk: {
        name: "Monk",
        description:
            "A master of martial arts, harnessing the power of the body in pursuit of physical and spiritual perfection.",
        UseSpells: false,
        SpellcastingAbility: null,
        skills: ["Acrobatics", "Athletics", "Stealth"],
        savingThrows: ["Strength", "Dexterity"],
    },
    Paladin: {
        name: "Paladin",
        description: "A holy warrior bound to a sacred oath.",
        UseSpells: true,
        SpellcastingAbility: "Charisma",
        skills: ["Athletics", "Insight", "Religion"],
        savingThrows: ["Wisdom", "Charisma"],
    },
    Ranger: {
        name: "Ranger",
        description:
            "A warrior who uses martial prowess and nature magic to combat threats on the edges of civilization.",
        UseSpells: true,
        SpellcastingAbility: "Wisdom",
        skills: ["Animal Handling", "Nature", "Survival"],
        savingThrows: ["Strength", "Dexterity"],
    },
    Rogue: {
        name: "Rogue",
        description: "A scoundrel who uses stealth and trickery to overcome obstacles and enemies.",
        UseSpells: false,
        SpellcastingAbility: null,
        skills: ["Acrobatics", "Stealth", "Deception"],
        savingThrows: ["Dexterity", "Intelligence"],
    },
    Sorcerer: {
        name: "Sorcerer",
        description: "A spellcaster who draws on inherent magic from a gift or bloodline.",
        UseSpells: true,
        SpellcastingAbility: "Charisma",
        skills: ["Arcana", "Deception", "Persuasion"],
        savingThrows: ["Constitution", "Charisma"],
    },
    Warlock: {
        name: "Warlock",
        description: "A wielder of magic that is derived from a bargain with an extraplanar entity.",
        UseSpells: true,
        SpellcastingAbility: "Charisma",
        skills: ["Arcana", "Deception", "Intimidation"],
        savingThrows: ["Wisdom", "Charisma"],
    },
    Wizard: {
        name: "Wizard",
        description: "A scholarly magic-user capable of manipulating the structures of reality.",
        UseSpells: true,
        SpellcastingAbility: "Intelligence",
        skills: ["Arcana", "History", "Investigation"],
        savingThrows: ["Intelligence", "Wisdom"],
    },
} as const;

export default classes;
export type ClasseKey = keyof typeof classes;
export type Classe = (typeof classes)[ClasseKey];
