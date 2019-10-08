function calculateFilter({
  selectedBiomes,
  selectedFeatures,
  selectedMaterials,
  selectedRegion
}) {
  var filter = {};
  if (selectedBiomes.length) {
    filter["biome"] = selectedBiomes;
  }
  if (selectedFeatures.length) {
    filter["feature"] = selectedFeatures;
  }
  if (selectedMaterials.length) {
    filter["material"] = selectedMaterials;
  }
  if (selectedRegion) {
    filter.selectedRegion = selectedRegion.geometry;
  }
  if (Object.keys(filter).length !== 0) {
    return filter;
  }
  return {};
}

export { calculateFilter };
