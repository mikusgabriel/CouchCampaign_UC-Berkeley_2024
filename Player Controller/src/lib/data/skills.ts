const skills = {
    Acrobatics: {
        name: "Acrobatics",
        description: "Ability to perform acrobatic feats, such as walking on a tight rope or performing somersaults.",
    },
    "Animal Handling": {
        name: "Animal Handling",
        description: "Ability to handle and control animals, as well as understand their behavior and needs.",
    },
    Arcana: {
        name: "Arcana",
        description: "Knowledge of magical theories, practices, and artifacts.",
    },
    Athletics: {
        name: "Athletics",
        description: "Ability to perform physical activities, such as climbing, jumping, or swimming.",
    },
    Deception: {
        name: "Deception",
        description: "Ability to lie, mislead, or conceal the truth.",
        associatedAbility: "Charisma",
    },
    History: {
        name: "History",
        description: "Knowledge of historical events, cultures, and figures.",
        associatedAbility: "Intelligence",
    },
    Insight: {
        name: "Insight",
        description: "Ability to read and understand people's emotions, motivations, and intentions.",
        associatedAbility: "Wisdom",
    },
    Intimidation: {
        name: "Intimidation",
        description: "Ability to influence others through threats, hostile actions, or physical presence.",
        associatedAbility: "Charisma",
    },
    Investigation: {
        name: "Investigation",
        description: "Ability to find and analyze clues, evidence, and information.",
        associatedAbility: "Intelligence",
    },
    Medicine: {
        name: "Medicine",
        description: "Knowledge of diseases, injuries, and their treatments.",
        associatedAbility: "Wisdom",
    },
    Nature: {
        name: "Nature",
        description: "Knowledge of plants, animals, and natural environments.",
        associatedAbility: "Intelligence",
    },
    Perception: {
        name: "Perception",
        description: "Ability to notice and observe details in the environment.",
        associatedAbility: "Wisdom",
    },
    Performance: {
        name: "Performance",
        description: "Ability to entertain through acting, music, or other forms of performance.",
        associatedAbility: "Charisma",
    },
    Persuasion: {
        name: "Persuasion",
        description: "Ability to influence others through negotiation, flattery, or other forms of persuasion.",
        associatedAbility: "Charisma",
    },
    Religion: {
        name: "Religion",
        description: "Knowledge of deities, religious practices, and mythological lore.",
        associatedAbility: "Intelligence",
    },
    "Sleight of Hand": {
        name: "Sleight of Hand",
        description: "Ability to perform dexterous acts, such as picking pockets or using slight-of-hand tricks.",
        associatedAbility: "Dexterity",
    },
    Stealth: {
        name: "Stealth",
        description: "Ability to move silently and conceal oneself from view.",
        associatedAbility: "Dexterity",
    },
    Survival: {
        name: "Survival",
        description:
            "Ability to navigate and survive in the wilderness, including tracking, hunting, and finding sustenance.",
        associatedAbility: "Wisdom",
    },
} as const;

export default skills;
export type SkillKey = keyof typeof skills;
export type Skill = (typeof skills)[SkillKey];
