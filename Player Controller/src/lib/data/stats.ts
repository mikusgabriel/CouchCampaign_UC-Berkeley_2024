const stats = {
    Strength: {
        name: "Strength",
        description: "Measures a character's raw physical power and ability to exert force.",
    },
    Dexterity: {
        name: "Dexterity",
        description: "Measures a character's agility, reflexes, and balance.",
    },
    Constitution: {
        name: "Constitution",
        description: "Measures a character's endurance, stamina, and overall health.",
    },
    Intelligence: {
        name: "Intelligence",
        description: "Measures a character's reasoning ability, memory, and ability to analyze information.",
    },
    Wisdom: {
        name: "Wisdom",
        description: "Measures a character's intuition, perception, and decision-making ability.",
    },
    Charisma: {
        name: "Charisma",
        description: "Measures a character's force of personality, persuasiveness, and leadership qualities.",
    },
} as const;

export default stats;
export type StatsKey = keyof typeof stats;
export type Stat = (typeof stats)[StatsKey];
