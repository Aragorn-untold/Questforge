document.addEventListener("DOMContentLoaded", function () {
  const autofillConfigs = [
    {
      dataId: "base-items-data",
      selectId: "id_base_item",
      fields: ["name", "type", "rarity", "description", "damage", "protection", "effect", "weight", "price"],
    },
    {
      dataId: "base-quests-data",
      selectId: "id_base_quest",
      fields: ["title", "description", "reward_description", "difficulty_rating", "level_recommendation"],
    },
    {
      dataId: "base-monsters-data",
      selectId: "id_base_monster",
      fields: ["name", "type", "alignment", "challenge_rating", "hit_points", "armor_class", "abilities"],
    },
  ];

  autofillConfigs.forEach(function (config) {
    const dataElement = document.getElementById(config.dataId);
    const selectElement = document.getElementById(config.selectId);

    if (!dataElement || !selectElement) return;

    const records = JSON.parse(dataElement.textContent);

    selectElement.addEventListener("change", function () {
      const record = records.find(function (candidate) {
        return String(candidate.id) === selectElement.value;
      });

      if (!record) return;

      config.fields.forEach(function (fieldName) {
        const field = document.getElementById("id_" + fieldName);
        if (field) field.value = record[fieldName] == null ? "" : record[fieldName];
      });
    });
  });
});
